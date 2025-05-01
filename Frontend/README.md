# SipControl App Documentation

## 0. How to run
```Terminal
npm install
npm run dev
```

## 1. Application Overview

SipControl is a mobile-friendly web application designed to help users manage their alcohol consumption. The app provides supportive chat interactions in two modes: "Sober" for those maintaining sobriety, and "Drink" for those who need support while consuming alcohol. The application features user authentication, personalized onboarding, a dashboard with progress tracking, and an AI-powered chat interface.

## 2. Architecture

### 2.1 Technical Stack
- **Frontend**: React (Single-Page Application)
- **Backend**: Python Flask
- **Chatbot**: Azure AI services
- **Routing**: React Router
- **State Management**: React Context API + local component state

### 2.2 Overall Architecture
SipControl follows a client-server architecture:
- The React frontend handles UI rendering and client-side routing
- The Flask backend serves API endpoints and connects to Azure services
- All data persists across navigation without page reloads

## 3. Project Structure

```
.
├── backend/
│   ├── app.py              # Flask backend
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML entry point
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   │   ├── Auth/       # Authentication components
│   │   │   ├── Onboarding/ # Survey components
│   │   │   ├── Home/       # Dashboard components
│   │   │   ├── Chat/       # Chat interface components
│   │   │   └── common/     # Shared UI elements
│   │   ├── pages/          # Page containers
│   │   ├── context/        # State management
│   │   ├── utils/          # Helper functions
│   │   ├── styles/         # CSS files
│   │   ├── App.jsx         # Application root
│   │   └── index.jsx       # JavaScript entry point
│   └── package.json        # Frontend dependencies
└── deploy.sh               # Deployment script
```

## 4. Component Hierarchy

```
App
├── AuthPage
│   ├── LoginForm
│   └── SignupForm
├── OnboardingPage
│   ├── SurveyContainer
│   ├── SurveyQuestion
│   └── SurveyNavigation
├── HomePage
│   ├── DailyStats
│   ├── GoalProgress
│   └── MoodTracker
└── ChatPage
    ├── ChatContainer
    ├── Message
    ├── InputBar
    ├── TipsList
    └── Celebration
```

## 5. Key Features & Implementation

### 5.1 User Authentication
- Simple login/signup forms
- JWT-based authentication (for production)
- For hackathon demo: simplified authentication with local state

### 5.2 Onboarding Flow
- Multi-step survey to collect user information
- Questions about drinking habits, goals, and challenges
- Progress tracking through survey steps

### 5.3 Home Dashboard
- Display of user's sobriety streak
- Progress toward goals
- Daily mood tracking

### 5.4 Chat Interface
- Two modes: "Sober" and "Drink"
- AI-powered responses based on user input
- Support features:
  - Tips for avoiding alcohol in social situations
  - Celebration animations for sobriety milestones
  - Customized responses based on user's history and goals

## 6. Data Flow

### 6.1 Authentication Flow
1. User enters credentials on AuthPage
2. Frontend sends auth request to backend
3. Backend validates and returns user data
4. Frontend updates UserContext with login state
5. User is redirected to Onboarding or Home based on their status

### 6.2 Chat Flow
1. User sends message from ChatPage
2. Frontend displays user message and sends to backend
3. Backend processes message with Azure AI
4. Backend returns appropriate response
5. Frontend displays bot response with any special UI elements (tips, celebrations)

## 7. API Endpoints (Backend)

For the hackathon demo, implement these key endpoints:

```
POST /api/auth/login         # User authentication
POST /api/auth/register      # User registration
POST /api/onboarding         # Save onboarding data
GET  /api/user/progress      # Get user progress data
POST /api/chat/message       # Process chat message
```

## 8. Hackathon Implementation Strategy

1. **First Priority**: Implement the Chat interface
   - Core "Sober" and "Drink" modes
   - Basic message exchange functionality

2. **Second Priority**: Implement Authentication
   - Simple login/signup forms
   - Local state for auth during demo

3. **Third Priority**: Implement Home dashboard
   - Basic progress tracking
   - Goal visualization

4. **Last Priority**: Implement Onboarding
   - Simplified survey flow
   - User data collection