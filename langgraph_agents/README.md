# Drinking Assessment and Support Agent Workflow

This project implements a LangGraph-based agent workflow for assessing and supporting users who may be drinking alcohol. The workflow consists of multiple agents that work together to:

1. Assess if a user is drinking based on chat history
2. Provide coping strategies if drinking is detected
3. End the conversation appropriately

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Azure OpenAI credentials:
```
AZURE_API_KEY=your_azure_api_key_here
AZURE_ENDPOINT=your_azure_endpoint_here
GPT4_DEPLOYMENT=your_gpt4_deployment_name_here
```

## Usage

The workflow can be tested using the provided test script:

```bash
python test_workflow.py
```

To use the workflow in your own code:

```python
from langchain_core.messages import HumanMessage
from workflow import run_workflow

# Create a list of messages
messages = [
    HumanMessage(content="Your message here")
]

# Run the workflow
result = run_workflow(messages)

# Process the results
for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")
```

## Workflow Description

The workflow follows this process:

1. **Core Agent**: Analyzes the chat history to determine if the user is drinking (using Azure OpenAI GPT-4)
2. **Router**: Directs the flow based on the drinking assessment
3. **Coping Solution Agent**: Provides support and coping strategies if drinking is detected (using Azure OpenAI GPT-4)
4. **End Conversation**: Concludes the interaction appropriately

## Customization

You can modify the prompts and logic in `workflow.py` to adjust:

- The assessment criteria for drinking behavior
- The type of coping strategies provided
- The conversation flow and responses
- Azure OpenAI model parameters (temperature, deployment names, etc.) 