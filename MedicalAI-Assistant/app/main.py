import os
import sys
import platform
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, 
                             QWidget, QFrame, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QPalette, QColor
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from model_manager import ModelManager
from knowledge_manager import KnowledgeBaseManager
from data_manager import DataManager
from model_manager_dialog import ModelManagerDialog

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.platform == "win32":
    try:
        # Try to set UTF-8 encoding for Windows terminal
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback for older Python versions
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ---------------- Medical Knowledge Base ----------------
# Add these imports at the top
import importlib.util
import sys

# ---------------- Knowledge Base Integration ----------------
def load_knowledge_base(path):
    """Dynamically load knowledge base from Python file"""
    try:
        spec = importlib.util.spec_from_file_location("knowledge_base", path)
        knowledge_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(knowledge_module)
        return knowledge_module.get_knowledge_base()
    except Exception as e:
        print(f"Error loading knowledge base {path}: {e}")
        return {}

# Replace the MedicalKnowledgeBase class with this simpler version
# ---------------- Medical Knowledge Base ----------------
class MedicalKnowledgeBase:
    def __init__(self):
        # Simple hardcoded knowledge base as fallback
        self.medical_responses = {
            "heart attack": {
                "symptoms": "Common symptoms include: chest pain or discomfort, shortness of breath, pain in arm/neck/jaw, nausea, lightheadedness, cold sweats.",
                "treatment": "Call emergency services immediately. Chew aspirin if not allergic. Perform CPR if trained and person is unresponsive.",
                "causes": "Blocked coronary arteries, blood clots, coronary artery spasm.",
                "prevention": "Healthy diet, regular exercise, no smoking, control blood pressure and cholesterol.",
                "what is": "A heart attack (myocardial infarction) occurs when blood flow to the heart is blocked, preventing oxygen from reaching heart muscle tissue."
            },
            "stroke": {
                "symptoms": "Face drooping, arm weakness, speech difficulty, sudden confusion, vision problems, severe headache.",
                "treatment": "Call emergency immediately. Note time symptoms started. Do not give food or drink.",
                "causes": "Blocked artery (ischemic) or leaking/bursting blood vessel (hemorrhagic).",
                "prevention": "Control blood pressure, healthy diet, exercise, avoid smoking, limit alcohol.",
                "what is": "A stroke occurs when blood supply to part of the brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients."
            }
        }
    
    def get_response(self, topic, aspect=None):
        topic_lower = topic.lower()
        for key in self.medical_responses:
            if key in topic_lower:
                if aspect and aspect in self.medical_responses[key]:
                    return self.medical_responses[key][aspect]
                return self.medical_responses[key].get("what is", "I need more specific information.")
        return None

# ---------------- Dummy Specialist for testing ----------------
class DummyKnowledgeSystem:
    def load_verified_knowledge(self, path):
        print(f"Loading knowledge from: {path}")

class DummyHeartAttackSpecialist:
    def __init__(self):
        self.knowledge_system = DummyKnowledgeSystem()

# ---------------- Main App ----------------
class MedicalAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.heart_attack_specialist = DummyHeartAttackSpecialist()
        self.conversation_history = []
        self.medical_knowledge = MedicalKnowledgeBase()  # This creates an instance
        self.current_model = "Heart-Specific Model"  # Default model
        self.medical_tokenizer = None
        self.medical_model = None
        
        # Initialize managers
        self.model_manager = ModelManager()
        self.kb_manager = KnowledgeBaseManager() 
        self.data_manager = DataManager()
        
        # Check for Jetson environment
        self.is_jetson = self.check_jetson_environment()
        
        # Set dark theme for the entire application
        self.set_dark_theme()
        
        self.setup_ui()
        self.setup_knowledge_bases()
        self.load_medical_model()
        self.set_dark_theme()
        self.setup_ui()
        self.setup_knowledge_bases()
        self.load_medical_model()    
    def check_jetson_environment(self):
        """Check if running on Jetson and optimize accordingly"""
        is_jetson = os.path.exists('/etc/nv_tegra_release')
        
        if is_jetson:
            print("Jetson environment detected - optimizing for hardware constraints")
            
            # Limit model options to only compatible ones
            compatible_models = []
            for model in self.model_manager.get_model_list():
                if self.model_manager.is_model_available(model):
                    compatible_models.append(model)
            
            if compatible_models:
                # Update the current model to first available one
                self.current_model = compatible_models[0]
        return is_jetson
    
    # ... rest of your MedicalAIApp methods ...
        
        
    
    def set_dark_theme(self):
        # Set dark palette for the entire application
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)
    
    # ---------------- UI ----------------
    def setup_ui(self):
        self.setWindowTitle("MedAI Assistant - Clinical Support System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
                border: 1px solid #1e293b;
            }
            QFrame {
                background-color: #1e293b;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        
        # Central widget and layout
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #0f172a;")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header with logo and title
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1e40af, stop: 1 #3b82f6);
                border-radius: 12px;
                border: none;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Title and subtitle
        title_layout = QHBoxLayout()
        
        # Logo placeholder (you can add an actual image here)
        logo_label = QLabel("🩺")
        logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """)
        logo_label.setFixedSize(60, 60)
        
        title_text = QLabel("MedAI Assistant")
        title_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_text)
        title_layout.addStretch()
        
        header_layout.addLayout(title_layout)
        
        # Subtitle
        subtitle = QLabel("AI-Powered Clinical Support System")
        subtitle.setStyleSheet("""
            QLabel {
                color: #e2e8f0;
                font-size: 14px;
                font-weight: medium;
                margin-top: 5px;
            }
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Status and model selection panel
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(15, 10, 15, 10)
        
        # Status indicator
        status_container = QFrame()
        status_container.setStyleSheet("background: transparent;")
        status_layout = QHBoxLayout(status_container)
        
        status_icon = QLabel("●")
        status_icon.setStyleSheet("""
            QLabel {
                color: #4ade80;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        status_text = QLabel("Status:")
        status_text.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-weight: bold;
            }
        """)
        
        self.status_label = QLabel("System Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #4ade80;
                font-weight: medium;
            }
        """)
        
        status_layout.addWidget(status_icon)
        status_layout.addWidget(status_text)
        status_layout.addWidget(self.status_label)
        status_layout.addSpacing(20)
        
        # Model selection
        model_text = QLabel("Model:")
        model_text.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-weight: bold;
            }
        """)
        
        self.model_combo = QComboBox()
        self.model_combo.addItem("Heart-Specific Model")
        self.model_combo.addItem("Medical GPT-2 Model")
        self.model_combo.setStyleSheet("""
            QComboBox {
                background-color: #334155;
                color: #f1f5f9;
                border: 1px solid #475569;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 180px;
            }
            QComboBox:drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #475569;
                border-left-style: solid;
            }
            QComboBox QAbstractItemView {
                background-color: #334155;
                color: #f1f5f9;
                selection-background-color: #3b82f6;
                border: 1px solid #475569;
            }
            QComboBox:hover {
                border: 1px solid #64748b;
            }
        """)
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        
        control_layout.addWidget(status_container)
        control_layout.addStretch()
        control_layout.addWidget(model_text)
        control_layout.addWidget(self.model_combo)
        
        layout.addWidget(control_frame)
        
        # Conversation area
        conv_frame = QFrame()
        conv_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        conv_layout = QVBoxLayout(conv_frame)
        conv_layout.setContentsMargins(0, 0, 0, 0)
        
        # Conversation header
        conv_header = QLabel("Clinical Conversation")
        conv_header.setStyleSheet("""
            QLabel {
                color: #e2e8f0;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 15px;
                background-color: #334155;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom: 1px solid #475569;
            }
        """)
        conv_layout.addWidget(conv_header)
        
        self.conversation_area = QTextEdit()
        self.conversation_area.setReadOnly(True)
        self.conversation_area.setFont(QFont("Segoe UI", 10))
        self.conversation_area.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b; 
                color: #e2e8f0; 
                border: none;
                padding: 15px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
        conv_layout.addWidget(self.conversation_area)
        
        layout.addWidget(conv_frame, 1)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter your medical question or concern...")
        self.input_box.returnPressed.connect(self.on_ask_click)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: #334155; 
                color: #f1f5f9; 
                border: 1px solid #475569; 
                border-radius: 6px;
                padding: 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
                background-color: #374151;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        
        self.ask_button = QPushButton("Send Consultation")
        self.ask_button.clicked.connect(self.on_ask_click)
        self.ask_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2563eb, stop: 1 #3b82f6);
                color: white; 
                border: none; 
                border-radius: 6px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1d4ed8, stop: 1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1e40af, stop: 1 #1d4ed8);
            }
            QPushButton:disabled {
                background-color: #475569;
                color: #94a3b8;
            }
        """)
        
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.ask_button)
        
        layout.addWidget(input_frame)
        
        # Footer with disclaimer
        footer = QLabel("⚠️ This AI assistant provides informational support only. Always consult qualified healthcare professionals for medical diagnosis and treatment.")
        footer.setStyleSheet("""
            QLabel {
                color: #94a3b8;
                font-size: 13px;
                
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
            }
        """)
        footer.setWordWrap(True)
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        # Add initial conversation
        self.add_to_conversation("User", "What are the symptoms of a heart attack?")
        self.add_to_conversation("AI", "Common symptoms include chest pain, shortness of breath, nausea, and sweating.")
        self.add_to_conversation("User", "How should it be treated?")
        self.add_to_conversation("AI", "Immediate response includes calling emergency services and administering CPR if needed...")
    
    def add_to_conversation(self, sender, message):
        if sender == "User":
            formatted_message = f"""
            <div style="margin: 10px 0;">
                <div style="color: #3b82f6; font-weight: bold; margin-bottom: 4px;">Patient:</div>
                <div style="background-color: #334155; padding: 12px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                    {message}
                </div>
            </div>
            """
        elif sender == "AI":
            formatted_message = f"""
            <div style="margin: 10px 0;">
                <div style="color: #10b981; font-weight: bold; margin-bottom: 4px;">MedAI:</div>
                <div style="background-color: #334155; padding: 12px; border-radius: 8px; border-left: 4px solid #10b981;">
                    {message}
                </div>
            </div>
            """
        else:  # System messages
            formatted_message = f"""
            <div style="margin: 10px 0; text-align: center;">
                <span style="color: #94a3b8; font-style: italic; font-size: 11px;">
                    {message}
                </span>
            </div>
            """
        
        self.conversation_area.append(formatted_message)
        self.conversation_area.moveCursor(QTextCursor.End)
        
        # Store in history
        self.conversation_history.append(f"{sender}: {message}")
    
    def on_model_changed(self, model_name):
        self.current_model = model_name
        self.status_label.setText(f"Loading {model_name}...")
        QApplication.processEvents()
        self.load_medical_model()
        
        if model_name == "Medical GPT-2 Model":
            warning = "Switched to Medical GPT-2 Model (General information only - not for specific medical advice)"
            self.add_to_conversation("System", warning)
        else:
            self.add_to_conversation("System", f"Switched to {model_name}")
    
    def on_ask_click(self):
        question = self.input_box.text().strip()
        if question:
            self.add_to_conversation("User", question)
            self.input_box.clear()
            
            # Simulate AI thinking
            self.status_label.setText("Generating response...")
            QApplication.processEvents()  # Update UI
            
            response = self.generate_medical_response(question)
            self.add_to_conversation("AI", response)
            
            if self.medical_model and self.medical_tokenizer:
                self.status_label.setText(f"{self.current_model} Loaded. Ready.")
            else:
                self.status_label.setText("Using Knowledge Base Only")
    
    def add_to_conversation(self, sender, message):
        if sender == "User":
            formatted_message = f"<p><span style='color: #569cd6; font-weight: bold;'>{sender}:</span> {message}</p>"
        elif sender == "AI":
            formatted_message = f"<p><span style='color: #4ec9b0; font-weight: bold;'>{sender}:</span> {message}</p>"
        else:  # System messages
            formatted_message = f"<p><span style='color: #ce9178; font-weight: bold;'>{sender}:</span> {message}</p>"
        
        self.conversation_area.append(formatted_message)
        self.conversation_area.moveCursor(QTextCursor.End)
        
        # Store in history
        self.conversation_history.append(f"{sender}: {message}")
    
    # ---------------- Knowledge Bases ----------------
    def get_knowledge_base_path(self, filename):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if platform.system() == "Windows":
            return os.path.join(base_dir, "knowledge_bases", filename.replace("/", "\\"))
        else:
            return os.path.join(base_dir, "knowledge_bases", filename)
    
    def setup_knowledge_bases(self):
        try:
            for kb_file in [
                "verified/heart_attack_cdc.json",
                "verified/who_cardiovascular.json",
                "verified/mayo_clinic_heart_attack.json",
                "verified/comprehensive_heart_health.json",
                "verified/heart_attack_aha.json"
            ]:
                path = self.get_knowledge_base_path(kb_file)
                if os.path.exists(path):
                    self.heart_attack_specialist.knowledge_system.load_verified_knowledge(path)
            print("All knowledge bases loaded successfully")
        except Exception as e:
            print(f"Error loading verified knowledge bases: {e}")
    
    def show_model_manager(self):
        dialog = ModelManagerDialog(self.model_manager, self)
        dialog.exec_()
        # Reload model if needed
        self.load_medical_model()

    def setup_management_buttons(self):
        # Add this to your setup_ui method where you want the buttons
        management_layout = QHBoxLayout()
        
        model_btn = QPushButton("Manage Models")
        model_btn.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #6d28d9;
            }
        """)
        model_btn.clicked.connect(self.show_model_manager)
        
        management_layout.addWidget(model_btn)
        # Add this layout to your main layout where appropriate
    
    # ---------------- Medical Model ----------------
    def get_medical_model_path(self):
    # First try to get path from model manager
        model_path = self.model_manager.get_model_path(self.current_model)
        if model_path and os.path.exists(model_path):
            return model_path
        
        # Fallback to hardcoded paths if model manager doesn't have it
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.current_model == "Heart-Specific Model":
            return os.path.join(base_dir, "app", "models", "heart_attack_specialized_complete", "model")
        else:  # Medical GPT-2 Model
            return os.path.join(base_dir, "app", "models", "medical_distilgpt2_complete", "model")
    
    def get_safe_medical_response(self, question):
        """Provide safe, general medical information without specific advice"""
        question_lower = question.lower()
        
        # List of safe general responses for common medical questions
        if any(word in question_lower for word in ["pain", "hurt", "ache", "sore"]):
            return "I understand you're experiencing discomfort. For persistent or severe pain, please consult a healthcare professional for proper evaluation. They can provide personalized advice based on your specific situation."
        
        elif any(word in question_lower for word in ["fever", "temperature", "hot"]):
            return "Fever can be a sign of various conditions. It's important to monitor your temperature and symptoms. If your fever is high (>103°F/39.4°C) or persists for more than 3 days, please seek medical attention."
        
        elif any(word in question_lower for word in ["headache", "migraine"]):
            return "Headaches can have many causes. For occasional headaches, rest and hydration may help. If you experience severe, sudden, or persistent headaches, please consult a healthcare provider for proper diagnosis."
        
        elif any(word in question_lower for word in ["cold", "flu", "cough", "sneeze"]):
            return "Respiratory symptoms can indicate various conditions. Rest, hydration, and over-the-counter remedies may help mild symptoms. If symptoms are severe or persist, please consult a healthcare professional."
        
        elif any(word in question_lower for word in ["heart", "chest", "cardiac"]):
            return "Heart-related symptoms should always be evaluated by a healthcare professional. If you're experiencing chest pain, shortness of breath, or other concerning symptoms, please seek immediate medical attention."
        
        elif any(word in question_lower for word in ["back pain", "backache"]):
            return "Back pain can have various causes. For mild cases, rest and gentle stretching may help. If pain is severe, persistent, or accompanied by other symptoms like numbness or weakness, please consult a healthcare provider."
        
        # General response for other medical questions
        elif any(word in question_lower for word in ["what is", "what are", "define", "explain"]):
            return "I can provide general health information, but for specific medical questions, it's important to consult with a healthcare professional who can consider your individual health status and needs."
        
        # Default response for other queries
        return "For medical concerns, it's always best to consult with a qualified healthcare professional who can provide personalized advice based on your specific situation and medical history."

    def load_medical_model(self):
        model_path = self.get_medical_model_path()
        
        # Check if model exists locally
        if not os.path.exists(model_path):
            error_msg = f"Model path does not exist: {model_path}"
            print(error_msg)
            self.status_label.setText("Model not found - using knowledge base only")
            self.medical_tokenizer = None
            self.medical_model = None
            self.add_to_conversation("System", f"Model not found at: {os.path.basename(model_path)}")
            return
        
        try:
            print(f"Loading model from: {model_path}")
            
            # Check if the model directory contains the necessary files
            required_files = ['model.safetensors', 'config.json', 'vocab.json']
            existing_files = os.listdir(model_path)
            missing_files = [f for f in required_files if f not in existing_files]
            
            if missing_files:
                error_msg = f"Model files missing: {missing_files}"
                print(error_msg)
                print(f"Available files: {existing_files}")
                self.status_label.setText("Model files incomplete - using knowledge base")
                self.medical_tokenizer = None
                self.medical_model = None
                self.add_to_conversation("System", f"Model files incomplete. Missing: {', '.join(missing_files)}")
                return
            
            # Load tokenizer and model using locally installed libraries
            print("Loading tokenizer...")
            self.medical_tokenizer = GPT2Tokenizer.from_pretrained(
                model_path,
                padding_side='left'
            )
            print("Tokenizer loaded successfully")
            
            print("Loading model...")
            self.medical_model = GPT2LMHeadModel.from_pretrained(model_path)
            print("Model loaded successfully")
            
            # Add padding token if it doesn't exist
            if self.medical_tokenizer.pad_token is None:
                self.medical_tokenizer.pad_token = self.medical_tokenizer.eos_token
                
            # Set model to evaluation mode
            self.medical_model.eval()
            
            success_msg = f"{self.current_model} loaded successfully"
            print(success_msg)
            self.status_label.setText(f"{self.current_model} Loaded. Ready.")
            self.add_to_conversation("System", f"{self.current_model} loaded from local storage")
            
        except Exception as e:
            error_msg = f"Error loading {self.current_model}: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.status_label.setText("Model load failed - using knowledge base")
            self.medical_tokenizer = None
            self.medical_model = None
            self.add_to_conversation("System", f"Failed to load model: {str(e)}")
    def generate_medical_response(self, question):
        print(f"Generating response for: {question}")
        
        # For Heart-Specific Model, use the normal generation
        if self.current_model == "Heart-Specific Model" and self.medical_model and self.medical_tokenizer:
            try:
                input_text = f"### Instruction:\n{question}\n\n### Response:\n"
                inputs = self.medical_tokenizer.encode(input_text, return_tensors="pt")

                outputs = self.medical_model.generate(
                    inputs,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.medical_tokenizer.eos_token_id,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3
                )

                model_response = self.medical_tokenizer.decode(outputs[0], skip_special_tokens=True)
                model_response = model_response.split("### Response:")[-1].strip()
                
                # If model response is reasonable, use it
                if len(model_response) > 5:
                    return model_response
                    
            except Exception as e:
                print(f"Error generating model response: {e}")
                return "I encountered an error processing your question. Please try again."
        
        # For Medical GPT-2 Model or if heart model fails, use safe fallback
        return self.get_safe_medical_response(question)

    def get_safe_medical_response(self, question):
        """Provide safe, general medical information without specific advice"""
        question_lower = question.lower()
        
        # List of safe general responses for common medical questions
        if any(word in question_lower for word in ["pain", "hurt", "ache", "sore"]):
            return "I understand you're experiencing discomfort. For persistent or severe pain, please consult a healthcare professional for proper evaluation. They can provide personalized advice based on your specific situation."
        
        elif any(word in question_lower for word in ["fever", "temperature", "hot"]):
            return "Fever can be a sign of various conditions. It's important to monitor your temperature and symptoms. If your fever is high (>103°F/39.4°C) or persists for more than 3 days, please seek medical attention."
        
        elif any(word in question_lower for word in ["headache", "migraine"]):
            return "Headaches can have many causes. For occasional headaches, rest and hydration may help. If you experience severe, sudden, or persistent headaches, please consult a healthcare provider for proper diagnosis."
        
        elif any(word in question_lower for word in ["cold", "flu", "cough", "sneeze"]):
            return "Respiratory symptoms can indicate various conditions. Rest, hydration, and over-the-counter remedies may help mild symptoms. If symptoms are severe or persist, please consult a healthcare professional."
        
        elif any(word in question_lower for word in ["heart", "chest", "cardiac"]):
            return "Heart-related symptoms should always be evaluated by a healthcare professional. If you're experiencing chest pain, shortness of breath, or other concerning symptoms, please seek immediate medical attention."
        
        elif any(word in question_lower for word in ["back pain", "backache"]):
            return "Back pain can have various causes. For mild cases, rest and gentle stretching may help. If pain is severe, persistent, or accompanied by other symptoms like numbness or weakness, please consult a healthcare provider."
        
        # Heart-specific knowledge for the heart model fallback
        elif any(word in question_lower for word in ["heart attack", "myocardial"]):
            if "symptom" in question_lower:
                return "Common heart attack symptoms include: chest pain or discomfort, shortness of breath, pain in arm/neck/jaw, nausea, lightheadedness, cold sweats."
            elif "treat" in question_lower or "what to do" in question_lower:
                return "For suspected heart attack: Call emergency services immediately, chew aspirin if not allergic, and perform CPR if trained and the person is unresponsive."
            elif "cause" in question_lower:
                return "Heart attacks are primarily caused by coronary artery disease where arteries become narrowed due to plaque buildup."
            else:
                return "A heart attack occurs when blood flow to the heart muscle is blocked, usually by a blood clot, causing damage to the heart muscle."
        
        # General response for other medical questions
        elif any(word in question_lower for word in ["what is", "what are", "define", "explain"]):
            return "I can provide general health information, but for specific medical questions, it's important to consult with a healthcare professional who can consider your individual health status and needs."
        
        # Default response for other queries
        return "For medical concerns, it's always best to consult with a qualified healthcare professional who can provide personalized advice based on your specific situation and medical history."

    def get_accurate_medical_response(self, question):
        """Provide accurate, verified medical information"""
        question_lower = question.lower()
        
        # Heart attack information
        if any(term in question_lower for term in ["heart attack", "myocardial infarction"]):
            if "symptom" in question_lower:
                return "Heart attack symptoms include: chest pain or discomfort, shortness of breath, pain in arm/neck/jaw, nausea, lightheadedness, cold sweats. Women may experience different symptoms like fatigue, indigestion, or back pain."
            elif "treat" in question_lower or "what to do" in question_lower:
                return "For suspected heart attack: 1. Call emergency services immediately 2. Chew aspirin (if not allergic) 3. Stay calm and rest 4. Perform CPR if trained and person is unresponsive 5. Use AED if available. Time is critical for heart attack treatment."
            elif "cause" in question_lower:
                return "Heart attacks are primarily caused by coronary artery disease where arteries become narrowed due to plaque buildup. Risk factors include smoking, high blood pressure, high cholesterol, diabetes, obesity, and family history."
            elif "prevent" in question_lower:
                return "Prevent heart attacks by: maintaining healthy diet, regular exercise, not smoking, controlling blood pressure/cholesterol, managing diabetes, reducing stress, and regular health check-ups."
            else:
                return "A heart attack (myocardial infarction) occurs when blood flow to the heart muscle is blocked, usually by a blood clot, causing damage to the heart muscle. This is a medical emergency requiring immediate treatment."
        
        # Stroke information
        elif "stroke" in question_lower:
            if "symptom" in question_lower:
                return "Stroke symptoms (remember FAST): Face drooping, Arm weakness, Speech difficulty, Time to call emergency. Other symptoms include sudden numbness, confusion, vision problems, dizziness, severe headache."
            elif "treat" in question_lower:
                return "Stroke treatment depends on type: ischemic strokes may be treated with clot-busting drugs or mechanical thrombectomy; hemorrhagic strokes may require surgery. Immediate medical attention is crucial."
            elif "cause" in question_lower:
                return "Strokes are caused by either blocked arteries (ischemic) or bleeding in the brain (hemorrhagic). Risk factors include high blood pressure, smoking, diabetes, high cholesterol, and atrial fibrillation."
            else:
                return "A stroke occurs when blood supply to part of the brain is interrupted or reduced, preventing brain tissue from getting oxygen and nutrients, causing brain cells to die within minutes."
        
        return None

    def is_medically_relevant(self, response, question):
        """Check if the response is medically relevant and accurate"""
        response_lower = response.lower()
        question_lower = question.lower()
        
        # Check for obvious nonsense
        if len(response) < 10:
            return False
        
        # Check for medically relevant terms based on question
        if "heart" in question_lower and not any(term in response_lower for term in ["heart", "chest", "blood", "attack", "cardiac"]):
            return False
            
        if "stroke" in question_lower and not any(term in response_lower for term in ["brain", "stroke", "blood", "attack", "neurolog"]):
            return False
        
        # Check for obviously wrong information
        wrong_terms = ["trimester", "pregnant", "baby", "9:30", "P.M.", "KJ", "local time"]
        if any(term in response_lower for term in wrong_terms):
            return False
        
        return True

    def is_gibberish(self, text):
        """Check if text appears to be gibberish or irrelevant"""
        # Less strict checking for LLM responses
        if len(text) < 5:  # Reduced from 15 to 5
            return True
            
        # Check for repetitive patterns
        words = text.split()
        if len(words) < 2:  # Reduced from 3 to 2
            return True
            
        # Check for obvious nonsense (like code or random characters)
        if re.search(r'[{}()\[\]<>]', text):  # Code-like characters
            return True
            
        # Allow short but meaningful responses from LLM
        return False
        
    def get_knowledge_based_response(self, question):
        question_lower = question.lower()
        
        # Check for heart-related questions
        heart_terms = ["heart", "cardiac", "chest pain", "myocardial", "attack"]
        if any(term in question_lower for term in heart_terms):
            if "symptom" in question_lower:
                return self.medical_knowledge.get_response("heart attack", "symptoms")
            elif "treat" in question_lower or "how to" in question_lower:
                return self.medical_knowledge.get_response("heart attack", "treatment")
            elif "cause" in question_lower:
                return self.medical_knowledge.get_response("heart attack", "causes")
            elif "prevent" in question_lower:
                return self.medical_knowledge.get_response("heart attack", "prevention")
            else:
                return self.medical_knowledge.get_response("heart attack", "what is")
        
        # Check for stroke-related questions
        if "stroke" in question_lower:
            if "symptom" in question_lower:
                return self.medical_knowledge.get_response("stroke", "symptoms")
            elif "treat" in question_lower or "how to" in question_lower:
                return self.medical_knowledge.get_response("stroke", "treatment")
            elif "cause" in question_lower:
                return self.medical_knowledge.get_response("stroke", "causes")
            elif "prevent" in question_lower:
                return self.medical_knowledge.get_response("stroke", "prevention")
            else:
                return self.medical_knowledge.get_response("stroke", "what is")
        
        return None
        # ---------------- Button Callback ----------------
    def on_ask_click(self):
        question = self.input_box.text().strip()
        if question:
            self.add_to_conversation("User", question)

            self.input_box.clear()
                
                # Simulate AI thinking
            self.status_label.setText("Generating response...")
            QApplication.processEvents()  # Update UI
                
            response = self.generate_medical_response(question)
            self.add_to_conversation("AI", response)
                
            if self.medical_model and self.medical_tokenizer:
                self.status_label.setText(f"{self.current_model} Loaded. Ready.")
            else:
                self.status_label.setText("Using Knowledge Base Only")

# ---------------- Run App ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedicalAIApp()
    window.show()
    sys.exit(app.exec_())