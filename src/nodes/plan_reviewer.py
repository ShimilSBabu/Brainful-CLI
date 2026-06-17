from langgraph.types import interrupt

from ..state import AgentState

def plan_reviewer(state:AgentState):
    print("Inside plan_reviewer..")
    plan_feasibility_confidence_score = state.plan_feasibility_checker.confidence
    plan_safty_confidence_score = state.plan_safty_critic.confidence
    # print(f"plan_reviewer state: {state}")
    print(f"plan_feasibility_confidence_score: {plan_feasibility_confidence_score}\nplan_safty_confidence_score: {plan_safty_confidence_score}")
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
    if state.plan_reviewer.review_count >= 1:
        if (plan_feasibility_confidence_score <= 0.5) and (plan_safty_confidence_score <= 0.5):
            message = f"The plan feasibility confidence score is {plan_feasibility_confidence_score} (<0.5) and the plan safty confidence score is {plan_safty_confidence_score} (<0.5)."
        elif plan_feasibility_confidence_score <= 0.5:
            message = f"The plan feasibility confidence score is {plan_feasibility_confidence_score} (<0.5)."
        elif plan_safty_confidence_score <= 0.5:
            message = f"The plan safty confidence score is {plan_safty_confidence_score} (<0.5)."
        answer = interrupt(
            {
                "approval": f"{message} Approve this plan?\n{state.planner}"
            }
        )

        if answer.lower() == "approve":
            approval = False
        else:
            approval = True

        return {
        "plan_reviewer":{
            "approval": approval
            }
        }
    
    if plan_feasibility_confidence_score <= 0.5 or plan_safty_confidence_score <= 0.5:
        approval = False
    else:
        approval = True
    state.plan_reviewer.review_count += 1

    return {
        "plan_reviewer":{
            "approval": approval
            }
        }