from langchain_core.messages import HumanMessage
from workflow import run_workflow
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

def setup_environment():
    """Setup environment variables and configurations"""
    dotenv_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path)

def interactive_session():
    """Run an interactive session with the AI agent"""
    print("\n=== Welcome to SipControl AI Interactive Testing Session ===")
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'new' to start a new conversation thread")
    print("================================================\n")

    thread_id = None
    conversation_history = []

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit']:
            print("\nEnding session. Goodbye!")
            break
        
        # Check for new conversation command
        if user_input.lower() == 'new':
            thread_id = None
            conversation_history = []
            print("\n=== Starting new conversation ===\n")
            continue
        
        # Create message and add to history
        message = HumanMessage(content=user_input)
        conversation_history.append(message)
        
        try:
            # Run the workflow with the current message and history
            print("\n[Debug] Running workflow...")
            print(f"[Debug] Thread ID: {thread_id}")
            print(f"[Debug] History length: {len(conversation_history)}")
            
            result = run_workflow(conversation_history, thread_id=thread_id)
            
            # Store thread_id for conversation continuity
            if thread_id is None:
                thread_id = result.get("session_id")
            
            # Display agent's response
            print("\nAI Assistant:", end=" ")
            
            # Get the last AI message from the result
            if result["messages"]:
                last_message = result["messages"][-1]
                print(last_message.content)
            
            # Display additional information if available
            if result.get("trigger_type"):
                print(f"\n[Debug] Detected trigger: {result['trigger_type']}")
            if result.get("met_goal") is not None:
                print(f"[Debug] Goal status: {'Met' if result['met_goal'] else 'Not met'}")
            
            # Update conversation history with AI's response
            conversation_history = result["messages"]
            
        except Exception as e:
            import traceback
            print(f"\nError occurred: {str(e)}")
            print("\nFull traceback:")
            traceback.print_exc()
            print("\nPlease try again or type 'new' to start a fresh conversation.")

def run_test_scenarios():
    """Run predefined test scenarios"""
    test_scenarios = {
        "stress": "I'm really stressed at work and had several drinks yesterday to calm down.",
        "social": "My friends keep pressuring me to drink at parties.",
        "boredom": "I'm just sitting at home bored and thinking about having a drink.",
        "positive": "I managed to avoid drinking at the party last night!"
    }
    
    print("\n=== Running Test Scenarios ===\n")
    
    for scenario, message in test_scenarios.items():
        print(f"\n--- Testing {scenario.upper()} scenario ---")
        print(f"User: {message}")
        
        result = run_workflow([HumanMessage(content=message)])
        
        print("\nAI Assistant:", end=" ")
        if result["messages"]:
            print(result["messages"][-1].content)
        
        print("\nDebug Information:")
        if result.get("trigger_type"):
            print(f"Detected trigger: {result['trigger_type']}")
        if result.get("met_goal") is not None:
            print(f"Goal status: {'Met' if result['met_goal'] else 'Not met'}")
        
        print("\n" + "="*50)

def main():
    setup_environment()
    
    while True:
        print("\nSipControl AI Testing Menu:")
        print("1. Interactive Session")
        print("2. Run Test Scenarios")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            interactive_session()
        elif choice == "2":
            run_test_scenarios()
        elif choice == "3":
            print("\nExiting. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
