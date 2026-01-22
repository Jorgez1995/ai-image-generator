import os
import time
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_image(prompt_dict):
    """
    Generate image from structured prompt dictionary.
    Returns: (image_bytes, generation_time) or (None, 0) on error
    """

    # Convert JSON prompt to natural language
    prompt_text = f"""Create an image with the following specifications:

Subject: {prompt_dict['subject']}
Setting: {prompt_dict['setting']}
Style: {prompt_dict['style']}
Lighting: {prompt_dict['lighting']}
Additional details: {prompt_dict['details']}

Generate a cohesive, high-quality image incorporating all these elements."""

    try:
        # Start timer
        start_time = time.time()

        # Generate image using OpenAI Images API
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt_text,
            size="1024x1024",
            quality="medium",
            n=1,
        )

        # Calculate generation time
        generation_time = time.time() - start_time

        # GPT Image models return base64-encoded images
        image_b64 = response.data[0].b64_json

        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_b64)

        return image_bytes, generation_time

    except Exception as e:
        print(f"Error generating image: {e}")
        return None, 0


# Test function
if __name__ == "__main__":
    test_prompt = {
        "subject": "a playful golden retriever bounding through the snow",
        "setting": "a tranquil snowy forest with towering pine trees",
        "style": "a sharp, hyper-realistic digital illustration",
        "lighting": "a warm golden sunset casting long shadows on the snow",
        "details": "paw prints trailing off into the distance",
    }

    print("Generating image...")
    image_bytes, gen_time = generate_image(test_prompt)

    if image_bytes:
        # Save to file
        with open("test_image.png", "wb") as f:
            f.write(image_bytes)
        print(f"✅ Image generated in {gen_time:.2f} seconds")
        print(f"Saved to: test_image.png")
    else:
        print("❌ Failed to generate image")
