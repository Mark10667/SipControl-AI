# SipControl AI API

This is the backend API for the SipControl AI application, which helps users reduce or quit alcohol consumption through personalized, empathetic support.

## MongoDB Structure

The application uses MongoDB with the following structure:

```
Database: drink-agent-app
|
├── Collection: users               (user profile + survey)
├── Collection: daily_logs           (daily drinking logs + agent feedback)
├── Collection: relapse_support      (emergency coping talks)
├── Collection: motivations          (milestones and celebrations)
├── Collection: notifications        (nudges and reminders)
```

### Collection Schemas

#### users
- user_id (PK)
- name
- email
- age_range
- gender
- height_cm
- weight_kg
- drinking_habits
- motivation
- health_conditions
- typical_triggers
- goals
- preferred_interaction_time
- created_at

#### daily_logs
- log_id (PK)
- user_id (FK)
- date
- alcohol_consumed
- meets_goal
- agent_feedback
- drink_reason
- coping_suggestion
- mood
- streak_count

#### relapse_support
- support_id (PK)
- user_id (FK)
- timestamp
- trigger_event
- agent_response
- resource_shared

#### motivations
- milestone_id (PK)
- user_id (FK)
- milestone
- money_saved_usd
- calories_avoided
- celebration_message
- achieved_at

#### notifications
- notification_id (PK)
- user_id (FK)
- send_time_local
- message
- type
- status

## API Documentation

The API documentation is available at the `/api` endpoint. You can also view it by running the application and visiting `http://localhost:5000/api`.

### Available Endpoints

1. **Create User** - `POST /api/user`
   - Creates a new user profile
   - Request body: `{ "name": "string", "email": "string", "age_range": "string", "gender": "string", "height_cm": "integer", "weight_kg": "integer", "drinking_habits": "string", "motivation": "string", "health_conditions": "string", "typical_triggers": "string", "goals": "string", "preferred_interaction_time": "string" }`
   - Response: `{ "user_id": "string", "status": "success" }`

2. **Create Daily Log** - `POST /api/daily-log`
   - Creates a daily drinking log
   - Request body: `{ "user_id": "string", "alcohol_consumed": "integer", "meets_goal": "boolean", "drink_reason": "string", "mood": "string" }`
   - Response: `{ "log_id": "string", "agent_feedback": "string", "coping_suggestion": "string", "streak_count": "integer", "status": "success" }`

3. **Create Relapse Support** - `POST /api/relapse-support`
   - Creates a relapse support entry
   - Request body: `{ "user_id": "string", "trigger_event": "string" }`
   - Response: `{ "support_id": "string", "agent_response": "string", "resource_shared": "string", "status": "success" }`

4. **Get Motivations** - `GET /api/motivations`
   - Gets user's motivations and milestones
   - Query parameters: `user_id` (required)
   - Response: `{ "motivations": [...], "status": "success" }`

5. **Get Notifications** - `GET /api/notifications`
   - Gets user's notifications
   - Query parameters: `user_id` (required)
   - Response: `{ "notifications": [...], "status": "success" }`

6. **Chat with AI** - `POST /api/chat`
   - Sends a message to the AI agent and gets a response
   - Request body: `{ "message": "string", "user_id": "string" }`
   - Response: `{ "response": "string", "status": "success" }`

7. **Get Chat History** - `GET /api/history`
   - Gets conversation history for a user
   - Query parameters: `user_id` (required), `limit` (optional, default: 10)
   - Response: `{ "history": [...], "status": "success" }`

8. **Upload File** - `POST /api/upload`
   - Uploads a file to Azure Blob Storage
   - Form data: `file` (required), `user_id` (required)
   - Response: `{ "message": "string", "blob_path": "string", "status": "success" }`

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with the following variables:
   ```
   # MongoDB Configuration
   MONGODB_URI=your_mongodb_connection_string
   MONGODB_DATABASE=drink-agent-app

   # Azure Blob Storage Configuration
   BLOB_CONNECTION_STRING=your_blob_connection_string
   BLOB_CONTAINER_NAME=your_blob_container_name

   # Azure OpenAI Configuration
   AZURE_ENDPOINT=your_azure_openai_endpoint
   AZURE_API_KEY=your_azure_openai_key
   GPT4_DEPLOYMENT=your_gpt4_deployment_name
   API_VERSION=2024-02-15-preview
   ```
4. Run the application: `python app.py`
5. Access the API at `http://localhost:5000`

## Frontend Integration

### Example: Creating a User

```javascript
fetch('https://your-api-url/api/user', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    age_range: '30-40',
    gender: 'male',
    height_cm: 180,
    weight_kg: 80,
    drinking_habits: '2-3 drinks per day',
    motivation: 'Improve health',
    health_conditions: 'None',
    typical_triggers: 'Stress, social events',
    goals: 'Reduce to 1 drink per week',
    preferred_interaction_time: 'Evening'
  }),
})
.then(response => response.json())
.then(data => {
  console.log('User ID:', data.user_id);
  // Store the user_id for future requests
})
.catch(error => console.error('Error:', error));
```

### Example: Creating a Daily Log

```javascript
fetch('https://your-api-url/api/daily-log', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: 'user-id-from-previous-step',
    alcohol_consumed: 2,
    meets_goal: true,
    drink_reason: 'Social event',
    mood: 'Happy'
  }),
})
.then(response => response.json())
.then(data => {
  console.log('Log ID:', data.log_id);
  console.log('Agent Feedback:', data.agent_feedback);
  console.log('Coping Suggestion:', data.coping_suggestion);
  console.log('Streak Count:', data.streak_count);
})
.catch(error => console.error('Error:', error));
```

### Example: Creating a Relapse Support Entry

```javascript
fetch('https://your-api-url/api/relapse-support', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: 'user-id-from-previous-step',
    trigger_event: 'Work stress'
  }),
})
.then(response => response.json())
.then(data => {
  console.log('Support ID:', data.support_id);
  console.log('Agent Response:', data.agent_response);
  console.log('Resource Shared:', data.resource_shared);
})
.catch(error => console.error('Error:', error));
```

### Example: Getting Motivations

```javascript
fetch('https://your-api-url/api/motivations?user_id=user-id-from-previous-step')
.then(response => response.json())
.then(data => {
  console.log('Motivations:', data.motivations);
})
.catch(error => console.error('Error:', error));
```

### Example: Getting Notifications

```javascript
fetch('https://your-api-url/api/notifications?user_id=user-id-from-previous-step')
.then(response => response.json())
.then(data => {
  console.log('Notifications:', data.notifications);
})
.catch(error => console.error('Error:', error));
```

### Example: Sending a Message to the AI

```javascript
fetch('https://your-api-url/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: 'user-id-from-previous-step',
    message: 'I want to reduce my alcohol consumption'
  }),
})
.then(response => response.json())
.then(data => {
  console.log('AI Response:', data.response);
})
.catch(error => console.error('Error:', error));
```

### Example: Getting Chat History

```javascript
fetch('https://your-api-url/api/history?user_id=user-id-from-previous-step&limit=10')
.then(response => response.json())
.then(data => {
  console.log('Chat History:', data.history);
})
.catch(error => console.error('Error:', error));
```

### Example: Uploading a File

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('user_id', 'user-id-from-previous-step');

fetch('https://your-api-url/api/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Upload Result:', data);
})
.catch(error => console.error('Error:', error));
```

## Deployment to Azure Web App

The application is configured for deployment to Azure Web App. Follow these steps:

1. Create an Azure Web App
2. Configure the following environment variables in the Azure Web App Configuration:
   - MONGODB_URI
   - MONGODB_DATABASE
   - BLOB_CONNECTION_STRING
   - BLOB_CONTAINER_NAME
   - AZURE_ENDPOINT
   - AZURE_API_KEY
   - GPT4_DEPLOYMENT
   - API_VERSION
3. Deploy the application to Azure Web App using the provided deploy.sh script

## Demo Page

A demo page is available at `http://localhost:5000/static/index.html` when running the application locally. This page demonstrates how to use all the API endpoints. 