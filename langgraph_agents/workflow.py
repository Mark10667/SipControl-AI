from typing import Annotated, Any, Dict, List, Tuple, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import Graph, StateGraph
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator
import os
from enum import Enum, auto

# Define trigger types as an Enum
class TriggerType(str, Enum):
    STRESS = "stress"
    SOCIAL_PRESSURE = "social_pressure"
    BOREDOM = "boredom"
    NEGATIVE_EMOTIONS = "negative_emotions"
    FATIGUE = "fatigue"
    CELEBRATIONS = "celebrations"
    LONELINESS = "loneliness"
    HABITUAL_PATTERNS = "habitual_patterns"
    UNKNOWN = "unknown"

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_step: str
    drinking_status: bool | None
    trigger_type: TriggerType | None
    memory: Dict[str, Any]  # For storing user preferences and history

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

# Trigger identification agent
def create_trigger_identification_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant specialized in identifying potential triggers for alcohol consumption. "
                  "Based on the conversation, identify the most likely trigger from the following options: "
                  "stress, social_pressure, boredom, negative_emotions, fatigue, celebrations, loneliness, habitual_patterns. "
                  "If none seem applicable, respond with 'unknown'."),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Based on the chat history, what seems to be the most likely trigger? "
                  "Respond with exactly one word from the list of triggers provided.")
    ])
    
    model = get_azure_chat_model(temperature=0.3)
    chain = prompt | model
    
    def trigger_agent(state: AgentState) -> AgentState:
        # Check memory first to see if we've already identified a pattern
        if state.get("memory", {}).get("common_triggers"):
            common_triggers = state["memory"]["common_triggers"]
            # Use memory to influence the identification (simplified logic)
            # In a real implementation, this would be more sophisticated
            
        response = chain.invoke({"messages": state["messages"]})
        trigger = response.content.strip().lower()
        
        # Map response to TriggerType enum
        try:
            state["trigger_type"] = TriggerType(trigger)
        except ValueError:
            state["trigger_type"] = TriggerType.UNKNOWN
            
        # Update memory with this trigger
        if "memory" not in state:
            state["memory"] = {}
        if "trigger_history" not in state["memory"]:
            state["memory"]["trigger_history"] = []
            
        # Add this trigger to history
        state["memory"]["trigger_history"].append(state["trigger_type"])
        
        # If we have enough history, identify common patterns
        if len(state["memory"]["trigger_history"]) >= 3:
            from collections import Counter
            trigger_counts = Counter(state["memory"]["trigger_history"])
            common_triggers = [t for t, c in trigger_counts.most_common(2)]
            state["memory"]["common_triggers"] = common_triggers
            
        return state
    
    return trigger_agent

# Create specialized coping strategy agents for each trigger type
def create_stress_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users manage stress without alcohol. "
                  "Provide compassionate, practical stress-reduction strategies such as deep breathing exercises, "
                  "progressive muscle relaxation, and guided imagery."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking due to stress. What stress management strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def stress_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return stress_agent

def create_social_pressure_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users resist social pressure to drink. "
                  "Provide strategies for assertive refusal skills and suggestions for alternative social activities."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking due to social pressure. What strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def social_pressure_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return social_pressure_agent

def create_boredom_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users address boredom without alcohol. "
                  "Provide engaging hobby ideas and mindfulness practices to prevent boredom-induced drinking."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking due to boredom. What alternative activities would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def boredom_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return boredom_agent

# Add the missing coping agent functions

def create_negative_emotions_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users manage negative emotions without alcohol. "
                  "Provide compassionate strategies for emotional awareness, acceptance, and healthy coping mechanisms like journaling."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking due to negative emotions. What emotional coping strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def negative_emotions_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return negative_emotions_agent

def create_fatigue_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users manage fatigue without alcohol. "
                  "Provide effective sleep hygiene tips, energy-boosting activities, and nutritional advice."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking due to fatigue. What energy management strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def fatigue_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return fatigue_agent

def create_celebrations_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users navigate celebrations without alcohol. "
                  "Provide ideas for alcohol-free events, non-alcoholic beverage options, and setting personal boundaries."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be concerned about drinking at celebrations. What alcohol-free celebration strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def celebrations_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return celebrations_agent

def create_loneliness_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users cope with loneliness without alcohol. "
                  "Provide strategies for social connection, volunteering opportunities, and meaningful solitary activities."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking due to loneliness. What social connection strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def loneliness_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return loneliness_agent

def create_habitual_patterns_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant specialized in helping users break habitual drinking patterns. "
                  "Provide habit tracking methods, ideas for new rituals, and mindfulness techniques for habit disruption."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking out of habit. What habit-breaking strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def habitual_patterns_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return habitual_patterns_agent

# Default coping solution agent for unknown triggers
def create_default_coping_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a supportive AI assistant helping users who are drinking or considering drinking alcohol. "
                  "Provide compassionate, practical coping strategies and alternatives to drinking."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "The user appears to be drinking. What coping strategies would you suggest?")
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def default_coping_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        state["messages"].append(response)
        state["next_step"] = "end"
        return state
    
    return default_coping_agent

# Function to determine next step based on drinking status
def get_next_step(state: AgentState) -> str:
    if state["drinking_status"]:
        return "identify_trigger"
    return "if not drink"

# Updated function to route to appropriate coping agent based on trigger type
def get_coping_strategy(state: AgentState) -> str:
    if state["trigger_type"] == TriggerType.STRESS:
        return "stress_coping"
    elif state["trigger_type"] == TriggerType.SOCIAL_PRESSURE:
        return "social_pressure_coping"
    elif state["trigger_type"] == TriggerType.BOREDOM:
        return "boredom_coping"
    elif state["trigger_type"] == TriggerType.NEGATIVE_EMOTIONS:
        return "negative_emotions_coping"
    elif state["trigger_type"] == TriggerType.FATIGUE:
        return "fatigue_coping"
    elif state["trigger_type"] == TriggerType.CELEBRATIONS:
        return "celebrations_coping"
    elif state["trigger_type"] == TriggerType.LONELINESS:
        return "loneliness_coping"
    elif state["trigger_type"] == TriggerType.HABITUAL_PATTERNS:
        return "habitual_patterns_coping"
    else:
        return "default_coping"

# Router node that updates state and returns next step
def router(state: AgentState) -> AgentState:
    state["next_step"] = get_next_step(state)
    return state

# # Create the workflow graph
# def create_workflow() -> Graph:
#     # Initialize workflow graph
#     workflow = StateGraph(AgentState)
    
#     # Add nodes
#     workflow.add_node("core_agent", create_core_agent())
#     workflow.add_node("router", router)
#     workflow.add_node("trigger_identification", create_trigger_identification_agent())
    
#     # Add specialized coping strategy nodes
#     workflow.add_node("stress_coping", create_stress_coping_agent())
#     workflow.add_node("social_pressure_coping", create_social_pressure_coping_agent())
#     workflow.add_node("boredom_coping", create_boredom_coping_agent())
#     # Add more specialized coping nodes for other trigger types
    
#     workflow.add_node("default_coping", create_default_coping_agent())
#     workflow.add_node("end_conversation", lambda x: x)
    
#     # Add edges
#     workflow.add_edge("core_agent", "router")
#     workflow.set_entry_point("core_agent")
    
#     # Add conditional edges from router
#     workflow.add_conditional_edges(
#         "router",
#         get_next_step,
#         {
#             "identify_trigger": "trigger_identification",
#             "if not drink": "end_conversation"
#         }
#     )
    
#     # Add conditional edges from trigger identification to appropriate coping strategy
#     workflow.add_conditional_edges(
#         "trigger_identification",
#         get_coping_strategy,
#         {
#             "stress_coping": "stress_coping",
#             "social_pressure_coping": "social_pressure_coping",
#             "boredom_coping": "boredom_coping",
#             #TODO: Add edges for other trigger types
#             "default_coping": "default_coping"
#         }
#     )
    
#     # Add edges from all coping strategies to end
#     workflow.add_edge("stress_coping", "end_conversation")
#     workflow.add_edge("social_pressure_coping", "end_conversation")
#     workflow.add_edge("boredom_coping", "end_conversation")
#     # Add edges for other coping strategies
#     workflow.add_edge("default_coping", "end_conversation")
    
#     # Set the final node
#     workflow.set_finish_point("end_conversation")
    
#     return workflow.compile()
# Create the workflow graph (uncompiled version)
def create_workflow() -> StateGraph:
    # Initialize workflow graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("core_agent", create_core_agent())
    workflow.add_node("router", router)
    workflow.add_node("trigger_identification", create_trigger_identification_agent())
    
    # Add specialized coping strategy nodes
    workflow.add_node("stress_coping", create_stress_coping_agent())
    workflow.add_node("social_pressure_coping", create_social_pressure_coping_agent())
    workflow.add_node("boredom_coping", create_boredom_coping_agent())
    
    # Add the missing coping strategy nodes for other trigger types
    workflow.add_node("negative_emotions_coping", create_negative_emotions_coping_agent())
    workflow.add_node("fatigue_coping", create_fatigue_coping_agent())
    workflow.add_node("celebrations_coping", create_celebrations_coping_agent())
    workflow.add_node("loneliness_coping", create_loneliness_coping_agent())
    workflow.add_node("habitual_patterns_coping", create_habitual_patterns_coping_agent())
    
    workflow.add_node("default_coping", create_default_coping_agent())
    workflow.add_node("end_conversation", lambda x: x)
    
    # Add edges
    workflow.add_edge("core_agent", "router")
    workflow.set_entry_point("core_agent")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        get_next_step,
        {
            "identify_trigger": "trigger_identification",
            "if not drink": "end_conversation"
        }
    )
    
    # Add conditional edges from trigger identification to appropriate coping strategy
    workflow.add_conditional_edges(
        "trigger_identification",
        get_coping_strategy,
        {
            "stress_coping": "stress_coping",
            "social_pressure_coping": "social_pressure_coping",
            "boredom_coping": "boredom_coping",
            "negative_emotions_coping": "negative_emotions_coping",
            "fatigue_coping": "fatigue_coping",
            "celebrations_coping": "celebrations_coping",
            "loneliness_coping": "loneliness_coping",
            "habitual_patterns_coping": "habitual_patterns_coping",
            "default_coping": "default_coping"
        }
    )
    
    # Add edges from all coping strategies to end
    workflow.add_edge("stress_coping", "end_conversation")
    workflow.add_edge("social_pressure_coping", "end_conversation")
    workflow.add_edge("boredom_coping", "end_conversation")
    workflow.add_edge("negative_emotions_coping", "end_conversation")
    workflow.add_edge("fatigue_coping", "end_conversation")
    workflow.add_edge("celebrations_coping", "end_conversation")
    workflow.add_edge("loneliness_coping", "end_conversation")
    workflow.add_edge("habitual_patterns_coping", "end_conversation")
    workflow.add_edge("default_coping", "end_conversation")
    
    # Set the final node
    workflow.set_finish_point("end_conversation")
    
    return workflow  # Return uncompiled workflow

# Function to run the workflow with memory persistence
def run_workflow(messages: List[BaseMessage], thread_id: str = None) -> Dict:
    from langgraph.checkpoint.memory import MemorySaver
    
    # Initialize memory saver for persistence
    memory_saver = MemorySaver()
    
    # Create the uncompiled workflow
    workflow = create_workflow()  # Use the existing create_workflow function
    
    # Compile the workflow with memory saver
    app = workflow.compile(checkpointer=memory_saver)
    
    # Prepare the initial state
    initial_state = {
        "messages": messages,
        "next_step": "core_agent",
        "drinking_status": None,
        "trigger_type": None,
        "memory": {}
    }
    
    # Generate a default thread_id if none is provided
    if thread_id is None:
        import uuid
        thread_id = str(uuid.uuid4())
    
    # Configure the thread_id for the checkpointer
    config = {"configurable": {"thread_id": thread_id}}
    
    # Invoke the app with memory persistence
    result = app.invoke(
        initial_state,
        config=config
    )
    
    return result

def display_workflow_flowchart():
    """
    Generates and displays a flow chart of the drinking assessment workflow using graphviz and IPython.display.
    This function is intended for use in Jupyter notebooks or IPython environments.
    """
    try:
        from graphviz import Digraph
        from IPython.display import Image, display
    except ImportError:
        print("graphviz and IPython.display are required to display the flow chart. Please install them with 'pip install graphviz ipython'.")
        return

    dot = Digraph(comment='Enhanced Drinking Assessment Workflow')
    
    # Define nodes
    dot.node('A', 'Start')
    dot.node('B', 'Input: messages')
    dot.node('C', 'Assess Drinking Status')
    dot.node('D', 'Is user drinking?')
    dot.node('E', 'Identify Trigger')
    dot.node('F1', 'Stress Coping Strategies')
    dot.node('F2', 'Social Pressure Strategies')
    dot.node('F3', 'Boredom Strategies')
    dot.node('F4', 'Negative Emotions Strategies')
    dot.node('F5', 'Other Specialized Strategies')
    dot.node('F6', 'Default Coping Strategies')
    dot.node('G', 'Append AI response to messages')
    dot.node('H', 'Return messages, status, trigger')

    # Define edges
    dot.edge('A', 'B')
    dot.edge('B', 'C')
    dot.edge('C', 'D')
    dot.edge('D', 'H', 'No')
    dot.edge('D', 'E', 'Yes')
    dot.edge('E', 'F1', 'Stress')
    dot.edge('E', 'F2', 'Social Pressure')
    dot.edge('E', 'F3', 'Boredom')
    dot.edge('E', 'F4', 'Negative Emotions')
    dot.edge('E', 'F5', 'Other Triggers')
    dot.edge('E', 'F6', 'Unknown Trigger')
    
    # Connect all coping strategy nodes to G
    dot.edge('F1', 'G')
    dot.edge('F2', 'G')
    dot.edge('F3', 'G')
    dot.edge('F4', 'G')
    dot.edge('F5', 'G')
    dot.edge('F6', 'G')
    dot.edge('G', 'H')

    # Save and display
    dot.render('enhanced_workflow_chart', format='png', cleanup=True)
    display(Image(filename='enhanced_workflow_chart.png'))