from langsmith import traceable
from langgraph.graph import END

from .state import AgentState

@traceable
def plan_revise_check(state:AgentState):
    approval = state.plan_reviewer.approval
    print(f"plan_revise_check approval: {approval}")
    if approval:
        return "execute"
    return "replan"

@traceable
def plan_execution_status(state:AgentState):
    all_tasks = state.executor.tasks
    for task_num, task in enumerate(all_tasks):
        if task.status == "pending":
            return "pending"
    return "done"

@traceable
def trivial_query_check(state:AgentState):
    if state.final_output:
        return END
    else:
        return [
                "plan_feasibility_checker_node",
                "plan_safty_critic_node"
            ]