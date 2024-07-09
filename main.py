import os
import sys
import json
import requests
from typing import List, Dict, Any
from colorama import init, Fore, Style
from halo import Halo

# Initialize colorama
init(autoreset=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable.")

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL_NAME = "claude-3-sonnet-20240229"

def get_user_input():
    print(Fore.GREEN + "Welcome to the Interactive Codebase Review Agent!")
    print(Fore.GREEN + "Please provide the following information:")
    
    description = input(Fore.YELLOW + "1. Brief description of the codebase, including the type of application: ")
    technologies = input(Fore.YELLOW + "2. Main technologies used (comma-separated): ")
    
    root_folder = input(Fore.YELLOW + "3. Root folder of the project on your local file system: ")
    
    return description, technologies, root_folder

def validate_input(description: str, technologies: str, root_folder: str) -> bool:
    if not description or not technologies or not root_folder:
        print(Fore.RED + "Error: All fields are required.")
        return False
    
    if not os.path.isdir(root_folder):
        print(Fore.RED + f"Error: The specified root folder '{root_folder}' does not exist.")
        return False
    
    return True

def analyze_codebase_structure(root_folder: str) -> Dict[str, Any]:
    file_count = 0
    total_lines = 0
    file_types = {}
    file_list = []

    # If root folder contains a .gitignore file, identify those files and directories
    gitignore_patterns = []
    if os.path.exists(os.path.join(root_folder, '.gitignore')):
        with open(os.path.join(root_folder, '.gitignore'), 'r') as f:
            gitignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for root, dirs, files in os.walk(root_folder):
        # Remove hidden directories from the dirs list
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            # Skip hidden files and files matching gitignore patterns
            if file.startswith('.') or any(file.endswith(pattern) for pattern in gitignore_patterns):
                continue
            
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_folder)
            file_count += 1
            
            _, extension = os.path.splitext(file)
            file_types[extension] = file_types.get(extension, 0) + 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_lines += content.count('\n') + 1
                    file_list.append({"path": relative_path, "contents": content})
            except Exception as e:
                print(Fore.YELLOW + f"Warning: Could not read file {file_path}. Error: {str(e)}")
                file_list.append({"path": relative_path, "contents": f"Error: Unable to read file. {str(e)}"})

    return {
        "file_count": file_count,
        "total_lines": total_lines,
        "file_types": file_types,
        "file_list": file_list
    }

def get_claude_suggestion(description: str, technologies: str, codebase_analysis: Dict[str, Any]) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    prompt = f"""Based on the following information about a codebase, suggest a good starting point for analysis:

Description: {description}
Technologies: {technologies}

File Count: {codebase_analysis['file_count']}
Total Lines of Code: {codebase_analysis['total_lines']}

File Types Distribution:
{json.dumps(codebase_analysis['file_types'], indent=2)}

File Structure:
{json.dumps(codebase_analysis['file_list'], indent=2)}

Please suggest a specific file that would be a good starting point for analyzing this codebase. Respond only with the file name, without any additional explanation or text.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    data = {
        "model": MODEL_NAME,
        "max_tokens": 1000,
        "messages": messages
    }

    with Halo(text='Waiting for Claude\'s response...', spinner='dots'):
        response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
        response.raise_for_status()

    return response.json()["content"][0]["text"].strip()

def get_file_content(file_path: str) -> str:
    encodings = ['utf-8', 'latin-1', 'ascii']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return f"Error: Unable to read file {file_path} with any of the attempted encodings."

def analyze_file(file_path: str, file_content: str, description: str, technologies: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    prompt = f"""Analyze the following file from a codebase:

File: {file_path}
Description of codebase: {description}
Technologies used: {technologies}

File content:
{file_content}

Please provide a detailed analysis of this file, including:
1. The purpose and functionality of the code in this file
2. How it fits into the overall structure of the codebase
3. Any notable coding patterns or practices used
4. Potential areas for improvement or optimization
5. Any security concerns or best practices that should be implemented
6. Suggestions for better documentation or testing, if applicable

Your analysis should be thorough and provide valuable insights for the development team.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    data = {
        "model": MODEL_NAME,
        "max_tokens": 2000,
        "messages": messages
    }

    with Halo(text='Analyzing file...', spinner='dots'):
        response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
        response.raise_for_status()

    return response.json()["content"][0]["text"]

def run_sequential_agentic_flow():
    print(Fore.BLUE + "Running sequential agentic flow...")

    step_1_triggering()

    description, technologies, root_folder = step_2_retrieval()
    
    print(Fore.GREEN + "\nAnalyzing codebase structure...")
    with Halo(text='Analyzing codebase structure...', spinner='dots'):
        codebase_analysis = analyze_codebase_structure(root_folder)
    
    print(Fore.GREEN + "\nGetting suggestion from Claude...")
    claude_suggestion = get_claude_suggestion(description, technologies, codebase_analysis)
    
    print(Fore.GREEN + "\nClaude's suggestion for starting point:")
    print(Fore.GREEN + claude_suggestion)
    
    while True:
        file_to_analyze = input(Fore.YELLOW + "\nEnter the path of the file you want to analyze (or 'q' to quit): ")
        
        if file_to_analyze.lower() == 'q':
            break
        
        full_file_path = os.path.join(root_folder, file_to_analyze)
        
        if not os.path.isfile(full_file_path):
            print(Fore.RED + f"Error: The file '{full_file_path}' does not exist.")
            continue
        
        if os.path.basename(full_file_path).startswith('.'):
            print(Fore.RED + f"Error: '{full_file_path}' is a hidden file and will be skipped.")
            continue
        
        print(Fore.GREEN + f"\nAnalyzing file: {file_to_analyze}")
        file_content = get_file_content(full_file_path)
        analysis = analyze_file(file_to_analyze, file_content, description, technologies)
        
        print(Fore.GREEN + "\nFile Analysis:")
        print(Fore.GREEN + analysis)
        
        continue_analysis = input(Fore.YELLOW + "\nDo you want to analyze another file? (y/n): ")
        if continue_analysis.lower() != 'y':
            break
    
    print(Fore.GREEN + "\nCodebase Review Summary:")
    print(Fore.GREEN + f"Description: {description}")
    print(Fore.GREEN + f"Technologies: {technologies}")
    print(Fore.GREEN + f"Root folder: {root_folder}")
    print(Fore.GREEN + f"Total files: {codebase_analysis['file_count']}") 
    print(Fore.GREEN + f"Total lines of code: {codebase_analysis['total_lines']}")
    print(Fore.GREEN + "File types distribution:")
    for ext, count in sorted(codebase_analysis['file_types'].items(), key=lambda x: x[1], reverse=True):
        print(Fore.GREEN + f"  {ext or 'No extension'}: {count}")

def step_1_triggering():
    print(Fore.BLUE + "Step 1 Triggering: No triggering step for this workflow as it is executed manually on the command line.")

def step_2_retrieval():
    print(Fore.BLUE + "Step 2 Retrieval: Retrieving user input...")

    while True:
        description, technologies, root_folder = get_user_input()
        if validate_input(description, technologies, root_folder):
            return description, technologies, root_folder

def step_3_agentic(root_folder):
    print(Fore.BLUE + "Step 3 Agentic: Analyzing codebase structure...")
    codebase_analysis = analyze_codebase_structure(root_folder)
    return codebase_analysis

def step_4_action():
    print(Fore.BLUE + "Step 4 Action: Analyzing file...")

def step_5_learn():
    print(Fore.BLUE + "Step 5 Learn: No learning step in this workflow.")
    pass

def step_6_notify():
    print(Fore.BLUE + "Step 6 Notify: No notification step in this workflow.")
    pass

if __name__ == "__main__":
    run_sequential_agentic_flow()
