
# 🍷 SipControl: Behavioral Health AI Agent for Alcohol Reduction

## 👥 Team Members
- **Mark**: Product & AI Agent ([LinkedIn](https://www.linkedin.com/in/mark-yecheng-ma/))
- **Tyler Li**: AI Agent, Backend & Cloud ([LinkedIn](https://www.linkedin.com/in/tyler-wq-li/))
- **Renee Schultz-Wu**: Full Stack ([LinkedIn](https://www.linkedin.com/in/renee-schultz-wu/))
- **Yolanda**: UI/UX & Product Design ([LinkedIn](https://www.linkedin.com/in/yolanda-tian/))

---

## ✨ Description

SipControl is a behavioral health AI agent designed to help individuals reduce or quit alcohol consumption through personalized, empathetic support. The agent combines daily self-reflection, proactive nudges, habit tracking, and relapse-prevention tools to guide users through their unique journey — one day at a time.

We believe real-time, non-judgmental digital support can bridge the gap between intention and action, empowering lasting change through compassion and accountability.

---

## 🗂️ Features

1. **Initial Intake Survey**: Customized goals (e.g., drink X% less per week)
2. **Daily Self-Reporting**:
   - Users log their drinking at preferred times
   - AI extracts consumption details from natural language
   - Tracks against goals; celebrates milestones or supports improvement
3. **Relapse-Prevention Conversations**:
   - When feeling triggered, users can talk to the agent for real-time support
4. **Motivational Support**:
   - Celebrates small wins: fewer drinks, skipped sessions, sober streaks

---

## ✅ Our Differentiation

### 🔍 Deep Exploration of Triggers and Motivation
Goes beyond basic survey data to uncover internal conflicts and build a tailored support plan.

### 🎯 Curated, Actionable Coping Strategies
Provides clear, evidence-based next steps instead of vague suggestions.

### 🔄 Behavioral Pattern Learning
Learns over time what strategies work for each individual and adapts support accordingly.

---

## 🎯 Who Benefits

SipControl supports individuals struggling with alcohol use and looking for personalized, nonjudgmental help to form healthier habits. With motivation tracking, daily check-ins, trigger detection, and action planning, users are guided toward lasting change.

---

## 🏗️ Technical Architecture Overview

**Cloud Stack**:
- **Frontend**: HTML/CSS/JavaScript (React-ready)
- **Backend**: Flask (Python)
- **AI**: Azure OpenAI (GPT-4)
- **Database**: Azure Cosmos DB (MongoDB API)
- **File Storage**: Azure Blob (e.g., quit manuals)
- **Agent Logic**: LangGraph stategraph

**Design Principles**:
- Microservice-inspired separation of concerns
- Flask handles routing and logic
- LangGraph manages conversation workflow
- MongoDB stores structured data
- Azure OpenAI provides LLM responses

---

## ⚙️ Agent Workflow DAG

### Core Components
- **Core Agent**: Coordinates state, logic, and next steps
- **Tool Node**: Executes external tools (coping strategies, calculations)
- **Specialized Tools**:
  - `alcohol_calculator`
  - `trigger_detector`
  - `stress_coping`
  - `social_pressure_coping`
  - `boredom_coping`
  - `default_coping`

### Workflow Steps
1. Starts with Core Agent receiving user input
2. If needed, Core Agent calls a tool via Tool Node
3. Tool returns result → Core Agent processes it
4. Based on result, agent either:
   - Calls another tool
   - Updates state
   - Ends conversation

### Example
> User: *“I’m feeling stressed after work and thinking about drinking…”*  
- Core Agent detects risk  
- Calls `trigger_detector` → returns `"stress"`  
- Core Agent then calls `stress_coping` tool  
- Returns a coping strategy and updates the user with empathy

---

## 🔧 Technologies Used

- **Data**: Azure Cosmos DB (MongoDB API), Azure Blob Storage
- **AI**: Azure OpenAI (ChatGPT4o)
- **Backend**: Python Flask
- **Agent Framework**: LangGraph

---

## 🚀 Future Work

- Integrate Azure AI Studio and Prompt Flow for better orchestration
- Add Retrieval-Augmented Generation (RAG) for enhanced memory
- Add agent-driven calendar integration (e.g., reminders for walks or check-ins)
- Enable personalized push notifications during high-risk times (e.g., 9pm)

---
