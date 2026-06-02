from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

MODELS=[
        "mistral-medium-latest",
        "mistral-large-latest",
        "mistral-small-latest"
        ]
API_KEYS=[
    os.environ["MISTRAL_API_KEY"],
    os.environ["MISTRAL_AUTONOMOUS_API_KEY"],
    os.environ["MISTRAL_API_KEY_PM"],
    os.environ["MISTRAL_API_KEY_EJ"]
]

def get_llm_responce(messages, api_key, model, temperature):
    try:
        llm = ChatMistralAI(
            model=model,
            temperature=temperature,
            api_key=api_key       
        )
        response = llm.invoke(messages)
        return {"status":1,"content":response.content}
    except Exception as e:
        return {"status":0,"content":str(e)}
        

def call_llm(messages, temperature=0.3, max_retries=15, llm_purpose=""):
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
                                      temperature=temperature
                                      )
            
            if response["status"]:
                return response
            
            print(f"response: {response}")
            sleep(10)
            retry_count += 1