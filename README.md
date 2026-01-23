# Image Prompt Generator

An interactive AI-powered image generation tool that helps users transform generic prompts into detailed, customized images.

## Features
- LLM-powered prompt enhancement
- Interactive tag selection interface
- Custom prompt options
- GPT-Image-1.5 integration
- Download generated images

## Live Demo
🚀 [Try it live on Hugging Face Spaces](https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME)

## Setup

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your API keys:
```
   OPENAI_API_KEY=your_key_here
```
4. Run: `streamlit run app.py`

### Deployment
This app is deployed on Hugging Face Spaces using the free tier. To deploy your own:
1. Create a Hugging Face account
2. Create a new Space with Docker SDK
3. Upload `app.py` and `requirements.txt`
4. Add your `OPENAI_API_KEY` in Space settings → Repository secrets

## Tech Stack
- Streamlit
- OpenAI GPT-4o-mini (prompt analysis)
- OpenAI GPT-Image-1.5 (image generation)
- Hosted on Hugging Face Spaces