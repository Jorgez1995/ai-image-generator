# AI Image Generator

An interactive AI-powered image generation tool that helps users transform generic prompts into detailed, customized images.

## Features
- LLM-powered prompt enhancement
- Interactive tag selection interface
- Custom prompt options
- GPT-Image-1 integration
- Download generated images

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your API keys:
```
   OPENAI_API_KEY=your_key_here
```
4. Run: `streamlit run app.py`

## Tech Stack
- Streamlit
- OpenAI GPT-4o-mini (prompt analysis)
- OpenAI GPT-Image-1 (image generation)