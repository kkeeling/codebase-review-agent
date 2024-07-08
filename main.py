import os
import sys
import json
import requests
from typing import List, Dict, Any
from colorama import init, Fore, Style

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
    
    # description = input(Fore.YELLOW + "1. Brief description of the codebase, including the type of application: ")
    # technologies = input(Fore.YELLOW + "2. Main technologies used (comma-separated): ")
    description = "foo"
    technologies = "bar"
    
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
    file_structure = {}

    # If root folder contains a .gitignore file, idenfity those files and directories
    if os.path.exists(os.path.join(root_folder, '.gitignore')):
        with open(os.path.join(root_folder, '.gitignore'), 'r') as f:
            gitignore_lines = f.readlines()

    # List the files that will be ignored from .gitignore
    print(Fore.GREEN + "Files and directories will be ignored:")
    for line in gitignore_lines:
        print(Fore.GREEN + f"  {line.strip()}")

    # Idenfity hidden folders and files (those that start with ".")
    hidden_files = [file for file in os.listdir(root_folder) if file.startswith('.')]
    print(Fore.GREEN + "Hidden files and directories (also ignored):")
    for file in hidden_files:
        print(Fore.GREEN + f"  {file}")

    for root, dirs, files in os.walk(root_folder):
        # Remove hidden directories from the dirs list
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        current_dir = file_structure
        path_parts = os.path.relpath(root, root_folder).split(os.sep)
        for part in path_parts:
            if part not in current_dir:
                current_dir[part] = {"files": [], "dirs": {}}
            current_dir = current_dir[part]["dirs"]

        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
            
            file_path = os.path.join(root, file)
            file_count += 1
            
            _, extension = os.path.splitext(file)
            file_types[extension] = file_types.get(extension, 0) + 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_lines += content.count('\n') + 1
                current_dir["files"].append(file)
            except Exception as e:
                print(Fore.RED + f"Warning: Could not read file {file_path}. Error: {str(e)}")

    return {
        "file_count": file_count,
        "total_lines": total_lines,
        "file_types": file_types,
        "file_structure": file_structure
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
{json.dumps(codebase_analysis['file_structure'], indent=2)}

Please suggest a specific file or directory that would be a good starting point for analyzing this codebase, and explain why you think it's a good choice.
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

    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["content"][0]["text"]

def get_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

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

    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["content"][0]["text"]

def main():
    description, technologies, root_folder = get_user_input()
    
    if not validate_input(description, technologies, root_folder):
        sys.exit(1)
    
    print(Fore.GREEN + "\nAnalyzing codebase structure...")
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

if __name__ == "__main__":
    main()