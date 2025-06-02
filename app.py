from flask import Flask, request, jsonify, send_file, render_template
import requests
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import uuid
from datetime import datetime
import os

app = Flask(__name__, static_folder="static", template_folder="static")

HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HF_API_KEY = "Bearer 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"

# DigitalOcean Spaces configuration
SPACES_BUCKET = 'photosnap-bucket'
SPACES_REGION = 'sgp1'
SPACES_ENDPOINT = 'https://sgp1.digitaloceanspaces.com'

def configure_spaces_client():
    """Configure boto3 client for DigitalOcean Spaces"""
    try:
        session = boto3.session.Session()
        client = session.client('s3',
                              region_name=SPACES_REGION,
                              endpoint_url=SPACES_ENDPOINT,
                              aws_access_key_id=os.getenv('DO_SPACES_KEY'),
                              aws_secret_access_key=os.getenv('DO_SPACES_SECRET'))
        return client
    except Exception as e:
        print(f"Failed to configure DigitalOcean Spaces client: {e}")
        return None

def upload_to_spaces(image_bytes, filename):
    """Upload image to DigitalOcean Spaces and return public URL"""
    client = configure_spaces_client()
    if not client:
        return None
    
    try:
        # Upload the image
        client.put_object(
            Bucket=SPACES_BUCKET,
            Key=filename,
            Body=image_bytes,
            ContentType='image/png',
            ACL='public-read'  # Make the file publicly accessible
        )
        
        # Return the public URL
        url = f"https://{SPACES_BUCKET}.{SPACES_REGION}.digitaloceanspaces.com/{filename}"
        return url
    except NoCredentialsError:
        print("DigitalOcean Spaces credentials not found")
        return None
    except ClientError as e:
        print(f"Failed to upload to DigitalOcean Spaces: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during upload: {e}")
        return None

# Serve the index.html at the root URL
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    headers = {
        "Authorization": HF_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt, "options": {"wait_for_model": True}})
    
    if response.status_code == 200:
        image_data = response.content
        return send_file(BytesIO(image_data), mimetype="image/png")
    else:
        return jsonify({"error": "Failed to generate image"}), response.status_code

@app.route('/upload-to-spaces', methods=['POST'])
def upload_image_to_spaces():
    """Upload the generated image to DigitalOcean Spaces"""
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # First generate the image
    headers = {
        "Authorization": HF_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt, "options": {"wait_for_model": True}})
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to generate image"}), response.status_code
    
    image_data = response.content
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    # Create a safe filename from prompt (first 30 chars, replace spaces and special chars)
    safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_prompt = safe_prompt.replace(' ', '_')
    filename = f"generated_images/{safe_prompt}_{timestamp}_{unique_id}.png"
    
    # Upload to DigitalOcean Spaces
    upload_url = upload_to_spaces(image_data, filename)
    
    if upload_url:
        return jsonify({
            "success": True,
            "message": "Image uploaded successfully to DigitalOcean Spaces",
            "url": upload_url,
            "filename": filename
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to upload image to DigitalOcean Spaces"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    # Check if required environment variables are set
    if not os.getenv('DO_SPACES_KEY') or not os.getenv('DO_SPACES_SECRET'):
        print("Warning: DigitalOcean Spaces credentials not found.")
        print("Please set DO_SPACES_KEY and DO_SPACES_SECRET environment variables.")
        print("Upload to Spaces functionality will not work without these credentials.")
    
    app.run(host='0.0.0.0', port=8080)
