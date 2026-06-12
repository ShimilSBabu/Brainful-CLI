from importlib import import_module
from dotenv import load_dotenv
import json

from ..state import AgentState
from ..model import get_react_agent
from ..helper_functions import fetch_structuredtools


def executor(state:AgentState):
    print("Inside Executor..")
    current_task = False
    current_task_num = False
    all_tasks = state.executor.tasks
    for task_num, task in enumerate(all_tasks):
        if task.status == "pending":
            current_task = task
            current_task_num = task_num
            break
    
    if not current_task:
        return state
    
    tool_name = task.tool_hint[0].name
    tool_parameters = task.tool_hint[0].parameters

    try:
        # module = import_module(f"..src.tools.{tool_name}", package=__package__)
        module = import_module(f"..tools.{tool_name}", package=__package__)
        result = module.run(**tool_parameters)
    except Exception as e:
        print(f"Direct tool execution interrupted due to the error below:\n{str(e)}\nSwitching to the ReAct Agent approach.")
        system_prompt="""You are a ReAct agent inside the executor node of a plan-execute agentic system.
        You will be given exactly one substep of a large plan. Execute the step given by the planner. 
        Tool hint will be provided by the planner. 
        If there is something wrong while tool call, correct it; especially tool argument architecture.
        """
        human_prompt = str(current_task)
        load_dotenv()
        # print(f"current_task:\n{current_task}")

        tools = fetch_structuredtools()
        result = get_react_agent(system_message=system_prompt, human_message=human_prompt, tools=tools)
        # print(f"result\n{result["messages"]}")
        print(f"result\n{result["messages"][-2].content}")
        result = json.loads(result["messages"][-2].content)
        # print(f"result\n{result}")
    if result["content"]:
        result_content = result["content"]
        all_tasks[current_task_num].result = result_content
        all_tasks[current_task_num].status = "done"
    else:
        result_error = result["error"] + str(result["metadata"])
        all_tasks[current_task_num].error = result_error
        all_tasks[current_task_num].status = "failed"
    all_tasks[current_task_num].retry_count += 1

    if tool_name == "return_final_output_tool":
        # return{
        #     "executor":{
        #         "tasks":all_tasks
        #     },
        #     "final_output":result_content
        # }
        state.final_output = result_content

    # print(f"all_tasks\n{all_tasks}\n")
    # return{
    #     "executor":{
    #         "tasks":all_tasks
    #     }
    # }
    state.executor.tasks = all_tasks
    return state