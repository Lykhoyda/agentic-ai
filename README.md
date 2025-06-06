# Agentic AI Projects

This repository contains projects developed as part of [The Complete Agentic AI Engineering Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/) on Udemy.

## Projects

### 01_deep_research

A multi-agent system that performs deep research on a given query:
- Uses a research manager to coordinate the process
- Includes specialized agents for search, planning, writing, and email communication
- Generates comprehensive research reports and can send them via email
- **Framework**: LangChain + OpenAI

### 02_debate

A debate system built with crewAI:
- Creates a structured debate between multiple AI agents on specified topics
- Agents have different perspectives and roles in the debate
- Produces a comprehensive report with arguments and conclusions
- **Framework**: CrewAI

### 03_financial_researcher

A financial research assistant built with crewAI:
- Analyzes financial data and markets
- Provides insights on investments and financial trends
- Generates detailed financial reports
- **Framework**: CrewAI

### 04_stock_picker

A stock analysis and recommendation system:
- Researches and analyzes stocks
- Maintains memory of past analyses
- Generates investment recommendations and reports
- **Framework**: CrewAI

### 05_coder

An AI coding assistant:
- Helps with software development tasks
- Can generate code based on requirements
- Assists with debugging and code improvements
- **Framework**: CrewAI

### 06_engineering_team

A simulated engineering team of AI agents:
- Collaborates on software development projects
- Different agents take on different engineering roles
- Handles the full development lifecycle
- **Framework**: CrewAI

### 07_sidekick

An AI assistant with multiple capabilities that can help you complete tasks using various tools:

- **Web browsing** - can navigate websites and extract information
- **File management** - can create, read, and modify files
- **Python execution** - can write and run Python code
- **Push notifications** - can send notifications to keep you updated
- **Wikipedia access** - can search and retrieve information from Wikipedia
- **Web search** - can perform online searches for information
- **Framework**: LangChain + LangGraph

## Setup

Each project has its own dependency requirements. Generally, you'll need to:

1. Create a Python environment
2. Install the required dependencies
3. Set up the necessary API keys in `.env` files

For crewAI-based projects (02_debate, 03_financial_researcher, etc.), use:
```bash
pip install uv
crewai install
```

For other projects, install dependencies using pip or a package manager specified in the project directory.

## Running the Projects

Each project has its own run instructions. For example:

- **Sidekick**: Navigate to `07_sidekick` and run `python app.py`
- **CrewAI projects**: Run `crewai run` from the project directory

## Dependencies

The main dependencies for the projects include:

- LangChain & LangGraph: For creating AI agent workflows (01_deep_research, 07_sidekick)
- CrewAI: For multi-agent systems (02_debate, 03_financial_researcher, 04_stock_picker, 05_coder, 06_engineering_team)
- Gradio: For building user interfaces
- Playwright: For web browsing capabilities
- Various LLM APIs (OpenAI, Anthropic, etc.)

See the `pyproject.toml` file in each project directory for specific dependencies.

## Course Information

These projects are based on [The Complete Agentic AI Engineering Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/) on Udemy, which covers:

- Building autonomous AI agents
- Multi-agent systems
- Tool use and web browsing
- Agent memory and reasoning
- LangChain, LangGraph, and CrewAI frameworks
