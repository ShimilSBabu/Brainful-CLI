## Day 1
1. Install and setup Git and UV.
2. Decide the base outline of the architecture of the application.
3. Create the folder structure for the decided architecture.
4. Create and store the necessary environmental variables in the .env file.

## Day 2
1. Make the function to call the model that will be used throughout the application development.
2. Test the model.

## Day 3
Define the architecture of the state with respect to the application's purpose.

## Day 4
Define the planner node.
- A planner has one job: take a goal and produce an ordered task list that an executor can work through without needing to think. The better the plan, the less the executor needs to improvise as improvisation is where agentic systems usually go wrong.

### The Planner Prompt Structure
The system prompt is doing most of the work. It needs four things:
1. Role + output contract — tell the model what it is and exactly what format it must return. Structured output (JSON) is non-negotiable for the executor to consume reliably.
2. Planning strategy — explicit instructions on how to decompose. Don't leave this implicit. Tell it to break on tool boundaries, to order by dependency, to flag unknowns.
3. Task schema — define what a task looks like. Each task should carry: an id, a description, a tool or agent hint, depends_on (ids), and an expected_output description. That last field is underrated — it forces the planner to be concrete about what "done" means.
4. Failure modes to avoid / Guardrails — explicitly tell it not to make tasks too granular (one LLM call per task is often the right granularity, not one line of code), not to plan beyond its knowledge horizon, and to flag ambiguity rather than assume

### Task Structure
    class Task(BaseModel):
        id: str = Field(..., description="Unique identifier, e.g. 't1'")
        description: str = Field(..., min_length=10)
        tool_hint: ToolHint = ToolHint.OTHER
        depends_on: list[str] = Field(default_factory=list)
        expected_output: str = Field(..., min_length=5)
        status: TaskStatus = TaskStatus.PENDING
        result: Any = None
        error: str | None = None

### Plan Structure
    class Plan(BaseModel):
        tasks: list[Task] = Field(..., min_length=1)
        goal_summary: str = Field(..., description="One-sentence restatement of the goal")
        estimated_steps: int = Field(..., ge=1)
### System Prompt Template 

    SYSTEM_PROMPT_TEMPLATE = """
    You are a planning agent in a plan-execute system. Your only job is to decompose a goal into an ordered list of discrete, executable tasks.
    
    ## Output format
    Return ONLY a single valid JSON object — no prose, no markdown fences, no explanation.
    
    If the goal is clear, return:
    {{
    "plan": {{
        "goal_summary": "<one-sentence restatement>",
        "estimated_steps": <integer>,
        "tasks": [
        {{
            "id": "t1",
            "description": "<specific, actionable description>",
            "tool_hint": "<{tool_hints}>",
            "depends_on": [],
            "expected_output": "<concrete description of what 'done' looks like>"
        }}
        ]
    }}
    }}
    
    If the goal is ambiguous or missing required context, return:
    {{
    "clarification": "<single, specific question>"
    }}
    
    ## Planning rules
    1. Break at tool boundaries — each task uses exactly one tool or capability.
    2. Order by dependency. Earlier tasks must produce outputs consumed by later tasks.
    3. Each task must be self-contained: its description must be unambiguous to an executor that has not read the goal.
    4. The `expected_output` field is mandatory and must be concrete — not "the result" but "a JSON array of {{'url': ..., 'title': ...}} with 5 entries".
    5. Consolidate sequential same-tool steps with no decision between them.
    6. Available tools: {tool_hints}.
    7. Do not plan steps that require information you do not have — include a discovery task first, or ask for clarification.
    8. Never combine planning with execution. Return the plan only.
    """

## Day 5
Define the Tools

1. Create the necessary tools.
2. Create a markdown (.md) file which contains all the necessary metadata regarding all the tools. This .md file will be used by the planner for getting the details about the tools.
3. Create a tool_registry_reader python file with a get_tools_info function which can provide the contents of the .md file when called.

### Python Imports Across Subdirectories

#### Setup
For a structure like:
```
dir1/
    __init__.py
    dir1.1/
        __init__.py
        fileA.py
    fileB.py
```
To use `func` from `fileB.py` inside `fileA.py`:

### Option 1: Relative import (clean, recommended)
```python
# in fileA.py
from ..fileB import func
```
Requires `__init__.py` in each directory, and must be run as a module — not directly.

### Option 2: Run as a module (fixes relative import errors)
```bash
python -m dir1.dir1_1.fileA
```
Running with `-m` from the project root tells Python the package context, making relative imports work.

### Option 3: sys.path hack (when running file directly)
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fileB import func
```
Manually adds the parent directory to Python's search path. No `__init__.py` needed.

### Option 4: Root-level entry point (for proper apps)
Create a `main.py` at the project root and run everything from there.

---

### Common Error: `ImportError: attempted relative import with no known parent package`
**Cause:** Running `fileA.py` directly (e.g. `python fileA.py`) — Python doesn't know it's part of a package.  
**Fix:** Use `python -m dir1.dir1_1.fileA` instead, or use the `sys.path` hack.

---

### What is `__init__.py`?
- Marks a directory as a Python **package**, enabling imports from it.
- Can be completely empty — its presence is what matters.
- Without it, Python (3.3+) treats the directory as a **namespace package** (implicit), but relative imports still won't work without it.

---

### Dot notation in relative imports
| Syntax | Meaning |
|---|---|
| `from .module import x` | Same directory |
| `from ..module import x` | One level up |
| `from ...module import x` | Two levels up |

---

### Absolute vs Relative imports

**Absolute** — full path from project root (preferred for clarity):
```python
from dir1.fileB import func
```

**Relative** — relative to current file's location:
```python
from ..fileB import func   # go one level up, then import fileB
```

Absolute imports work anywhere; relative imports only work inside packages.

---

### Importing the whole module vs a specific function
```python
import dir1.fileB                # import whole module
dir1.fileB.func()                # call with full path

from dir1.fileB import func      # import just the function
func()                           # call directly

from dir1.fileB import func as f # alias to avoid name conflicts
f()
```

---

### Quick decision guide
| Situation | Best approach |
|---|---|
| Proper project with packages | Absolute import + `__init__.py` |
| Inside a package, sibling/parent file | Relative import (`..`) |
| Running a file directly | `sys.path` hack |
| Large app with a clear entry point | `main.py` at root + `python -m` |


## Day 6
Define plan reviewers.

1. Define plan feasibility checker.
2. Define plan safty critic.

### Plan Feasibility Checker
1. Checks whether the plan is feasible.
2. Checks whether the plan is able to satisfy the user query.
3. Checks whether the plan is minimal.

### Plan Safty Critic
1. Checks whether the plan in itself can become harmful to the user/system.
2. Checks whether any step within the plan can become harmful to the user/system.

### Plan Reviewer
Checks the results of Plan Feasibility Checker & Plan Safty Critic and decides whether to;

1. Execute the plan
2. Pass the current plan and the issues from review to replanner for planning again.


## Day 7
Define the RePlanner node
The RePlanner is the one which is called when there are issues with the current plan and the reviewer decided that the current plan must be changed/modified for the safe fullfilment of the user's query.
### The RePlanner takes as input;
1. User query
2. The current plan
3. Reviews from Plan Feasibility Checker & Plan Safty Critic
4. Human opinions/suggestions if any.


## Day 8
Define the Executor node
The Executor is the one which takes the steps prepared by the planner and then executes them one by one (or parallel if programmed to).
If the direct tool call fails, it should be redirected to a ReAct agent which can handle tool executions.

* There may be tasks which depends on previous tasks. For those, the results of the previous tasks must be fetched.
* Tool results could be stored in the state or in a persistant memory.
* A function or tool which takes the dependancies (task id) as input and gets the result of the dependancies (previous task) is necessary.

### Concerns while building execution node
1. Must validate whether the tool arguments are having the correct format or not.
2. Must verify whether the tool execution went correctly or not.
3. Must asserten whether the tool results are having the right format or not.

### Executor friendly tool returns
Gave a unified structure for tool returns.
```python
return {
        "status":status,
        "content":content,
        "error":str(error),
        "metadata":{
            "metadata_1":metadata_1,
            "metadata_2":metadata_2,
            "metadata_3":metadata_3
            }
        }
```

This structure will be helpful for automated executors.

### Added a get_react_agent function which can handle tool calls incase normal direct tool call fails.
* For this react agent, the tool information must be given as 'structuredtools' format.
```python
from langchain_core.tools import StructuredTool
tool = StructuredTool.from_function(
                func=function_name,
                name=module_name,
                description=function_description
            )
```
* But in our case, as the tools are not considered hard coded and are taking an automated approach, we'll use 
module=import_module(f"src.tools.{module_name}", package=_\_package__)
    * package=_\_package__ tells Python where the relative import should start from.
    * In Python, \_\_package__ is a special attribute automatically set by the import system to indicate the package context of a module.It’s mainly used to help Python resolve relative imports correctly. It tells Python the package name that the current module belongs to.

So,
```python
tools = []
file_path = os.path.join(os.getcwd(),"src", "tools")
for file in os.listdir(path=file_path):
    if file.endswith(".py"):
        module_name=file.split(".py")[0]
        module=import_module(f"src.tools.{module_name}", package=__package__)
        tool = StructuredTool.from_function(
            func=module.run,
            name=module.__name__, # name=module_name in our case
            description=module.run.__doc__
        )
        tools.append(tool)
```


## Day 9
Create a conditional edge which ends the workflow if the plan is completed. Otherwise, the executor must be called again until all the tasks are completed.

Move the conditional edges to a single seperate file inside src. 


## Day 10
Add observability via LangSmith.

1. Create an account in LangSmith (https://smith.langchain.com/).
2. Create an 'Application' in LangSmith
3. Copy the api-key from there.
4. Inside the .env file, add these environmental variables.

    * LANGSMITH_TRACING=true
    * LANGSMITH_ENDPOINT=https://api.smith.langchain.com
    * LANGSMITH_API_KEY=\<the api-key copied earlier>
    * LANGSMITH_PROJECT=\<name of the application>


For tracing the custom tools or functions,
```python
    from langsmith import traceable

    @traceable
    def my_function():
        ...
```