import os
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable.")

MODEL_NAME = "claude-3-sonnet-20240229"  # Update this to the correct model name

def load_system_prompt():
    with open("system_prompt.md", "r") as file:
        return file.read()

def analyze_codebase_with_anthropic_claude(description: str, codebase: dict) -> str:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    system_prompt = load_system_prompt()

    import json

    user_prompt = f"""Analyze the following codebase:
    
    Description: {description}
    
    Codebase details:
    {json.dumps(codebase, indent=2, default=str)}
    """
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error calling Anthropic API: {str(e)}")
        return "Error: Unable to analyze codebase with Claude."
