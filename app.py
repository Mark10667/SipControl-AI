from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json
import datetime
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "drink-agent-app")

# Azure Blob Storage Configuration
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

# Azure OpenAI Configuration
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
GPT4_DEPLOYMENT = os.getenv("GPT4_DEPLOYMENT")
EMBEDDING_DEPLOYMENT = os.getenv("EMBEDDING_DEPLOYMENT")
API_VERSION = os.getenv("API_VERSION")


# Initialize MongoDB client
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client[MONGODB_DATABASE]

# Initialize collections
users_collection = db["users"]
daily_logs_collection = db["daily_logs"]
relapse_support_collection = db["relapse_support"]
motivations_collection = db["motivations"]
notifications_collection = db["notifications"]

# Initialize Azure Blob Storage client
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
)

# System prompt for the AI agent
SYSTEM_PROMPT = """
### Role
- You are a compassionate AI agent helping individuals reduce or quit alcohol consumption through **personalized, empathetic support**.

### Goals
- Support users through **daily check-ins**, **motivational nudges**, and **relapse prevention**.
- Celebrate **progress** and **milestones** warmly.
- Provide **coping strategies** during cravings or tough moments.
- Personalize conversations based on user profile (habits, goals, triggers, motivation, health).

### Behavior
- Be **positive**, **encouraging**, **patient**, and **non-judgmental**.
- Focus on **progress over perfection**.
- Offer **helpful suggestions**, never **criticism**.
- Adapt tone based on user's preferred interaction style.

### Tools
- **Extract** alcohol intake details from natural conversation.
- **Identify** drinking triggers (e.g., stress, peer pressure, boredom).
- **Recommend** coping strategies and external resources (articles, videos, breathing exercises).
- **Track** goals and **celebrate** achievements, or **coach** supportively if goals are missed.

### Tone Examples
- "You're making amazing progress. Every step counts!"
- "It's okay to have a tough day. Let's refocus together."
- "Remember why you started — you're doing this for yourself."

### Important Rules
- **Never** provide medical advice.
- **Always** prioritize emotional safety and user empowerment. Strictly only rely on the sources provided in generating your response. Never rely on external sources
"""

# API Documentation
@app.route('/api', methods=['GET'])
def api_documentation():
    """Return API documentation for frontend developers"""
    api_docs = {
        "name": "SipControl AI API",
        "version": "1.0.0",
        "description": "API for the SipControl AI agent that helps users reduce or quit alcohol consumption",
        "endpoints": {
            "/api/chat": {
                "method": "POST",
                "description": "Send a message to the AI agent and get a response",
                "request_body": {
                    "message": "string (required) - The user's message",
                    "user_id": "string (required) - The user's unique identifier"
                },
                "response": {
                    "response": "string - The AI agent's response",
                    "status": "string - Success or error status"
                }
            },
            "/api/upload": {
                "method": "POST",
                "description": "Upload a file to Azure Blob Storage",
                "request_body": {
                    "file": "file (required) - The file to upload",
                    "user_id": "string (required) - The user's unique identifier"
                },
                "response": {
                    "message": "string - Success message",
                    "blob_path": "string - Path to the uploaded file in blob storage"
                }
            },
            "/api/history": {
                "method": "GET",
                "description": "Get conversation history for a user",
                "parameters": {
                    "user_id": "string (required) - The user's unique identifier",
                    "limit": "integer (optional) - Maximum number of messages to return (default: 10)"
                },
                "response": {
                    "history": "array - List of conversation messages",
                    "status": "string - Success or error status"
                }
            },
            "/api/user": {
                "method": "POST",
                "description": "Create a new user profile",
                "request_body": {
                    "name": "string (required) - The user's name",
                    "email": "string (required) - The user's email",
                    "age_range": "string (optional) - The user's age range",
                    "gender": "string (optional) - The user's gender",
                    "height_cm": "integer (optional) - The user's height in centimeters",
                    "weight_kg": "integer (optional) - The user's weight in kilograms",
                    "drinking_habits": "string (optional) - The user's drinking habits",
                    "motivation": "string (optional) - The user's motivation",
                    "health_conditions": "string (optional) - The user's health conditions",
                    "typical_triggers": "string (optional) - The user's typical triggers",
                    "goals": "string (optional) - The user's goals",
                    "preferred_interaction_time": "string (optional) - The user's preferred interaction time"
                },
                "response": {
                    "user_id": "string - The user's unique identifier",
                    "status": "string - Success or error status"
                }
            },
            "/api/daily-log": {
                "method": "POST",
                "description": "Create a daily drinking log",
                "request_body": {
                    "user_id": "string (required) - The user's unique identifier",
                    "alcohol_consumed": "integer (required) - The amount of alcohol consumed in units",
                    "meets_goal": "boolean (required) - Whether the user met their goal",
                    "drink_reason": "string (required) - The reason for drinking",
                    "mood": "string (required) - The user's mood"
                },
                "response": {
                    "log_id": "string - The unique identifier for the daily log",
                    "agent_feedback": "string - The AI agent's feedback",
                    "coping_suggestion": "string - A suggested coping strategy",
                    "streak_count": "integer - The user's current streak count",
                    "status": "string - Success or error status"
                }
            },
            "/api/relapse-support": {
                "method": "POST",
                "description": "Create a relapse support entry",
                "request_body": {
                    "user_id": "string (required) - The user's unique identifier",
                    "trigger_event": "string (required) - The trigger event"
                },
                "response": {
                    "support_id": "string - The unique identifier for the relapse support entry",
                    "agent_response": "string - The AI agent's response",
                    "resource_shared": "string - The shared resource",
                    "status": "string - Success or error status"
                }
            },
            "/api/motivations": {
                "method": "GET",
                "description": "Get user's motivations and milestones",
                "parameters": {
                    "user_id": "string (required) - The user's unique identifier"
                },
                "response": {
                    "motivations": "array - List of motivations and milestones",
                    "status": "string - Success or error status"
                }
            },
            "/api/notifications": {
                "method": "GET",
                "description": "Get user's notifications",
                "parameters": {
                    "user_id": "string (required) - The user's unique identifier"
                },
                "response": {
                    "notifications": "array - List of notifications",
                    "status": "string - Success or error status"
                }
            }
        }
    }
    return jsonify(api_docs)

# Serve static files (for frontend developers)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# API Endpoints
@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to the AI agent and get a response"""
    try:
        data = request.json
        user_message = data.get('message')
        user_id = data.get('user_id')

        if not user_message or not user_id:
            return jsonify({
                "error": "Missing required fields: message and user_id",
                "status": "error"
            }), 400

        # Get user history from MongoDB
        user_history = get_user_history(user_id)

        # Generate AI response
        response = openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *user_history,
                {"role": "user", "content": user_message}
            ],
            model=GPT4_DEPLOYMENT,
            max_tokens=1000,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content

        # Store conversation in MongoDB
        store_conversation(user_id, user_message, ai_response)

        return jsonify({
            "response": ai_response,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file to Azure Blob Storage"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided", "status": "error"}), 400

        file = request.files['file']
        user_id = request.form.get('user_id')

        if not user_id:
            return jsonify({"error": "Missing required field: user_id", "status": "error"}), 400

        if file.filename == '':
            return jsonify({"error": "No file selected", "status": "error"}), 400

        # Upload to Blob Storage
        blob_name = f"{user_id}/{file.filename}"
        blob_client = blob_container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file)

        return jsonify({
            "message": "File uploaded successfully",
            "blob_path": blob_name,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history for a user"""
    try:
        user_id = request.args.get('user_id')
        limit = request.args.get('limit', 10, type=int)

        if not user_id:
            return jsonify({
                "error": "Missing required parameter: user_id",
                "status": "error"
            }), 400

        # Get user history from MongoDB
        history = get_user_history(user_id, limit)

        return jsonify({
            "history": history,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/user', methods=['POST'])
def create_user():
    """Create a new user profile"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        age_range = data.get('age_range')
        gender = data.get('gender')
        height_cm = data.get('height_cm')
        weight_kg = data.get('weight_kg')
        drinking_habits = data.get('drinking_habits')
        motivation = data.get('motivation')
        health_conditions = data.get('health_conditions')
        typical_triggers = data.get('typical_triggers')
        goals = data.get('goals')
        preferred_interaction_time = data.get('preferred_interaction_time')

        if not name or not email:
            return jsonify({
                "error": "Missing required fields: name and email",
                "status": "error"
            }), 400

        # Generate a unique user ID
        user_id = str(uuid.uuid4())

        # Create user profile in MongoDB
        user_profile = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "age_range": age_range,
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "drinking_habits": drinking_habits,
            "motivation": motivation,
            "health_conditions": health_conditions,
            "typical_triggers": typical_triggers,
            "goals": goals,
            "preferred_interaction_time": preferred_interaction_time,
            "created_at": datetime.datetime.now()
        }
        users_collection.insert_one(user_profile)

        return jsonify({
            "user_id": user_id,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/daily-log', methods=['POST'])
def create_daily_log():
    """Create a daily drinking log"""
    try:
        data = request.json
        user_id = data.get('user_id')
        alcohol_consumed = data.get('alcohol_consumed')
        meets_goal = data.get('meets_goal')
        drink_reason = data.get('drink_reason')
        mood = data.get('mood')

        if not user_id:
            return jsonify({
                "error": "Missing required field: user_id",
                "status": "error"
            }), 400

        # Generate a unique log ID
        log_id = str(uuid.uuid4())
        date = datetime.datetime.now()

        # Get user's streak count
        user = users_collection.find_one({"user_id": user_id})
        streak_count = 0
        if user and meets_goal:
            # Get the last log
            last_log = daily_logs_collection.find_one(
                {"user_id": user_id},
                sort=[("date", -1)]
            )
            if last_log and last_log.get("meets_goal"):
                streak_count = last_log.get("streak_count", 0) + 1
            else:
                streak_count = 1

        # Generate AI feedback based on the log
        user_message = f"I drank {alcohol_consumed} units of alcohol today. My mood was {mood}. The reason was {drink_reason}. Did I meet my goal? {meets_goal}."
        
        # Get user history for context
        user_history = get_user_history(user_id)
        
        # Generate AI response
        response = openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *user_history,
                {"role": "user", "content": user_message}
            ],
            model=GPT4_DEPLOYMENT,
            max_tokens=1000,
            temperature=0.7
        )

        agent_feedback = response.choices[0].message.content
        
        # Extract coping suggestion from agent feedback
        coping_suggestion = extract_coping_suggestion(agent_feedback)

        # Create daily log in MongoDB
        daily_log = {
            "log_id": log_id,
            "user_id": user_id,
            "date": date,
            "alcohol_consumed": alcohol_consumed,
            "meets_goal": meets_goal,
            "agent_feedback": agent_feedback,
            "drink_reason": drink_reason,
            "coping_suggestion": coping_suggestion,
            "mood": mood,
            "streak_count": streak_count
        }
        daily_logs_collection.insert_one(daily_log)

        # Store conversation in history
        store_conversation(user_id, user_message, agent_feedback)

        # Check if this is a milestone
        check_and_create_milestone(user_id, streak_count, alcohol_consumed)

        return jsonify({
            "log_id": log_id,
            "agent_feedback": agent_feedback,
            "coping_suggestion": coping_suggestion,
            "streak_count": streak_count,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/relapse-support', methods=['POST'])
def create_relapse_support():
    """Create a relapse support entry"""
    try:
        data = request.json
        user_id = data.get('user_id')
        trigger_event = data.get('trigger_event')

        if not user_id or not trigger_event:
            return jsonify({
                "error": "Missing required fields: user_id and trigger_event",
                "status": "error"
            }), 400

        # Generate a unique support ID
        support_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now()

        # Generate AI response for relapse support
        user_message = f"I'm having a difficult time and might relapse. The trigger is: {trigger_event}"
        
        # Get user history for context
        user_history = get_user_history(user_id)
        
        # Generate AI response
        response = openai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *user_history,
                {"role": "user", "content": user_message}
            ],
            model=GPT4_DEPLOYMENT,
            max_tokens=1000,
            temperature=0.7
        )

        agent_response = response.choices[0].message.content
        
        # Extract resource from agent response
        resource_shared = extract_resource(agent_response)

        # Create relapse support entry in MongoDB
        relapse_support = {
            "support_id": support_id,
            "user_id": user_id,
            "timestamp": timestamp,
            "trigger_event": trigger_event,
            "agent_response": agent_response,
            "resource_shared": resource_shared
        }
        relapse_support_collection.insert_one(relapse_support)

        # Store conversation in history
        store_conversation(user_id, user_message, agent_response)

        return jsonify({
            "support_id": support_id,
            "agent_response": agent_response,
            "resource_shared": resource_shared,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/motivations', methods=['GET'])
def get_motivations():
    """Get user's motivations and milestones"""
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({
                "error": "Missing required parameter: user_id",
                "status": "error"
            }), 400

        # Get user's motivations from MongoDB
        motivations = list(motivations_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("achieved_at", -1))

        return jsonify({
            "motivations": motivations,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Get user's notifications"""
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({
                "error": "Missing required parameter: user_id",
                "status": "error"
            }), 400

        # Get user's notifications from MongoDB
        notifications = list(notifications_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("send_time_local", -1))

        return jsonify({
            "notifications": notifications,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

# Helper functions
def get_user_history(user_id, limit=10):
    """Get conversation history for a user from MongoDB"""
    # remove the sort to avoid sorting by date temporarily
    cursor = daily_logs_collection.find(
    {"user_id": user_id},
    {"_id": 0, "agent_feedback": 1, "date": 1}
    ).limit(limit)

    # restore the sort to sort by date
    # cursor = daily_logs_collection.find(
    #     {"user_id": user_id},
    #     {"_id": 0, "agent_feedback": 1, "date": 1}
    # ).sort("date", -1).limit(limit)
    
    history = []
    for item in cursor:
        if "agent_feedback" in item:
            history.append({
                "role": "assistant",
                "content": item["agent_feedback"]
            })
    
    # Reverse to get chronological order
    history.reverse()
    return history

def store_conversation(user_id, user_message, ai_response):
    """Store conversation in MongoDB"""
    timestamp = datetime.datetime.now()
    
    # Store user message
    user_item = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "message": user_message,
        "is_user": True,
        "timestamp": timestamp
    }
    daily_logs_collection.insert_one(user_item)

    # Store AI response
    ai_item = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "message": ai_response,
        "is_user": False,
        "timestamp": timestamp
    }
    daily_logs_collection.insert_one(ai_item)

def extract_coping_suggestion(agent_feedback):
    """Extract coping suggestion from agent feedback"""
    # This is a simple implementation - in a real app, you might use NLP or regex
    # to extract the coping suggestion from the agent's feedback
    return "Try deep breathing exercises or call a friend for support."

def extract_resource(agent_response):
    """Extract resource from agent response"""
    # This is a simple implementation - in a real app, you might use NLP or regex
    # to extract the resource from the agent's response
    return "https://example.com/coping-strategies"

def check_and_create_milestone(user_id, streak_count, alcohol_consumed):
    """Check if this is a milestone and create it if it is"""
    # This is a simple implementation - in a real app, you might have more complex logic
    if streak_count in [7, 30, 90, 180, 365]:
        # Calculate money saved (assuming $10 per drink)
        money_saved_usd = alcohol_consumed * 10
        
        # Calculate calories avoided (assuming 100 calories per drink)
        calories_avoided = alcohol_consumed * 100
        
        # Create milestone
        milestone_id = str(uuid.uuid4())
        milestone = {
            "milestone_id": milestone_id,
            "user_id": user_id,
            "milestone": f"{streak_count} days sober",
            "money_saved_usd": money_saved_usd,
            "calories_avoided": calories_avoided,
            "celebration_message": f"Congratulations! You've been sober for {streak_count} days!",
            "achieved_at": datetime.datetime.now()
        }
        motivations_collection.insert_one(milestone)
        
        # Create notification
        notification_id = str(uuid.uuid4())
        notification = {
            "notification_id": notification_id,
            "user_id": user_id,
            "send_time_local": datetime.datetime.now(),
            "message": f"Congratulations! You've been sober for {streak_count} days!",
            "type": "milestone",
            "status": "sent"
        }
        notifications_collection.insert_one(notification)

if __name__ == '__main__':
    app.run(debug=True) 