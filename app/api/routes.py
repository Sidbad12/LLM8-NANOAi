from flask import Blueprint, request, jsonify
import json
from datetime import datetime
import os

api_bp = Blueprint('api', __name__)

# Simple medical knowledge base
MEDICAL_KNOWLEDGE = {
    "heart attack": {
        "symptoms": "Chest pain, shortness of breath, nausea, sweating, arm/jaw pain",
        "treatment": "Call emergency, chew aspirin if not allergic, perform CPR if trained",
        "causes": "Blocked coronary arteries, blood clots, coronary artery spasm"
    },
    "stroke": {
        "symptoms": "Face drooping, arm weakness, speech difficulty, confusion, vision problems",
        "treatment": "Call emergency immediately, note time symptoms started",
        "causes": "Blocked artery (ischemic) or bleeding in brain (hemorrhagic)"
    }
}

@api_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').lower()
        
        # Simple response logic - you can replace with actual model inference
        response = generate_medical_response(message)
        
        # Save to chat history
        save_chat_history(message, response)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/history', methods=['GET'])
def get_history():
    try:
        history = load_chat_history()
        return jsonify({'history': history})
    except:
        return jsonify({'history': []})

def generate_medical_response(message):
    """Generate medical response based on message content"""
    # Check for specific medical terms
    for condition, info in MEDICAL_KNOWLEDGE.items():
        if condition in message:
            if 'symptom' in message:
                return f"Symptoms of {condition}: {info['symptoms']}"
            elif 'treat' in message or 'what to do' in message:
                return f"Treatment for {condition}: {info['treatment']}"
            elif 'cause' in message:
                return f"Causes of {condition}: {info['causes']}"
            else:
                return f"About {condition}: {info['symptoms']}. {info['treatment']}"
    
    # Default response
    return "I can provide information about heart attacks, strokes, and other medical conditions. Please ask specific questions about symptoms, treatment, or causes."

def save_chat_history(question, answer):
    """Save chat history to file"""
    history_file = 'chat_history.json'
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append({
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer
        })
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error saving chat history: {e}")

def load_chat_history():
    """Load chat history from file"""
    history_file = 'chat_history.json'
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return []