import os
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable.")

MODEL_NAME = "claude-3-sonnet-20240229"  # Update this to the correct model name

def analyze_codebase_with_anthropic_claude(description: str, codebase: dict) -> str:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Analyze the following codebase:
    
    Description: {description}
    Total files: {codebase['file_count']}
    Total lines of code: {codebase['total_lines']}
    File types distribution: {codebase['file_types']}
    
    Please provide a comprehensive analysis of the codebase, including:
    1. Overall structure and organization
    2. Potential improvements or best practices that could be applied
    3. Any security concerns or performance issues
    4. Suggestions for better code maintainability and scalability
    
    Here's a sample of the code files:
    """
    
    for file in codebase['file_list'][:5]:  # Limit to 5 files to avoid exceeding token limits
        prompt += f"\n\nFile: {file['path']}\n```\n{file['contents'][:1000]}...\n```"

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error calling Anthropic API: {str(e)}")
        return "Error: Unable to analyze codebase with Claude."
