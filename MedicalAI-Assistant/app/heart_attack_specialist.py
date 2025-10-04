import os
import sys
import torch
import warnings
from typing import Dict, List, Optional

# Add the knowledge_bases directory to the path to import heart_attack_knowledge
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from knowledge_bases.heart_attack_knowledge import HeartAttackKnowledgeSystem
except ImportError:
    # Fallback if the file is moved
    try:
        from heart_attack_knowledge import HeartAttackKnowledgeSystem
    except ImportError:
        # Create a minimal fallback
        class HeartAttackKnowledgeSystem:
            def get_response(self, question):
                return "Knowledge base not available. Please ask about heart attack symptoms, prevention, or emergency response."

class HeartAttackSpecialist:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.knowledge_system = HeartAttackKnowledgeSystem()
        
        # Load model if path provided
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
            
    def load_model(self, model_path):
        """Load model with PyTorch compatibility"""
        try:
            from transformers import GPT2Tokenizer, GPT2LMHeadModel
            
            # Load tokenizer
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            # Load model
            self.model = GPT2LMHeadModel.from_pretrained(model_path)
            
            # Set to evaluation mode
            self.model.eval()
            
            # Handle device assignment
            if hasattr(self.model, 'device'):
                self.device = self.model.device
            else:
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                self.model.to(self.device)
                
            print(f"Heart attack model loaded on {self.device}")
            
        except Exception as e:
            warnings.warn(f"Error loading model: {str(e)}")
            self.model = None
            self.tokenizer = None
            
    def get_response(self, question):
        """Get a response using knowledge base first, then model"""
        # First try the knowledge base
        kb_response = self.knowledge_system.get_response(question)
        if kb_response and not kb_response.startswith("I can provide information"):
            return kb_response
            
        # Fall back to model if available
        if self.model and self.tokenizer:
            return self.generate_with_model(question)
            
        return "Please ask about heart attack symptoms, prevention, or emergency response."
        
    def generate_with_model(self, question, max_length=200):
        """Generate response with model"""
        try:
            input_text = f"### Instruction:\n{question}\n\n### Response:\n"
            
            # Tokenize input
            inputs = self.tokenizer.encode(input_text, return_tensors="pt")
            
            # Move to appropriate device
            inputs = inputs.to(self.device)
                
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if "### Response:" in response:
                response = response.split("### Response:")[-1].strip()
                
            return response
            
        except Exception as e:
            warnings.warn(f"Error generating response: {str(e)}")
            return "Error generating response. Please try again."