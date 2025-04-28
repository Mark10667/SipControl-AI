from typing import Annotated, Any, Dict, List, Tuple, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import Graph, StateGraph
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator
import os

# Define the state of our graph
class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_step: str
    drinking_status: bool | None

def get_azure_chat_model(temperature=0):
    return AzureChatOpenAI(
        azure_deployment=os.getenv("GPT4_DEPLOYMENT"),
        openai_api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_ENDPOINT").rstrip('/'),  # Remove trailing slash if present
        api_key=os.getenv("AZURE_API_KEY"),
        temperature=temperature
    )

# Core agent that processes the conversation and makes initial assessment
def create_core_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant helping assess if a user is drinking alcohol or not based on their chat history. "
                  "Analyze the conversation carefully and determine if there are any mentions or indications of alcohol consumption."),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Based on the chat history, determine if the user is drinking or not. "
                  "Respond with 'DRINKING' if you detect alcohol consumption, 'NOT_DRINKING' if you don't.")
    ])
    
    model = get_azure_chat_model(temperature=0)
    chain = prompt | model
    
    def core_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["drinking_status"] = response.content == "DRINKING"
        return state
    
    return core_agent

# Coping solution agent that provides help for drinking situations
def create_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant helping users who are drinking or considering drinking alcohol. "
                  "Provide compassionate, practical coping strategies and alternatives to drinking."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking or considering drinking. What coping strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def coping_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return coping_agent

# Function to determine next step based on drinking status
def get_next_step(state: AgentState) -> str:
    if state["drinking_status"]:
        return "drink"
    return "if not drink"

# Router node that updates state and returns next step
def router(state: AgentState) -> AgentState:
    state["next_step"] = get_next_step(state)
    return state

# Create the workflow graph
def create_workflow() -> Graph:
    # Initialize workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("core_agent", create_core_agent())
    workflow.add_node("router", router)
    workflow.add_node("coping_solution_agent", create_coping_agent())
    workflow.add_node("end_conversation", lambda x: x)
    
    # Add edges
    workflow.add_edge("core_agent", "router")
    workflow.set_entry_point("core_agent")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        get_next_step,  # Use the function that returns just the string
        {
            "drink": "coping_solution_agent",
            "if not drink": "end_conversation"
        }
    )
    
    # Add edge from coping agent to end
    workflow.add_edge("coping_solution_agent", "end_conversation")
    
    # Set the final node
    workflow.set_finish_point("end_conversation")
    
    return workflow.compile()

# Function to run the workflow
def run_workflow(messages: List[BaseMessage]) -> Dict:
    workflow = create_workflow()
    result = workflow.invoke({
        "messages": messages,
        "next_step": "core_agent",
        "drinking_status": None
    })
    return result 