import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def analyze_codebase_with_google_gemini(description: str, codebase: dict) -> str:
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Analyze the following codebase:
    
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
    
    for file in codebase['file_list']:
        prompt += f"\n\nFile: {file['path']}\n```\n{file['contents']}...\n```"
    
    safety_settings = [
        {
            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
    ]

    response = model.generate_content(
        prompt,
        safety_settings=safety_settings,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            top_p=1,
            top_k=32,
            max_output_tokens=2048,
        )
    )

    return response.text
