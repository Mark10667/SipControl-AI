
# 🍷 SipControl: Behavioral Health AI Agent for Alcohol Reduction
<img width="65%" alt="sip_control_theme" src="https://github.com/user-attachments/assets/19615262-fefd-4495-91f7-df0202d52536" />

## 👥 Team Members
- **Mark**: Product & AI Agent ([LinkedIn](https://www.linkedin.com/in/mark-yecheng-ma/))
- **Tyler Li**: AI Agent, Backend & Cloud ([LinkedIn](https://www.linkedin.com/in/tyler-wq-li/))
- **Renee Schultz-Wu**: Full Stack ([LinkedIn](https://www.linkedin.com/in/renee-schultz-wu/))
- **Yolanda**: UI/UX & Product Design ([LinkedIn](https://www.linkedin.com/in/yolanda-tian/))

---

## ✨ Description
![3161746082431_ pic_hd](https://github.com/user-attachments/assets/617c16b7-a312-4a65-adf4-c0102286c926)

SipControl is a behavioral health AI agent designed to help individuals reduce or quit alcohol consumption through personalized, empathetic support. The agent combines daily self-reflection, proactive nudges, habit tracking, and relapse-prevention tools to guide users through their unique journey — one day at a time.

We believe real-time, non-judgmental digital support can bridge the gap between intention and action, empowering lasting change through compassion and accountability.

---

## 🗂️ Features

1. **Initial Intake Survey**: Customized goals (e.g., drink X% less per week)
<img width="392" alt="Screenshot 2025-05-01 at 1 35 37 AM" src="https://github.com/user-attachments/assets/96316bad-ac32-4fe0-8190-b13fa1aee6c1" />
<img width="401" alt="Screenshot 2025-05-01 at 1 29 15 AM" src="https://github.com/user-attachments/assets/d94a1766-7661-4862-aeac-e12d32a24f20" />
<img width="396" alt="Screenshot 2025-05-01 at 1 36 15 AM" src="https://github.com/user-attachments/assets/b5f216d0-a1aa-4ed0-a72a-26140c6a8a4b" />
<img width="406" alt="Screenshot 2025-05-01 at 1 36 41 AM" src="https://github.com/user-attachments/assets/355f87a8-63cf-48c0-8c6e-c07cbb3fa9b8" />

3. **Daily Self-Reporting**:
   - Users log their drinking at preferred times
   - AI extracts consumption details from natural language
   - Tracks against goals; celebrates milestones or supports improvement
  <img width="395" alt="Screenshot 2025-05-01 at 1 34 58 AM" src="https://github.com/user-attachments/assets/12bf5d40-b02a-4700-9f46-b4b9aaf01ca2" />

4. **Relapse-Prevention Conversations**:
   - When feeling triggered, users can talk to the agent for real-time support
<img width="284" alt="Screenshot 2025-05-01 at 1 38 56 AM" src="https://github.com/user-attachments/assets/7ce3f8df-1cbf-45e6-a1be-5205b53492c5" />

5. **Motivational Support**:
   - Celebrates small wins: fewer drinks, skipped sessions, sober streaks
<img width="396" alt="Screenshot 2025-05-01 at 1 30 52 AM" src="https://github.com/user-attachments/assets/fb5b3d36-07ca-4098-8265-58ec60789f4b" />


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
<img width="1706" alt="Screenshot 2025-05-01 at 1 21 17 AM" src="https://github.com/user-attachments/assets/7abb1f78-ba05-4096-ad66-e63849bd64de" />

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
<img width="1374" alt="Screenshot 2025-05-01 at 1 37 58 AM" src="https://github.com/user-attachments/assets/437e4782-0b12-4c77-b759-8c49cc1f9e0b" />

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
