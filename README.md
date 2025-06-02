# text-to-image-save-image
This project uses the Stable Diffusion Pipeline to generate images from text prompts. The Stable Diffusion Pipeline is a machine learning model that uses a diffusion process to generate images from text prompts. This is a simple GUI application for generating images based on user prompts.


## Table of Contents

- [Requirements](#requirements)
- [Description](#description)
- [HuggingFace Account Setup](#HuggingFaceAccountSetup)
- [Deploy the App](#DeploytheApp)
- [License](#license)


## Requirements

- You need a DigitalOcean account. If you do not already have one, first [sign up](https://cloud.digitalocean.com/registrations/new?utm_team=devrel&utm_source=github&utm_content=signup).

- HuggingFace [account](https://huggingface.co/)

- [Stable Diffusion Model](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)


## Description

When you run the code, you will be prompted to enter a text prompt. Once you have entered a text prompt, the Stable Diffusion Pipeline will generate an image based on the text prompt. The generated image will be displayed using matplotlib.

This [web service]([https://txt-to-img-s92go.ondigitalocean.app/]) hosted on DigitalOcean App Platform  will give you a prompt to enter a text. Once you have entered a text prompt, the Stable Diffusion Pipeline will generate an image based on the text prompt. The website uses the Latent Diffusion Model to create and display the image as per user's input.

[Autoscaling](https://www.digitalocean.com/blog/introducing-cpu-based-autoscaling-app-platform?utm_team=devrel&utm_source=github&utm_content=blog) is also enabled in the deployed app to ensure that the app can handle increased traffic. To learn more about autoscaling, see the [Autoscaling video by Bikram Gupta](https://www.youtube.com/watch?v=k8pCGYPeqOQ).


## HuggingFace Account Setup

To run this file you need a HuggingFace API Token.

1. Go to the Hugging Face [website](https://huggingface.co/)
2. Click on the "Sign In" button in the top-right corner of the page.
3. Sign in with your Hugging Face account or create a new account if you don't have one.
4. Once you are signed in, click on your profile picture in the top-right corner of the page and select "Account settings" from the dropdown menu.
5. On the account settings page, click on the "API token" tab.
6. Click on the "Generate new token" button to create a new authorization token.
7. Enter a name for your token in the "Token name" field (e.g. "Image Generator App").
8. Choose the permissions you want to grant to your token (e.g. "Read-only" or "Full access").
9. Click on the "Generate" button to create your token.
10. Copy the generated token and use it in your Python code where it says self.authorization_token = "".
