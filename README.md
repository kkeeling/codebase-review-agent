# Interactive Codebase Review Agent

This project is an Interactive Codebase Review Agent that analyzes and provides insights into your codebase using AI-powered tools.

## Features

- Analyzes the structure of your codebase
- Provides statistics on file count, total lines of code, and file type distribution
- Uses Google's Gemini AI to perform a comprehensive analysis of your codebase
- Offers insights on code organization, potential improvements, security concerns, and maintainability

## Requirements

- Python 3.6+
- Anthropic API key (for Claude AI, not currently used but required)
- Google API key (for Gemini AI)

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   ```
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   export GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

Run the main script:

```
python main.py
```

Follow the prompts to enter:
1. A brief description of your codebase
2. The root folder of your project on your local file system

The agent will then analyze your codebase and provide a detailed report.

## Output

The agent will provide:
- A summary of your codebase structure
- File count and total lines of code
- Distribution of file types
- A comprehensive analysis from Google's Gemini AI, including:
  - Overall structure and organization
  - Potential improvements and best practices
  - Security concerns and performance issues
  - Suggestions for better code maintainability and scalability

## Note

This project is currently a work in progress. Some features like the action step (Step 4) are yet to be implemented.

## License

[MIT License](LICENSE)
