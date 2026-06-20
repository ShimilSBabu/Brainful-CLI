from langgraph.graph import StateGraph, START, END
from fastapi import FastAPI
from langgraph.types import Command

from src.state import AgentState
from src.nodes.planner import planner
from src.nodes.plan_feasibilty_checker import plan_feasibility_checker
from src.nodes.plan_safty_critic import plan_safty_critic
from src.nodes.plan_reviewer import plan_reviewer
from src.nodes.replanner import replanner
from src.nodes.executor import executor
from src.conditional_edges import plan_revise_check, plan_execution_status, trivial_query_check
from langgraph.checkpoint.sqlite import SqliteSaver

app = FastAPI()

@app.get("/run_cli_agent")
def main(state_input_user_query:str="", thread_id:str="", resume_command:str=""):
    print("Hello from day-1-strip-to-core!")

    config = {
    "configurable": {
        "thread_id": thread_id if thread_id else "test_user_123"
    }
}

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("planner_node", planner)
    graph_builder.add_node("plan_feasibility_checker_node", plan_feasibility_checker)
    graph_builder.add_node("plan_safty_critic_node", plan_safty_critic)
    graph_builder.add_node("plan_reviewer_node", plan_reviewer)
    graph_builder.add_node("executor_node", executor)
    graph_builder.add_node("replanner_node", replanner)

    graph_builder.add_edge(START, "planner_node")
    # graph_builder.add_edge("planner_node", "plan_feasibility_checker_node")
    # graph_builder.add_edge("planner_node", "plan_safty_critic_node")
    graph_builder.add_edge("plan_feasibility_checker_node", "plan_reviewer_node")
    graph_builder.add_edge("plan_safty_critic_node", "plan_reviewer_node")
    graph_builder.add_edge("replanner_node", "plan_feasibility_checker_node")
    graph_builder.add_edge("replanner_node", "plan_safty_critic_node")

    graph_builder.add_conditional_edges(
        source="planner_node",
        path=trivial_query_check
    )

    graph_builder.add_conditional_edges(
        source="plan_reviewer_node",
        path=plan_revise_check,
        path_map={
            "replan": "replanner_node",
            "execute": "executor_node"
        }
    )
    graph_builder.add_conditional_edges(
        source="executor_node",
        path=plan_execution_status,
        path_map={
            "pending":"executor_node",
            "done":END
        }
    )
    # state_input_user_query = {"user_query":"Give me all the files starting with '.py' in the 'tools' folder of this directory."}
    state = AgentState(
        input={"user_query":state_input_user_query}
        )
    
    with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
        graph = graph_builder.compile(checkpointer=checkpointer)
    # state_input_user_query = {"user_query":"Give me all the files ending with '.py' in the 'nodes' folder of the 'src' folder of this directory."}
        # for event in graph.stream(
        #         state,
        #         config=config
        #     ):
        #         print("-"*40)
        #         print(f"event\n{event}")
        #         print("-"*40)
        if resume_command:
            graph.invoke(
                Command(resume=resume_command),
                config=config
            )
        else:
            state = graph.invoke(
                state,
                config=config
                )
    print("="*50)
    print(f"state.final_output: {state["final_output"]}")
    print("="*50)
    if state["final_output"]:
        # return {"status": 200, "message":state["final_output"]}
        return state["final_output"]
    else:
        return {"status": 400, "message":"No output found.."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        # host="0.0.0.0",
        host="127.0.0.1",
        port=8080,
        use_colors=True,
        reload=True
        )
