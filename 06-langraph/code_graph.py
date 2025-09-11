# flake8: noqa
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.constants import START, END
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import Literal

load_dotenv()

client = OpenAI()

class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool
    
class ClassifyCodingAccuracy(BaseModel):
    accuracy_percent: str

class State (TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percent : str | None
    is_coding_question: bool
    
def classify_message(state: State):
    print("⚠️ classify_message")
    query = state["user_query"]
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to detect if the user's query is
    related to coding question or not.
    Return the response in specified JSON boolean only.
    """
    
    #Structured responses
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content": query}
        ]
    )
    
    is_coding_question=response.choices[0].message.parsed.is_coding_question
    state["is_coding_question"]= is_coding_question
    return state

def coding_query(state: State):
    print("⚠️ coding_query")
    query = state["user_query"]
    SYSTEM_PROMPT = """
        You are a coding Expert Agent
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":query}
            ]
    )
    state["llm_result"]= response.choices[0].message.content
    return state

def coding_validate (state: State):
    print("⚠️ coding_validate")
    query = state["user_query"]
    llm_code = state["llm_result"]
    SYSTEM_PROMPT = f"""
        You are expert in calculating accuracy of the code according to the question.
        Return the percentage of accuracy
        
        User Query: {query}
        Code: {llm_code}
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=ClassifyCodingAccuracy,
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":query}
                 ]
    )
    state["accuracy_percent"]= response.choices[0].message.parsed.accuracy_percent
    return state

def routing_query(state: State) -> Literal["general_query","coding_query"]:
    print("⚠️ routing_query")
    is_coding = state["is_coding_question"]
    if is_coding:
        return "coding_query"
    
    return "general_query"

def general_query(state: State):
    print("⚠️ general_query")
    query = state["user_query"]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":query}
            ]
    )
    state["llm_result"]= response.choices[0].message.content
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("coding_query",coding_query)
graph_builder.add_node("coding_validate",coding_validate)
graph_builder.add_node("classify_message",classify_message)
graph_builder.add_node("routing_query",routing_query)
graph_builder.add_node("general_query",general_query)

graph_builder.add_edge(START,"classify_message")
graph_builder.add_conditional_edges("classify_message",routing_query)

graph_builder.add_edge("general_query",END)

graph_builder.add_edge("coding_query","coding_validate")
graph_builder.add_edge("coding_validate",END)


graph = graph_builder.compile()

def main():
    user = input(">")
    
    _state: State = {
        "user_query":user,
        "accuracy_percent":None,
        "is_coding_question": False,
        "llm_result": None
    }
    response = graph.invoke(_state)
    print(response)


main()