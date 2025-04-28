from langchain_core.messages import HumanMessage
from workflow import run_workflow
from dotenv import load_dotenv
import os
from pathlib import Path

def main():
    # Load environment variables from parent directory
    dotenv_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path)
    
    # Test case 1: User indicating drinking
    messages_drinking = [
        HumanMessage(content="I'm really stressed and I've been drinking a lot lately to cope."),
    ]
    
    # Test case 2: User not indicating drinking
    messages_not_drinking = [
        HumanMessage(content="I've been feeling stressed but I'm trying to stay healthy by exercising."),
    ]
    
    print("Testing with drinking scenario:")
    result_drinking = run_workflow(messages_drinking)
    print("\nFinal messages:")
    for msg in result_drinking["messages"]:
        print(f"{msg.type}: {msg.content}")
    
    print("\nTesting with non-drinking scenario:")
    result_not_drinking = run_workflow(messages_not_drinking)
    print("\nFinal messages:")
    for msg in result_not_drinking["messages"]:
        print(f"{msg.type}: {msg.content}")

if __name__ == "__main__":
    main() 