from typing import Annotated, Any, Dict, List, Tuple, TypedDict, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator
import os
from enum import Enum, auto
from typing import Optional
from datetime import datetime
from langchain.tools import StructuredTool, Tool
from typing_extensions import TypedDict
import uuid

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
    # start_time_system: datetime
    # end_time_local: Optional[datetime]
    # end_time_system: Optional[datetime]
    beverage_logs: List[Dict[str, float]]  # {type: str, quantity: float, volume_ml: float, abv: float, total_pure_alcohol_ml: float}
    met_goal: bool
    agent_suggestion: List[str]
    conversation_ended: bool  # New field to track if conversation should end
    step_counter: int  # Add this new field
    debug_log: List[Dict[str, str]]  # Add this new field
    tool_output: Optional[Dict[str, Any]]  # Add this field to store tool results

# Add this function to track tool usage
def log_step(state: AgentState, step_name: str, details: str) -> None:
    """Helper function to log steps in the conversation"""
    # if "debug_log" not in state:
    #     state["debug_log"] = []
    state["debug_log"].append({
        "step": state["step_counter"],
        "current_step": step_name,
        "details": details,
        "next_step": state["next_step"], # Add the next action
        "met_goal": state["met_goal"],
        "trigger_type": state["trigger_type"]
    })
    # print("current state:\n ", state)

def get_azure_chat_model(temperature=0):
    return AzureChatOpenAI(
        azure_deployment=os.getenv("GPT4_DEPLOYMENT"),
        openai_api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_ENDPOINT").rstrip('/'),  # Remove trailing slash if present
        api_key=os.getenv("AZURE_API_KEY"),
        temperature=temperature
    )

# Core agent that processes the conversation and makes initial assessment
def core_agent(state: AgentState) -> AgentState:
    # Increment counter
    state["step_counter"] = state.get("step_counter", 0) + 1
    
    # Check for max steps
    MAX_STEPS = 5
    if state["step_counter"] >= MAX_STEPS:
        log_step(state, "core_agent", f"Reached maximum steps ({MAX_STEPS}). Ending conversation.")
        state["conversation_ended"] = True
        state["next_step"] = "end"
        state["messages"].append(AIMessage(content="I apologize, but I need to end this conversation loop. Please feel free to start a new conversation if you need more assistance."))
        return state
    
    # Create context summary from state using only existing fields
    context_summary = f"""
    Current conversation state:
    - Session type: {state['session_type']}
    - Beverage logs: {state['beverage_logs']}
    - Goal status: {'Met' if state.get('met_goal') else 'Not met' if state.get('met_goal') is False else 'Not evaluated'}
    - Identified trigger: {state.get('trigger_type', 'Not identified')}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", '''
        You are SipControl, an empathetic AI assistant that helps users manage their alcohol consumption and build healthier drinking habits.

        Your role is to be the central coordinator of the conversation. You have access to the following tools:
        1. alcohol_calculator: Calculate and track alcohol consumption
        2. trigger_detector: Identify triggers for drinking behavior
        3. stress_coping: Provide stress management strategies
        4. social_pressure_coping: Help with social pressure situations
        5. boredom_coping: Suggest activities to combat boredom

        IMPORTANT: Before responding, review the current conversation state.
        - If beverage logs exist, acknowledge and reference the drinking information
        - If a trigger has been identified, use the appropriate coping strategy
        - Maintain continuity in the conversation

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
        Tool calls needed (only one tool at a time): 
        {{"name": "alcohol_calculator", "parameters": {{"beverage_type": "<type of drink>", "quantity": "<number>", "unit": "<glass/bottle/can/shot>"}}}}
        or
        {{"name": "trigger_detector"}}
        or
        {{"name": "stress_coping"}}
        or
        {{"name": "social_pressure_coping"}}
        or
        {{"name": "boredom_coping"}}
        or
        {{"name": "default_coping"}}
        '''),
        ("system", context_summary),  # Add the context summary as a system message
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    
    response = chain.invoke({"messages": state["messages"]})
    
    # Clean up the response content by removing extra spaces and normalizing newlines
    cleaned_content = response.content.replace('\n', ' ').strip()
    parts = [part.strip() for part in cleaned_content.split('---')]
    
    status = parts[0].strip()
    message = parts[1].strip() if len(parts) > 1 else ""
    tool_calls = parts[2].strip() if len(parts) > 2 else ""
    
    if tool_calls:
        state["next_step"] = "tool_node"
    else:
        state["next_step"] = "core_agent" if not state["conversation_ended"] else "end"
    
    # Move log_step here after next_step is determined
    log_step(state, "core_agent", f"""
    Status: {status}
    Message: {message}
    Tool Calls: {tool_calls if tool_calls else 'None'}
    """)
    
    state["conversation_ended"] = (status == "END")
    state["messages"].append(AIMessage(content=message))
    
    # Handle tool results if they exist
    if "tool_output" in state and state["tool_output"] is not None:  # Add None check
        tool_output = state["tool_output"]
        if "type" in tool_output and "data" in tool_output:  # Add safety checks
            output_type = tool_output["type"]
            data = tool_output["data"]
            
            if output_type == "alcohol_result":
                state["beverage_logs"].append(data)
                state["met_goal"] = data["met_goal"]
            elif output_type == "trigger_result":
                state["trigger_type"] = data["trigger_type"]
                state["messages"].append(HumanMessage(content=data["explanation"]))
            elif output_type == "coping_response":
                state["messages"].append(AIMessage(content=data["response"]))
    
    return state
    
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
    unit: str,
    abv: float = None,
    daily_goal_ml: float = 30.0
) -> Dict:
    """Calculate alcohol consumption and return results"""

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~alcohol_calculator~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    beverage_type = beverage_type.lower()

    # Infer defaults if needed
    if abv is None:
        abv = ABV_LOOKUP.get(beverage_type, 0.12)
    
    volume_ml_per_unit = VOLUME_LOOKUP.get(unit, 150)
    total_volume = quantity * volume_ml_per_unit
    total_pure_alcohol_ml = total_volume * abv
    met_goal = total_pure_alcohol_ml <= daily_goal_ml

    return {
        "type": "alcohol_result",
        "data": {
            "beverage_type": beverage_type,
            "quantity": quantity,
            "volume_ml_per_unit": volume_ml_per_unit,
            "abv": abv,
            "total_pure_alcohol_ml": round(total_pure_alcohol_ml, 2),
            "met_goal": met_goal
        }
    }

# Trigger identification agent
def trigger_detector(messages: List[BaseMessage]) -> Dict:
    """Identify triggers and return results"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''
        You are a behavioral health AI assistant with expertise in addiction psychology and relapse prevention. 
        Your role is to analyze user conversations and identify the most likely psychological trigger behind alcohol use episodes.

        Based on the conversation, identify the most likely trigger from these options:
        - stress
        - social_pressure
        - boredom
        If none apply, respond with 'unknown'.

        Return your response in this format:
        TRIGGER_TYPE
        ---
        Brief explanation of why you identified this trigger
        '''),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.3)
    chain = prompt | model
    response = chain.invoke({"messages": messages})
    
    parts = response.content.split('---')
    trigger = parts[0].strip().lower()
    explanation = parts[1].strip() if len(parts) > 1 else ""
    
    try:
        trigger_type = TriggerType(trigger)
    except ValueError:
        trigger_type = TriggerType.UNKNOWN
    
    return {
        "type": "trigger_result",
        "data": {
            "trigger_type": trigger_type,
            "explanation": explanation
        }
    }

# Create specialized coping strategy agents for each trigger type
def stress_coping(messages: List[BaseMessage]) -> Dict:
    """Provide stress management strategies"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''
        You are a behavioral health AI assistant specialized in helping users manage stress without turning to alcohol. 
        With expertise in stress psychology and self-regulation techniques, your goal is to offer practical, supportive strategies that reduce anxiety and tension.
         
        Provide compassionate, practical stress-reduction strategies such as:
        - Deep breathing exercises
        - Progressive muscle relaxation
        - Guided imagery
        - Mindfulness techniques

        Return your response in this format:
        CONTINUE
        ---
        Your supportive message with specific stress management strategies
        '''),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    response = chain.invoke({"messages": messages})
    
    return {
        "type": "coping_response",
        "data": {
            "response": response.content,
            "continue_conversation": True
        }
    }
    
def social_pressure_coping(messages: List[BaseMessage]) -> Dict:
    """Provide social pressure management strategies"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''
        You are a behavioral health AI assistant specialized in helping users resist social pressure to drink. 
        You understand the dynamics of peer influence, confidence building, and healthy boundary setting.
                
        Provide strategies for:
        - Assertive refusal skills
        - Alternative social activities
        - Managing peer pressure
        - Building confidence in social situations

        Return your response in this format:
        CONTINUE
        ---
        Your supportive message with specific social pressure management strategies
        '''),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    response = chain.invoke({"messages": messages})
    
    return {
        "type": "coping_response",
        "data": {
            "response": response.content,
            "continue_conversation": True
        }
    }
    
def boredom_coping(messages: List[BaseMessage]) -> Dict:
    """Provide boredom management strategies"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''
        You are a behavioral health AI assistant focused on helping users address boredom without resorting to alcohol. 
        You understand how boredom can lead to unhealthy coping, and aim to redirect users toward rewarding, stimulating alternatives.
                
        Provide engaging alternatives such as:
        - Hobby suggestions
        - Physical activities
        - Creative projects
        - Social connections
        - Learning opportunities

        Return your response in this format:
        CONTINUE
        ---
        Your supportive message with specific activity suggestions and engagement strategies
        '''),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    response = chain.invoke({"messages": messages})
    
    return {
        "type": "coping_response",
        "data": {
            "response": response.content,
            "continue_conversation": True
        }
    }

def default_coping(messages: List[BaseMessage]) -> Dict:
    """Provide default coping strategies"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''
        You are a supportive behavioral health AI assistant helping users who are drinking or considering drinking, but whose trigger is unclear. 
        Your goal is to offer grounding, holistic strategies that promote well-being, reflection, and healthy alternatives to alcohol.
                
        Focus on:
        - General wellness strategies
        - Healthy alternatives to drinking
        - Building resilience
        - Self-reflection techniques

        Return your response in this format:
        CONTINUE
        ---
        Your supportive message with general coping strategies and encouragement
        '''),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    model = get_azure_chat_model(temperature=0.7)
    chain = prompt | model
    response = chain.invoke({"messages": messages})
    
    return {
        "type": "coping_response",
        "data": {
            "response": response.content,
            "continue_conversation": True
        }
    }

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

# # Router node that updates state and returns next step
# def router(state: AgentState) -> AgentState:
#     state["next_step"] = get_next_step(state)
#     return state
def create_tool_registry():
    """Return a list of Tool objects"""
    return [
        Tool.from_function(
            func=alcohol_calculator,
            name="alcohol_calculator",
            description="Calculate alcohol consumption and compare to daily goal"
        ),
        Tool.from_function(
            func=trigger_detector,
            name="trigger_detector",
            description="Identify triggers for drinking behavior"
        ),
        Tool.from_function(
            func=stress_coping,
            name="stress_coping",
            description="Provide stress management strategies"
        ),
        Tool.from_function(
            func=social_pressure_coping,
            name="social_pressure_coping",
            description="Help with social pressure situations"
        ),
        Tool.from_function(
            func=boredom_coping,
            name="boredom_coping",
            description="Suggest activities to combat boredom"
        ),
        Tool.from_function(
            func=default_coping,
            name="default_coping",
            description="Provide general coping strategies"
        )
    ]

# Then update the create_workflow function
def create_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Create nodes
    workflow.add_node("core_agent", core_agent)
    
    # Create ToolNode without output_key
    tools = create_tool_registry()
    tool_node = ToolNode(tools)  # Remove the output_key parameter
    
    # Add a wrapper function to store tool output in state
    def tool_node_with_state_update(state: AgentState):
        # Execute tool and get result
        result = tool_node.invoke(state)
        # Store the result in state
        state["tool_output"] = result
        return state
    
    workflow.add_node("tool_node", tool_node_with_state_update)
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
    
    return workflow

# Function to run the workflow with memory persistence
def run_workflow(messages: List[BaseMessage], thread_id: str = None) -> Dict:
    
    
    # Create the uncompiled workflow
    workflow = create_workflow()  # Use the existing create_workflow function
    
    # Prepare the initial state with all required fields
    initial_state = {
        "messages": messages,
        "next_step": "core_agent",
        "met_goal": None,
        "trigger_type": None,
        "memory": {},
        "step_counter": 0,
        "session_id": thread_id or str(uuid.uuid4()),
        "user_id": "",
        "session_type": "DAILY_CHECKIN",
        "start_time_local": datetime.now(),
        # "start_time_system": datetime.utcnow(),
        # "end_time_local": None,
        # "end_time_system": None,
        "beverage_logs": [],
        "agent_suggestion": [],
        "conversation_ended": False,
        "debug_log": [],  # Add this field
        "tool_output": None,  # Initialize as None
    }
    
    # Compile the workflow with memory saver
    app = workflow.compile()
    
    # Invoke the app with memory persistence
    result = app.invoke(
        initial_state
    )
    
    # Print debug information
    if "debug_log" in result:
        print("\n=== Debug Log ===")
        for entry in result["debug_log"]:
            print(f"\nStep {entry['step']}:")
            print(f"Current Step: {entry['current_step']}")
            print(f"Details: {entry['details']}")
            print(f"Next Step: {entry['next_step']}")
            if entry['met_goal'] is not None:
                print(f"Met Goal: {entry['met_goal']}")
            if entry['trigger_type']:
                print(f"Trigger Type: {entry['trigger_type']}")
        print("===============")
    
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