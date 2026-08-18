# Smart CLI Agent
[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2.x-4B8BBE)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.61%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

> An AI-powered agent system that understands natural language queries, decomposes them into executable tasks, validates them for feasibility and safety, and executes them with full observability.

## What It Does

Smart CLI Agent is an intelligent assistant framework that bridges the gap between user intent and system execution. It takes natural language commands, validates them against safety and feasibility criteria, and executes them in a structured, observable manner.

### Key Capabilities

- **Intelligent Task Planning**: Decompose complex user queries into ordered, executable subtasks
- **Multi-Stage Validation**: Evaluate plans through feasibility, safety, and review stages before execution
- **Safe Execution**: Built-in safety checks and constraints (dry runs, human checkpoints, scope restrictions, rate limiting)
- **Tool Integration**: Execute shell commands, read/write/modify documents, and return structured outputs
- **Stateful Workflows**: Support for long-running queries with resumption via thread IDs
- **Web Interface**: Interactive Streamlit UI for easy interaction
- **RESTful API**: FastAPI backend for programmatic access

## Why Use This

- **Reduce Manual Steps**: Let the agent handle task decomposition and coordination
- **Safety First**: Automatic feasibility and safety validation before execution
- **Transparency**: Full observability of plan, validation results, and execution steps
- **Extensible**: Easy to add new tools, nodes, and validation rules
- **Production Ready**: Built on proven frameworks (LangGraph, FastAPI, Streamlit)

## Getting Started

### Prerequisites

- Python 3.12 or higher
- UV package manager ([install UV](https://docs.astral.sh/uv/getting-started/installation/))
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd day_1_strip_to_core
   ```

2. **Set up the Python environment**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your configuration:
   ```env
   # LLM Configuration
   MISTRAL_API_KEY=your_mistral_api_key_here
   
   # FastAPI Configuration
   FASTAPI_HOST=127.0.0.1
   FASTAPI_PORT=8080
   
   # Streamlit Configuration
   STREAMLIT_PORT=8501
   ```

### Usage

#### Option 1: Web UI (Recommended for Beginners)

```bash
# Terminal 1: Start the FastAPI backend
uv run uvicorn main:app --host 127.0.0.1 --port 8080

# Terminal 2: Start the Streamlit frontend
uv run streamlit run src/views/streamlit_ui.py
```

Then open your browser to `http://localhost:8501` and:
1. Enter a User ID
2. Enter your query (e.g., "List all python files in this directory")
3. Click "Click Me" to execute

#### Option 2: API Endpoint (Programmatic)

```bash
# Start the backend server
uv run uvicorn main:app --host 127.0.0.1 --port 8080
```

Then make requests:
```bash
curl "http://127.0.0.1:8080/run_cli_agent?state_input_user_query=list%20files&thread_id=user_123"
```

#### Query Types

The agent handles two types of queries:

1. **Trivial Tasks**: General knowledge questions
   - Example: "What is the capital of France?"
   - Response: Direct answer from the LLM

2. **Non-Trivial Tasks**: System operations
   - Example: "Find all Python files and show their line count"
   - Response: Multi-step plan → validation → execution

### Project Structure

```
src/
├── state.py                    # Agent state definitions (Pydantic models)
├── model.py                    # LLM interface
├── helper_functions.py         # Utility functions
├── conditional_edges.py        # Graph routing logic
├── nodes/
│   ├── planner.py             # Task decomposition
│   ├── plan_feasibilty_checker.py  # Feasibility validation
│   ├── plan_safty_critic.py   # Safety validation
│   ├── plan_reviewer.py       # Quality review
│   ├── executor.py            # Task execution
│   └── replanner.py           # Plan adjustment
├── tools/
│   ├── shell_tool.py          # Execute shell commands
│   ├── read_document_tool.py  # Read file contents
│   ├── write_document_tool.py # Create/write files
│   ├── modify_document_tool.py # Edit file contents
│   ├── return_final_output_tool.py # Return results
│   └── tool_registry.md       # Tool specifications
└── views/
    └── streamlit_ui.py        # Web interface
```

## Architecture

The agent workflow follows a LangGraph-based state machine:

```
START
  ↓
PLANNER (Decompose query into tasks)
  ├→ Trivial Query? → FINAL OUTPUT
  ↓
PLAN FEASIBILITY CHECKER (Validate technical viability)
  ↓
PLAN SAFETY CRITIC (Evaluate safety constraints)
  ↓
PLAN REVIEWER (Quality assurance)
  ├→ Needs Revision? → REPLANNER
  ↓
EXECUTOR (Execute validated plan)
  ↓
FINAL OUTPUT
```

### Core Components

- **State Management**: Structured state objects track plan, validation results, and execution progress
- **Feasibility Validation**: 8-dimensional scoring (goal alignment, sequencing, resource feasibility, etc.)
- **Safety Validation**: 8-dimensional assessment (irreversibility, data sensitivity, authorization, etc.)
- **Conditional Routing**: Intelligent branching based on feasibility/safety verdicts
- **Thread Support**: Enable query resumption and long-running operations

## Examples

### Example 1: Simple Shell Command
```
User: "Create a new file called test.txt with hello world"
→ Agent: Creates the file using shell_tool
→ Result: File created successfully
```

### Example 2: Complex Task with Validation
```
User: "Delete all log files in the /var/log directory"
→ Planner: Breaks into: find logs → review → delete
→ Safety Critic: Warns about irreversibility → suggests dry-run first
→ Reviewer: Approves with constraints (dry-run checkpoint required)
→ Executor: Runs with safety constraints applied
```

## Development

### Add a New Tool

1. Create a new tool file in `src/tools/`
2. Register it in the tool registry
3. Reference it in task `tool_hint` fields

### Customize Validation Rules

Edit the nodes in `src/nodes/`:
- Modify dimension scoring logic in `plan_feasibilty_checker.py`
- Add safety constraints in `plan_safty_critic.py`

### Extend the Workflow

Modify `main.py` to add new nodes or change conditional routing logic.

## Support & Help

- **Issues**: Check existing [issues](../../issues) or create a new one
- **Discussions**: Use [discussions](../../discussions) for questions and ideas
- **Documentation**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design docs
- **Contributing**: Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) file for details.

## Author

**SHIMIL S BABU**
- GitHub: [@shimil-babu](https://github.com/shimil-babu)

---