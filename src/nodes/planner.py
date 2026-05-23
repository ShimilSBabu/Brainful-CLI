from state import AgentState
from model import call_llm
from tools.tool_registry_reader import get_tools_info

def planner(state:AgentState):
    user_query = state['input']['user_query']
    tool_hints = get_tools_info()

    planner_system_prompt = f"""
    You are a planning agent in a plan-execute system for a smart CLI assistant. Your only job is to decompose a goal into an ordered list of discrete, executable tasks.
    
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

    messages = [
        {
            "role":"system",
            "content":planner_system_prompt
        },
        {
            "role":"human",
            "content":user_query
        }
    ]
    response = call_llm(messages)

    if response["status"]:
        response_content = response["content"]
        state.PlannerState = response_content
    else:
        print("Response Status:")
    
    return state