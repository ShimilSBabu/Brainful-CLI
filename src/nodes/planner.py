import os

from ..state import AgentState
from ..model import call_llm
from ..helper_functions import read_tool_registry
import json

def planner(state:AgentState):
    print("Inside Planner..")
    os_dict = {
        'nt':"windows"
    }
    user_query = state.input.user_query
    tool_hints = read_tool_registry()
    os_name = os_dict[os.name]

    planner_system_prompt = f"""
You have 2 modes;
1. Non-trivial task mode: The user's query requires to do/perform in this computer or is something related to this computer.
2. Trivial task mode: The user is asking for some general knowledge.

If the user's query if a trivial task:
    Directly reply to the user in the format {{"final_output":{{your reply in markdown format}}}}. Do not add anything extra. No greetings are required.

Else:
    You are a planning agent in a plan-execute system for a smart CLI assistant. Your only job is to decompose a goal into an ordered list of discrete, executable tasks.
    
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
    9. For tasks with return_final_output_tool tool, the task must have 'depends_on' to other tasks in its tool_hint.

    EXTRA INFORMATION
    The current system is having the operating system: {os_name}

    ## Important
    - return_final_output_tool tool is the only tool which can display the final output to the user.
    - Always call return_final_output_tool tool for giving the final output to the user.
    - Specify the task name in the 'depends_on' for fetching the results of previous tasks.
    - To include output of another task (eg:- t5) in the 'content' of task containing tool return_final_output_tool, incude exactly [output of {{task_id}}] (eg:- [output of t5]).
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
    # print(f"response: {response}")

    if response["status"]:
        response_content = response["content"]
        # print(f"response_content({type(response_content)})\n{response_content}")
        json_start = response_content.find("{")
        json_end = response_content.rfind("}") + 1
        response_content_trimmed = response_content[json_start:json_end]
        # print(f"response_content({type(response_content_trimmed)})\n{response_content_trimmed}")
        response_loaded = json.loads(response_content_trimmed)
        if "final_output" in response_loaded:
            print("This is a trivial task. Choosing Fast track")
            return response_loaded
        print("This is a non-trivial task. Choosing Plan-Elaborate")
        
        plan = response_loaded["plan"]
        
        tasks_list= plan["tasks"]
        return {
            "planner":plan,
            "executor":{
                "tasks":tasks_list
            }
        }
    else:
        print(f"Response Status: {response["status"]}")
    
    return state.model_dump()