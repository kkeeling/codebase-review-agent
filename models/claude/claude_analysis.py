import json
import os
import time
import requests
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable.")

MODEL_NAME = "claude-3-sonnet-20240229"  # Update this to the correct model name

def load_system_prompt():
    url = "https://raw.githubusercontent.com/kkeeling/codebase-review-agent/main/models/claude/system_prompt.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch system prompt. Status code: {response.status_code}")

def analyze_codebase_with_anthropic_claude(description: str, codebase: dict) -> str:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    system_prompt = load_system_prompt()

    user_prompt = f"""Analyze the following codebase:
    
    Description: {description}
    
    Codebase details:
    {json.dumps(codebase, indent=2, default=str)}
    """

    # Write user_prompt to log file
    epoch_time = int(time.time())
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"session_{epoch_time}.log")
    with open(log_file, "w") as f:
        f.write(user_prompt)
        
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
