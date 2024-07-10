# Interactive Codebase Review Agent

This project is an Interactive Codebase Review Agent that leverages AI-powered tools to analyze and provide comprehensive insights into your codebase. It uses both Anthropic's Claude and Google's Gemini AI models to offer a detailed review of your project's structure, potential improvements, and overall quality.

## Features

- Analyzes the structure and organization of your codebase
- Provides detailed statistics including file count, total lines of code, and file type distribution
- Utilizes Anthropic's Claude AI for in-depth code analysis (optional)
- Leverages Google's Gemini AI for comprehensive codebase review
- Offers insights on code organization, potential improvements, security concerns, and maintainability
- Follows a sequential agentic flow for a thorough review process

## Requirements

- Python 3.6+
- Anthropic API key (for Claude AI)
- Google API key (for Gemini AI)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/interactive-codebase-review-agent.git
   cd interactive-codebase-review-agent
   ```

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

1. Run the main script:
   ```
   python main.py
   ```

2. Follow the prompts to enter:
   - A brief description of your codebase
   - The root folder of your project on your local file system
   - Choose the AI model for analysis (Claude or Gemini)

3. The agent will then proceed through the following steps:
   - Step 1: Triggering - Initiates the analysis process
   - Step 2: Retrieval - Gathers information about your codebase
   - Step 3: Agentic - Performs AI-powered analysis using the chosen model
   - Step 4: Action - (To be implemented) Will suggest or perform actions based on the analysis
   - Step 5: Learn - Processes the analysis results
   - Step 6: Notify - Provides the final report and insights

## Output

The agent will provide a comprehensive report including:
- A summary of your codebase structure
- File count and total lines of code
- Distribution of file types
- A detailed analysis from the chosen AI model, covering:
  - Overall structure and organization
  - Potential improvements and best practices
  - Security concerns and performance issues
  - Suggestions for better code maintainability and scalability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Note

This project is actively under development. Some features, like the action step (Step 4), are yet to be fully implemented.

## License

This project is licensed under the [MIT License](LICENSE).
