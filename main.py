import os
import sys
import json
import requests
from typing import List, Dict, Any
from colorama import init, Fore, Style
from halo import Halo
from claude_analysis import analyze_codebase_with_anthropic_claude
from gemini_analysis import analyze_codebase_with_google_gemini

# Initialize colorama
init(autoreset=True)


def get_user_input():
    print(Fore.GREEN + "Welcome to the Interactive Codebase Review Agent!")
    print(Fore.GREEN + "Please provide the following information:")
    
    description = input(Fore.YELLOW + "1. Brief description of the codebase, including the type of application: ")
    root_folder = input(Fore.YELLOW + "2. Root folder of the project on your local file system: ")
    
    while True:
        model_choice = input(Fore.YELLOW + "3. Choose the model to use (gemini/claude) [default: claude]: ").lower()
        if model_choice == '':
            model_choice = 'claude'
        if model_choice in ['gemini', 'claude']:
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 'gemini' or 'claude', or press Enter for the default (claude).")
    
    return description, root_folder, model_choice

def validate_input(description: str, root_folder: str) -> bool:
    if not description or not root_folder:
        print(Fore.RED + "Error: All fields are required.")
        return False
    
    if not os.path.isdir(root_folder):
        print(Fore.RED + f"Error: The specified root folder '{root_folder}' does not exist.")
        return False
    
    return True

def analyze_codebase_structure(root_folder: str, description: str) -> Dict[str, Any]:
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

    codebase_analysis = {
        "file_count": file_count,
        "total_lines": total_lines,
        "file_types": file_types,
        "file_list": file_list
    }

    # Analyze codebase with Google Gemini
    gemini_analysis = analyze_codebase_with_google_gemini(description, codebase_analysis)
    codebase_analysis["gemini_analysis"] = gemini_analysis

    return codebase_analysis


def run_sequential_agentic_flow():
    print(Fore.BLUE + "Running sequential agentic flow...")

    step_1_triggering()
    description, root_folder, model_choice = step_2_retrieval()
    step_3_agentic(description, root_folder, model_choice)
    step_4_action()
    step_5_learn()
    step_6_notify()

def step_1_triggering():
    print(Fore.BLUE + "Step 1 Triggering: No triggering step for this workflow as it is executed manually on the command line.")

def step_2_retrieval():
    print(Fore.BLUE + "Step 2 Retrieval: Retrieving user input...")

    while True:
        description, root_folder, model_choice = get_user_input()
        if validate_input(description, root_folder):
            return description, root_folder, model_choice

def step_3_agentic(description, root_folder, model_choice):
    print(Fore.BLUE + "Step 3 Agentic: Analyzing codebase structure...")

    # Analyze codebase structure
    with Halo(text='Analyzing codebase structure...', spinner='dots'):
        codebase_analysis = analyze_codebase_structure(root_folder, description)

    print(Fore.GREEN + "\nCodebase Review Summary:")
    print(Fore.GREEN + f"Description: {description}")
    print(Fore.GREEN + f"Root folder: {root_folder}")
    print(Fore.GREEN + f"Total files: {codebase_analysis['file_count']}") 
    print(Fore.GREEN + f"Total lines of code: {codebase_analysis['total_lines']}")
    print(Fore.GREEN + "File types distribution:")

    for ext, count in sorted(codebase_analysis['file_types'].items(), key=lambda x: x[1], reverse=True):
        print(Fore.GREEN + f"  {ext or 'No extension'}: {count}")

    if model_choice == 'claude':
        print(Fore.GREEN + "\nClaude 3.5 Sonnet Analysis:")
        with Halo(text='Analyzing with Claude...', spinner='dots'):
            analysis = analyze_codebase_with_anthropic_claude(description, codebase_analysis)
    else:
        print(Fore.GREEN + "\nGoogle Gemini Analysis:")
        with Halo(text='Analyzing with Gemini...', spinner='dots'):
            analysis = analyze_codebase_with_google_gemini(description, codebase_analysis)

    print(Fore.GREEN + analysis)

def step_4_action():
    print(Fore.BLUE + "Step 4 Action: TBD")

def step_5_learn():
    print(Fore.BLUE + "Step 5 Learn: No learning step in this workflow.")
    pass

def step_6_notify():
    print(Fore.BLUE + "Step 6 Notify: No notification step in this workflow.")
    pass

if __name__ == "__main__":
    run_sequential_agentic_flow()
