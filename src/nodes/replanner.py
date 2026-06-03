from ..state import AgentState
from ..model import call_llm
from ..helper_functions import read_tool_registry
import json

def replanner(state:AgentState):
    print("Inside RePlanner..")
    user_query = state.input.user_query
    tool_hints = read_tool_registry()

    planner_system_prompt = f"""
    You are a Replanning agent in a plan-execute system for a smart CLI assistant.
    You are called as there was some issue with the primary plan. Your primary objective is to replan and decompose the goal into an ordered list of discrete, executable tasks, while solving the current cause of issues.

    You will receive:

    1. Original user goal
    2. Previous plan
    3. Current execution state
    4. Completed tasks and their results
    5. Current issue due to which the previous plan was stopped/paused.

    ## Output format
    Return ONLY a single valid JSON object — no prose, no markdown fences, no JSON fences, no explanation.
    
    If the goal is clear, return:
    {{
    "plan": {{
        "goal_summary": "<one-sentence restatement>",
        "estimated_steps": <integer>,
        "tasks": [
        {{
            "id": "t1",
            "description": "<specific, actionable description>",
            "tool_hint": [{{
                "name"= "shell_tool",
                "parameters"={{"command"=<command>, 
                    "arguments"=<arguments>}}
                }}],
            
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

    steps_executed = [task for task in state.planner.tasks if task.status == "done"]
    steps_pending = [task for task in state.planner.tasks if task.status == "pending"]
    current_step = [task for task in state.planner.tasks if task.status == "running"]
    steps_failed = [task for task in state.planner.tasks if task.status == "failed"]

    plan_review = f"""
    # Plan Feasibility Checker Output
    {state.plan_feasibility_checker}

    # Plan Safty Critic Output
    {state.plan_safty_critic}

    # Steps Executed
    {steps_executed}

    # Steps Pending
    {steps_pending}

    # Current Step
    {current_step}

    # Failed Steps
    {steps_failed}
    """

    messages = [
        {
            "role":"system",
            "content":planner_system_prompt
        },
        {
            "role":"human",
            "content":user_query
        },
        {
            "role":"ai",
            "content":str(state.planner)
        },
        {
            "role":"developer",
            "content":plan_review
        }
    ]
    response = call_llm(messages)
    # print(f"response: {response}")

    if response["status"]:
        response_content = response["content"]
        # print(f"response_content({type(response_content)})\n{response_content}")
        json_start = response_content.find("{")
        json_end = response_content.rfind("}") + 1
        response_content_trimmed = response_content[json_start:json_end]
        # print(f"response_content({type(response_content_trimmed)})\n{response_content_trimmed}")
        state.planner = json.loads(response_content_trimmed)["plan"]
    else:
        print(f"Response Status: {response["status"]}")
    
    return state