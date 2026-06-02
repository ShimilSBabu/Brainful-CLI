from ..state import AgentState

def plan_reviewer(state:AgentState):
    plan_feasibility_confidence_score = state.plan_feasibility_checker.confidence
    plan_safty_confidence_score = state.plan_safty_critic.confidence
    # state.plan_reviewer.plan_review = plan_feasibility_confidence_score
    # state.plan_reviewer.confidence.PlanSaftyCriticStateConfidence = plan_safty_confidence_score

    # next_node_list = []
    # if plan_feasibility_confidence_score <= 0.5:
    #     next_node_list.append("plan_feasibility_checker")
    # if plan_safty_confidence_score <= 0.5:
    #     next_node_list.append("plan_safty_critic")
    # if next_node_list:
    #     return next_node_list
    # return "executor"

    if plan_feasibility_confidence_score <= 0.5 or plan_safty_confidence_score <= 0.5:
        return {
            "plan_reviewer":{
                "approval": False
                }
            }
    return {
            "plan_reviewer":{
                "approval": True
                }
            }