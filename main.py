from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from src.state import AgentState
from src.nodes.planner import planner
from src.nodes.plan_feasibilty_checker import plan_feasibility_checker
from src.nodes.plan_safty_critic import plan_safty_critic
from src.nodes.plan_reviewer import plan_reviewer
from src.nodes.replanner import replanner
from src.nodes.executor import executor

def plan_revise_check(state:AgentState):
    approval = state.plan_reviewer.approval
    if approval:
        return "execute"
    return "replan"


def main():
    print("Hello from day-1-strip-to-core!")

    # user_query = input("Hi human, tell me your query: ")

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("planner_node", planner)
    graph_builder.add_node("plan_feasibility_checker_node", plan_feasibility_checker)
    graph_builder.add_node("plan_safty_critic_node", plan_safty_critic)
    graph_builder.add_node("plan_reviewer_node", plan_reviewer)
    graph_builder.add_node("executor_node", executor)
    graph_builder.add_node("replanner_node", replanner)

    graph_builder.add_edge(START, "planner_node")
    graph_builder.add_edge("planner_node", "plan_feasibility_checker_node")
    graph_builder.add_edge("planner_node", "plan_safty_critic_node")
    graph_builder.add_edge("plan_feasibility_checker_node", "plan_reviewer_node")
    graph_builder.add_edge("plan_safty_critic_node", "plan_reviewer_node")
    graph_builder.add_edge("plan_reviewer_node", "replanner_node")
    graph_builder.add_edge("plan_reviewer_node", "executor_node")
    graph_builder.add_edge("executor_node", END)

    graph_builder.add_conditional_edges(
        source="plan_reviewer_node",
        path=plan_revise_check,
        path_map={
            "replan": "replanner_node",
            "execute": "executor_node"
        }
    )

    graph = graph_builder.compile()
    state_input_user_query = {"user_query":"Give me all the files ending with '.py' in the 'nodes' folder of the 'src' folder of this directory."}
    # state_input_user_query = {"user_query":"Give me all the files starting with '.py' in the 'tools' folder of this directory."}
    state = AgentState(
        input=state_input_user_query
        )
    graph.invoke(state)

if __name__ == "__main__":
    main()
