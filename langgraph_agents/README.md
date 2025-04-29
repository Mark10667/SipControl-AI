# LangGraph Agents

This folder contains the workflow and test scripts for the drinking assessment agent.

## Setup Instructions

### 1. Clone the repository (if you haven't already)
```
git clone <your-repo-url>
cd SipControl-AI/langgraph_agents
```

### 2. Create and activate the Python environment
We recommend using conda to manage dependencies and ensure compatibility (Python 3.12 or lower is required for some packages):

```
conda create -n agent_py312 python=3.12 -y
conda activate agent_py312
```

### 3. Install required Python packages
```
pip install -r requirements.txt
```
If you don't have a `requirements.txt`, install the following manually:
```
pip install langchain-core langchain-openai python-dotenv graphviz ipython
```

### 4. Install Graphviz system package
Graphviz is required for flow chart visualization:
- **macOS:**
  ```
  brew install graphviz
  ```
- **Ubuntu/Debian:**
  ```
  sudo apt-get install graphviz
  ```
- **Windows:**
  Download and install from [Graphviz Downloads](https://graphviz.gitlab.io/download/)

### 5. Set up environment variables
Create a `.env` file in this directory with your Azure OpenAI credentials:
```
AZURE_API_KEY=your_azure_api_key
AZURE_ENDPOINT=your_azure_endpoint
GPT4_DEPLOYMENT=your_gpt4_deployment_name
```

## Running the Test Script

To run the test workflow script, use:
```
python test_workflow.py
```

This will execute the test cases and print the results to the console.

## Visualizing the Workflow

To visualize the workflow as a flow chart, open the provided Jupyter notebook (or create one) and run:
```python
from workflow import display_workflow_flowchart

display_workflow_flowchart()
```

## Troubleshooting
- **ModuleNotFoundError:** If you see errors about missing modules (e.g., `langchain_core`), make sure you have installed all required Python packages in the active environment.
- **ExecutableNotFound: 'dot':** If you see errors about `dot` not found, make sure you have installed the Graphviz system package and that it is on your system's PATH.
- **Python version issues:** Some packages require Python 3.12 or lower. Use the provided conda environment instructions.

---

For further help, please check the code comments or open an issue in the repository. 