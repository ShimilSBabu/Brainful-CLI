from .state import AgentState
from langsmith import traceable

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