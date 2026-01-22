import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Fixed categories for prompt enhancement
CATEGORIES = {
    "subject": "The main subject or focal point",
    "setting": "The environment, background, or location",
    "style": "Visual style, art medium, or aesthetic",
    "lighting": "Lighting conditions and mood/atmosphere",
    "details": "Additional elements, objects, or features",
}


def analyze_prompt(user_prompt):
    """
    Takes a generic user prompt and returns suggested options for each category.
    Returns a dict with category names as keys and lists of suggestions as values.
    """

    system_prompt = """You are an expert at enhancing image generation prompts.
Given a user's basic prompt, generate creative and diverse suggestions for each category.

IMPORTANT RULES:
1. For "subject": ALWAYS include the action, pose, or activity mentioned by the user.
   - If user says "woman looking at sunset" → subject should include "looking at" or "gazing at"
   - If user says "dog playing" → subject should include "playing" or the specific action
   - Don't separate the subject from what they're doing

2. For "style": ALWAYS include "Photorealistic, high detail, natural colors" as the first option

3. Provide 4-5 specific, varied options for each category

Return your response as a JSON object with this structure:
{
  "subject": ["option 1 WITH action/pose", "option 2 WITH action/pose", ...],
  "setting": ["option 1", "option 2", ...],
  "style": ["Photorealistic, high detail, natural colors", "option 2", ...],
  "lighting": ["option 1", "option 2", ...],
  "details": ["option 1", "option 2", ...]
}"""

    user_message = f"""User's prompt: "{user_prompt}"

Generate suggestions for these categories:
- subject: {CATEGORIES['subject']} - MUST include the action/pose/activity from the user's prompt
- setting: {CATEGORIES['setting']}
- style: {CATEGORIES['style']} (MUST include "Photorealistic, high detail, natural colors" as first option)
- lighting: {CATEGORIES['lighting']}
- details: {CATEGORIES['details']}

Remember: The subject options should describe both WHO/WHAT and WHAT THEY'RE DOING."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
        )

        import json

        suggestions = json.loads(response.choices[0].message.content)

        # Safety check: ensure realistic option is in style
        if "style" in suggestions:
            realistic_option = "Photorealistic, high detail, natural colors"
            if realistic_option not in suggestions["style"]:
                suggestions["style"].insert(0, realistic_option)

        return suggestions

    except Exception as e:
        print(f"Error in analyze_prompt: {e}")
        return None


if __name__ == "__main__":
    test_prompt = "dog in snow"
    result = analyze_prompt(test_prompt)

    if result:
        print("Suggestions:")
        import json

        print(json.dumps(result, indent=2))

        if "Photorealistic" in result.get("style", []):
            print("\n✅ Realistic option is present in style!")
        else:
            print("\n❌ Warning: Realistic option missing!")
    else:
        print("Failed to get suggestions")
