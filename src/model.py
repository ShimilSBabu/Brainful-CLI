from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
from time import sleep
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langgraph.prebuilt import ToolNode
from typing import Annotated, Sequence
from langgraph.graph.message import add_messages

load_dotenv()

MODELS=[
        "mistral-medium-latest",
        "mistral-large-latest",
        "mistral-small-latest"
        ]
API_KEYS=[
    os.environ["MISTRAL_API_KEY"],
    os.environ["MISTRAL_AUTONOMOUS_API_KEY"],
    # os.environ["MISTRAL_API_KEY_PM"],
    os.environ["MISTRAL_API_KEY_EJ"]
]

def get_llm_responce(messages, api_key, model, temperature, structured_output=""):
    try:
        llm = ChatMistralAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=64000
        )
        if structured_output:
            llm = llm.with_structured_output(structured_output)
            
        response = llm.invoke(messages)
        return {"status":1,"content":response.content}
    except Exception as e:
        return {"status":0,"content":str(e)}
        

def call_llm(messages, temperature=0.3, max_retries=15, llm_purpose="", structured_output=""):
    retry_count=0
    response=0
    
    if not messages:
        return {"status":0, "content":"Cannot process empty message."}
    for model in MODELS:
        for api_key in API_KEYS:
            if retry_count==max_retries:
                if response:
                    return {"status":0, "content":f"Max number of trial attempts reached. Error\n{response['content']}"}
                return {"status":0, "content":"Max number of trial attempts reached."}
            
            print(f"\nGetting response from {llm_purpose} LLM:: Trial Count: {retry_count+1}")
            response=get_llm_responce(messages, 
                                      api_key, 
                                      model=model, 
                                      temperature=temperature,
                                      structured_output=structured_output
                                      )
            
            if response["status"]:
                return response
            
            print(f"response: {response}")
            sleep(10)
            retry_count += 1

class MessagesState(BaseModel):
    messages:Annotated[Sequence[BaseMessage], add_messages]
    intermediate_output:str=""
    final_output:str=""


llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.1,
            api_key=os.environ["MISTRAL_AUTONOMOUS_API_KEY"],
            max_tokens=32000
        )

def should_continue(state: MessagesState):
    last = state.messages[-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END

def get_react_agent(system_message:str, human_message:str, tools:object):
    llm_with_tools = llm.bind_tools(tools)
    def call_llm(state: MessagesState):
        response = "Unable to reach the ReAct LLM."
        for trial_count in range(3):
            try:
                response = llm_with_tools.invoke(state.messages)
                return {"messages": [response]}
            except Exception as e:
                print(f"\nTrial {trial_count+1}/3:Retrying the ReAct agent due to the below mentioned error.\n{str(e)}\n")
                sleep(10)
        return {"messages": [response]}

    tool_node = ToolNode(tools, handle_tool_errors=True)

    graph = (
        StateGraph(MessagesState)
        .add_node("agent", call_llm)
        .add_node("tools", tool_node)
        .add_edge(START, "agent")
        .add_conditional_edges("agent", should_continue)
        .add_edge("tools", "agent")   # always loop back for self-correction
        .compile()
    )

    result = graph.invoke(
        {
        "messages": [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
            ]
    }
    )
    content = result["messages"][-1].content
    if "```" in content:
        json_start = content.find("```")
        json_end = content.rfind("```") + 1
        result["messages"][-1].content = content[json_start:json_end]
    return result