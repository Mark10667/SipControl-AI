from typing import Annotated, Any, Dict, List, Tuple, TypedDict, Literal
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import Graph, StateGraph, ToolNode
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator
import os
from enum import Enum, auto
from typing import Optional
from datetime import datetime

# Define trigger types as an Enum
class TriggerType(str, Enum):
    STRESS = "stress"
    SOCIAL_PRESSURE = "social_pressure"
    BOREDOM = "boredom"
    UNKNOWN = "unknown"

class AgentState(TypedDict):
    messages: List[BaseMessage]
    next_step: str
    # drinking_status: Optional[bool]
    trigger_type: Optional[TriggerType]
    memory: Dict[str, Any]  # For storing user preferences and history
    session_id: str
    user_id: str
    session_type: Literal["DAILY_CHECKIN", "RELAPSE_SUPPORT", "SUGGESTION_REQUEST", "OTHER"]
    start_time_local: datetime
    start_time_system: datetime
    end_time_local: Optional[datetime]
    end_time_system: Optional[datetime]
    beverage_logs: List[Dict[str, float]]  # {type: str, quantity: float, volume_ml: float, abv: float, total_pure_alcohol_ml: float}
    met_goal: bool
    agent_suggestion: List[str]
    conversation_ended: bool  # New field to track if conversation should end




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
        ("system", '''
You are SipControl, an empathetic AI assistant that helps users manage their alcohol consumption and build healthier drinking habits.

Your role is to be the central coordinator of the conversation. You have access to the following tools:
1. alcohol_calculator: Calculate and track alcohol consumption
2. trigger_detector: Identify triggers for drinking behavior
3. stress_coping_agent: Provide stress management strategies
4. social_pressure_coping_agent: Help with social pressure situations
5. boredom_coping_agent: Suggest activities to combat boredom

For each user message:
1. Assess if they're discussing alcohol consumption
   - If yes, use alcohol_calculator to track and evaluate
   - Update beverage_logs with the results
2. If they're struggling or went over their goal:
   - Use trigger_detector to identify the cause
   - Based on the trigger, call the appropriate coping agent
3. Maintain a supportive, conversational tone
4. Decide if the conversation should continue or end

Return your response in this format:
CONTINUE or END
---
Your message to the user
---
Tool calls needed (if any):
tool1: parameters
tool2: parameters
        '''),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    def core_agent(state: AgentState) -> AgentState:
        response = chain.invoke({"messages": state["messages"]})
        
        # Parse the response
        parts = response.content.split('---')
        status = parts[0].strip()
        message = parts[1].strip()
        tool_calls = parts[2].strip() if len(parts) > 2 else ""
        
        # Update state
        state["conversation_ended"] = (status == "END")
        state["messages"].append(HumanMessage(content=message))
        
        # Parse tool calls if any
        if tool_calls:
            state["next_step"] = "tool_node"
        else:
            state["next_step"] = "end" if state["conversation_ended"] else "core_agent"
        
        return state
    
    return core_agent




# Reference ABV table (can expand later)
ABV_LOOKUP = {
    "beer": 0.05,
    "light_beer": 0.04,
    "wine": 0.12,
    "red_wine": 0.13,
    "white_wine": 0.11,
    "cabernet": 0.13,
    "vodka": 0.4,
    "whiskey": 0.4,
    "cocktail": 0.2
}

# Default volume (ml) per unit type
VOLUME_LOOKUP = {
    "glass": 150,
    "bottle": 750,
    "can": 355,
    "shot": 45
}

def alcohol_calculator(
    beverage_type: str,
    quantity: int,
    volume_ml_per_unit: int = None,
    abv: float = None,
    daily_goal_ml: float = 30.0  # e.g. ~2 standard drinks worth of pure alcohol
) -> Dict:
    """
    Estimate alcohol consumption and compare to goal.
    """
    beverage_type = beverage_type.lower()

    # Infer defaults if needed
    if abv is None:
        abv = ABV_LOOKUP.get(beverage_type, 0.12)
    if volume_ml_per_unit is None:
        volume_ml_per_unit = VOLUME_LOOKUP.get("glass", 150)

    total_volume = quantity * volume_ml_per_unit
    total_pure_alcohol_ml = total_volume * abv

    met_goal = total_pure_alcohol_ml <= daily_goal_ml

    return {
        "beverage_type": beverage_type,
        "quantity": quantity,
        "volume_ml_per_unit": volume_ml_per_unit,
        "abv": abv,
        "total_pure_alcohol_ml": round(total_pure_alcohol_ml, 2),
        "met_goal": met_goal,
        "feedback": "Goal met! Well done." if met_goal else "You went over the goal today, but it's okay — let's reflect on what happened."
    }



# Trigger identification agent
def create_trigger_identification_agent():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant specialized in identifying potential triggers for alcohol consumption. "
                  "Based on the conversation, identify the most likely trigger from the following options: "
                  "stress, social_pressure, boredom. "
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
    if not state["END"]:
        return "END"
    return "continue_core_agent"

# Updated function to route to appropriate coping agent based on trigger type
def get_coping_strategy(state: AgentState) -> str:
    if state["trigger_type"] == TriggerType.STRESS:
        return "stress_coping"
    elif state["trigger_type"] == TriggerType.SOCIAL_PRESSURE:
        return "social_pressure_coping"
    elif state["trigger_type"] == TriggerType.BOREDOM:
        return "boredom_coping"
    else:
        return "default_coping"

# Router node that updates state and returns next step
def router(state: AgentState) -> AgentState:
    state["next_step"] = get_next_step(state)
    return state

# Create the workflow graph (uncompiled version)
def create_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Define available tools
    tool_registry = {
        "alcohol_calculator": alcohol_calculator,
        "trigger_detector": create_trigger_identification_agent(),
        "stress_coping_agent": create_stress_coping_agent(),
        "social_pressure_coping_agent": create_social_pressure_coping_agent(),
        "boredom_coping_agent": create_boredom_coping_agent(),
    }
    
    # Create nodes
    workflow.add_node("core_agent", create_core_agent())
    workflow.add_node("tool_node", ToolNode(tool_registry))
    workflow.add_node("end", lambda x: x)
    
    # Set entry point
    workflow.set_entry_point("core_agent")
    
    # Define edges
    workflow.add_conditional_edges(
        "core_agent",
        lambda x: x["next_step"],
        {
            "tool_node": "tool_node",
            "core_agent": "core_agent",
            "end": "end"
        }
    )
    
    # After tools, always return to core_agent
    workflow.add_edge("tool_node", "core_agent")
    
    # Set finish point
    workflow.set_finish_point("end")
    
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
        "met_goal": None,
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

# def display_workflow_flowchart():
#     """
#     Generates and displays a flow chart of the drinking assessment workflow using graphviz and IPython.display.
#     This function is intended for use in Jupyter notebooks or IPython environments.
#     """
#     try:
#         from graphviz import Digraph
#         from IPython.display import Image, display
#     except ImportError:
#         print("graphviz and IPython.display are required to display the flow chart. Please install them with 'pip install graphviz ipython'.")
#         return

#     dot = Digraph(comment='Enhanced Drinking Assessment Workflow')
    
#     # Define nodes
#     dot.node('A', 'Start')
#     dot.node('B', 'Input: messages')
#     dot.node('C', 'Assess Drinking Status')
#     dot.node('D', 'Is user drinking?')
#     dot.node('E', 'Identify Trigger')
#     dot.node('F1', 'Stress Coping Strategies')
#     dot.node('F2', 'Social Pressure Strategies')
#     dot.node('F3', 'Boredom Strategies')
#     dot.node('F4', 'Default Coping Strategies')
#     dot.node('G', 'Append AI response to messages')
#     dot.node('H', 'Return messages, status, trigger')

#     # Define edges
#     dot.edge('A', 'B')
#     dot.edge('B', 'C')
#     dot.edge('C', 'D')
#     dot.edge('D', 'H', 'No')
#     dot.edge('D', 'E', 'Yes')
#     dot.edge('E', 'F1', 'Stress')
#     dot.edge('E', 'F2', 'Social Pressure')
#     dot.edge('E', 'F3', 'Boredom')
#     dot.edge('E', 'F4', 'Unknown Trigger')
    
#     # Connect all coping strategy nodes to G
#     dot.edge('F1', 'G')
#     dot.edge('F2', 'G')
#     dot.edge('F3', 'G')
#     dot.edge('F4', 'G')
#     dot.edge('G', 'H')

#     # Save and display
#     dot.render('enhanced_workflow_chart', format='png', cleanup=True)
#     display(Image(filename='enhanced_workflow_chart.png'))