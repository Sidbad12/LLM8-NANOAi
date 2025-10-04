from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from datetime import datetime
import os
import sys
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import numpy as np


app = Flask(__name__)

# Medical knowledge base as fallback
MEDICAL_KNOWLEDGE = {
    "heart attack": {
        "symptoms": "Chest pain or discomfort, shortness of breath, pain in arm/neck/jaw, nausea, lightheadedness, cold sweats. Women may experience different symptoms like fatigue or back pain.",
        "treatment": "Call emergency services immediately. Chew aspirin if not allergic. Perform CPR if trained. Do not delay treatment.",
        "causes": "Blocked coronary arteries due to plaque buildup, blood clots, coronary artery spasm, or spontaneous coronary artery dissection.",
        "prevention": "Maintain healthy diet, exercise regularly, avoid smoking, control blood pressure and cholesterol, manage stress, get regular checkups.",
        "what is": "A heart attack (myocardial infarction) occurs when blood flow to the heart is blocked, damaging heart muscle tissue. This is a medical emergency requiring immediate treatment."
    },
    "stroke": {
        "symptoms": "Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency. Also sudden numbness, confusion, vision problems, dizziness, severe headache.",
        "treatment": "Call emergency immediately. Note time symptoms started. Ischemic strokes may be treated with clot-busting drugs if given quickly. Do not give food or drink.",
        "causes": "Blocked artery (ischemic stroke) or bleeding in brain (hemorrhagic stroke). Risk factors include high blood pressure, smoking, diabetes, high cholesterol.",
        "prevention": "Control blood pressure, healthy diet, regular exercise, avoid smoking, limit alcohol, manage atrial fibrillation if present.",
        "what is": "A stroke occurs when blood supply to part of the brain is interrupted, preventing brain tissue from getting oxygen and nutrients, causing brain cells to die within minutes."
    }
}

# Initialize model and tokenizer
model = None
tokenizer = None
model_loaded = False

def load_medical_model():
    global model, tokenizer, model_loaded
    
    print("Loading heart-specialized model...")
    model_path = "models/heart_attack_specialized_complete/model/"
    
    try:
        # Load tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        print("Tokenizer loaded successfully")
        
        # Check which model file to use
        bin_path = os.path.join(model_path, "pytorch_model.bin")
        safetensors_path = os.path.join(model_path, "model.safetensors")
        
        if os.path.exists(bin_path):
            print("Using pytorch_model.bin file...")
            model = GPT2LMHeadModel.from_pretrained(model_path)
        elif os.path.exists(safetensors_path):
            print("Using model.safetensors file...")
            try:
                model = GPT2LMHeadModel.from_pretrained(model_path, use_safetensors=True)
            except:
                print("Safetensors corrupted, using base model...")
                model = GPT2LMHeadModel.from_pretrained("gpt2")
        else:
            print("No model files found, downloading base model...")
            model = GPT2LMHeadModel.from_pretrained("gpt2")
            model.save_pretrained(model_path)
        
        model.eval()
        model_loaded = True
        print("✅ Model loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("⚠️ Falling back to base GPT-2 model...")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        model.eval()
        model_loaded = True
        
def fix_json_files(model_path):
    """Check and fix corrupted JSON files in model directory"""
    json_files = ['special_tokens_map.json', 'tokenizer_config.json', 'config.json']
    
    for json_file in json_files:
        file_path = os.path.join(model_path, json_file)
        if os.path.exists(file_path):
            # Check if file is empty or invalid JSON
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        print(f"Warning: {json_file} is empty, recreating...")
                        recreate_json_file(file_path, json_file)
                    else:
                        # Try to parse JSON to check if valid
                        json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: {json_file} is corrupted, recreating...")
                recreate_json_file(file_path, json_file)
            except Exception as e:
                print(f"Error checking {json_file}: {e}")

def recreate_json_file(file_path, json_file):
    """Recreate a JSON file with default content"""
    default_content = {
        'special_tokens_map.json': {
            "bos_token": "<|endoftext|>",
            "eos_token": "<|endoftext|>", 
            "unk_token": "<|endoftext|>"
        },
        'tokenizer_config.json': {
            "add_prefix_space": False,
            "bos_token": "<|endoftext|>",
            "eos_token": "<|endoftext|>",
            "model_max_length": 1024,
            "name_or_path": "distilgpt2",
            "pad_token": "<|endoftext|>",
            "special_tokens_map_file": "special_tokens_map.json",
            "tokenizer_class": "GPT2Tokenizer",
            "unk_token": "<|endoftext|>"
        }
    }
    
    if json_file in default_content:
        with open(file_path, 'w') as f:
            json.dump(default_content[json_file], f, indent=2)
        print(f"Recreated {json_file}")

def generate_medical_response(message):
    """Generate response using model first, knowledge base as fallback"""
    # Try to use the AI model first
    if model_loaded:
        try:
            # Prepare input
            input_text = f"### Medical Question:\n{message}\n\n### Answer:\n"
            inputs = tokenizer.encode(input_text, return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2
                )
            
            # Decode and clean up response
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.split("### Answer:")[-1].strip()
            
            # Validate response
            if response and len(response) > 10:
                return response, "model"
                
        except Exception as e:
            print(f"Model generation error: {e}")
    
    # Fall back to knowledge base
    kb_response = get_knowledge_based_response(message)
    return kb_response, "knowledge_base"

def get_knowledge_based_response(message):
    """Get response from medical knowledge base"""
    message_lower = message.lower()
    
    # Check for specific medical conditions
    for condition, info in MEDICAL_KNOWLEDGE.items():
        if condition in message_lower:
            if any(word in message_lower for word in ['symptom', 'sign', 'feel']):
                return f"Symptoms of {condition}: {info['symptoms']}"
            elif any(word in message_lower for word in ['treat', 'cure', 'what to do', 'how to']):
                return f"Treatment for {condition}: {info['treatment']}"
            elif any(word in message_lower for word in ['cause', 'why', 'reason']):
                return f"Causes of {condition}: {info['causes']}"
            elif any(word in message_lower for word in ['prevent', 'avoid', 'reduce risk']):
                return f"Prevention of {condition}: {info['prevention']}"
            else:
                return f"About {condition}: {info['what is']}"
    
    # General medical response
    return "I specialize in heart-related medical information. You can ask me about symptoms, treatment, causes, or prevention of heart conditions. For other medical concerns, please consult a healthcare professional."

@app.route('/')
def index():
    return render_template('index.html', model_loaded=model_loaded)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Generate response (model first, then knowledge base)
        response, response_source = generate_medical_response(message)
        
        # Save to chat history
        save_chat_history(message, response, response_source)
        
        return jsonify({
            'response': response,
            'source': response_source,
            'model_loaded': model_loaded
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = load_chat_history()
        return jsonify({'history': history})
    except:
        return jsonify({'history': []})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'model_loaded': model_loaded,
        'model_type': 'Heart-Specialized DistilGPT2' if model_loaded else 'None'
    })

def save_chat_history(question, answer, source):
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
            'answer': answer,
            'source': source
        })
        
        # Keep only last 100 messages
        if len(history) > 100:
            history = history[-100:]
        
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

# Add this right before the main block
with app.app_context():
    print("💡 Loading heart-specialized model...")
    load_medical_model()

if __name__ == '__main__':
    print("🚀 Starting Medical AI Assistant Web Server...")
    print("🌐 Server ready at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)