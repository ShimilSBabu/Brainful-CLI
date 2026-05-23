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