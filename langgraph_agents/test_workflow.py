from langchain_core.messages import HumanMessage
from workflow import run_workflow, TriggerType
from dotenv import load_dotenv
import os
from pathlib import Path
from workflow import agent_memory_collection, get_latest_agent_memory, insert_test_user, agent_memory_collection
from typing import List, Dict

def main():
    # Load environment variables from parent directory
    dotenv_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path)
    
    # Clean up memory for test user before running tests
    user_id = "test_user"
    agent_memory_collection.delete_many({"user_id": user_id})
    
    insert_test_user(user_id, name="Test User", email="test@example.com")
    
    # Test cases for different trigger scenarios
    test_scenarios = {
        "stress": [
            HumanMessage(content="I'm really stressed at work and I've been drinking to calm my nerves. I can't seem to relax without a drink after my shift."),
        ],
        "social_pressure": [
            HumanMessage(content="I went out with friends last night and ended up drinking even though I didn't want to. They kept pushing drinks on me and I felt awkward saying no."),
        ],
        "boredom": [
            HumanMessage(content="I've been so bored lately. There's nothing to do at home so I've just been drinking to pass the time."),
        ],
        "negative_emotions": [
            HumanMessage(content="I got some really bad news yesterday and I'm feeling depressed. I started drinking to numb the feelings."),
        ],
        "fatigue": [
            HumanMessage(content="I've been so tired from working double shifts. I've been having a few drinks to help me unwind and fall asleep faster."),
        ],
        "celebrations": [
            HumanMessage(content="My friend's birthday is this weekend and I know there will be lots of drinking. I always drink too much at parties."),
        ],
        "loneliness": [
            HumanMessage(content="Living alone has been hard. I've started drinking in the evenings because I feel so lonely and it helps me forget."),
        ],
        "habitual_patterns": [
            HumanMessage(content="I've realized I'm automatically reaching for a drink when I get home. It's become such a habit I don't even think about it anymore."),
        ],
        "not_drinking": [
            HumanMessage(content="I've been feeling stressed but I'm trying to stay healthy by exercising and meditating instead of turning to alcohol."),
        ],
    }
    
    # Test with memory persistence across multiple interactions
    print("Testing memory persistence across interactions:")
    thread_id = "test_thread_123"
    
    # First interaction - establish drinking problem
    messages_first = [
        HumanMessage(content="I've been really stressed lately and I find myself drinking every evening after work.")
    ]
    
    # Second interaction - follow-up after some time
    messages_second = [
        HumanMessage(content="I tried those breathing exercises you suggested, but I still had a drink yesterday when my boss criticized my work.")
    ]
    
    # Run tests for each scenario
    for scenario, messages in test_scenarios.items():
        print(f"\n\n--- Testing {scenario.upper()} scenario ---")
        result = run_workflow(messages, user_id, thread_id)
        
        print("\nResult details:")
        print(f"Drinking status: {result['drinking_status']}")
        if "trigger_type" in result:
            print(f"Identified trigger: {result['trigger_type']}")
        
        print("\nFinal messages:")
        for msg in result["messages"]:
            print(f"{msg.type}: {msg.content[:100]}..." if len(msg.content) > 100 else f"{msg.type}: {msg.content}")
    
    # Test memory persistence
    print("\n\n--- Testing MEMORY PERSISTENCE ---")
    print("First interaction:")
    result_first = run_workflow(messages_first, user_id, thread_id)
    print(f"Drinking status: {result_first['drinking_status']}")
    if "trigger_type" in result_first:
        print(f"Identified trigger: {result_first['trigger_type']}")
    
    print("\nSecond interaction (same thread):")
    result_second = run_workflow(messages_second, user_id, thread_id)
    print(f"Drinking status: {result_second['drinking_status']}")
    if "trigger_type" in result_second:
        print(f"Identified trigger: {result_second['trigger_type']}")
    
    if "memory" in result_second:
        print("\nMemory contents after two interactions:")
        for key, value in result_second["memory"].items():
            print(f"{key}: {value}")

def test_individual_scenario(scenario_name, message_content):
    """Helper function to test a specific scenario with custom message"""
    messages = [HumanMessage(content=message_content)]
    
    print(f"\n--- Testing custom {scenario_name} scenario ---")
    result = run_workflow(messages, "test_user", "test_thread_123")
    
    print("\nResult details:")
    print(f"Drinking status: {result['drinking_status']}")
    if "trigger_type" in result:
        print(f"Identified trigger: {result['trigger_type']}")
    
    print("\nFinal messages:")
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content[:100]}..." if len(msg.content) > 100 else f"{msg.type}: {msg.content}")
    
    return result

if __name__ == "__main__":
    main()
    
    # Uncomment to run an individual test with a custom message
    # test_individual_scenario("custom scenario", "I've been drinking a lot lately because of problems at work and at home.")