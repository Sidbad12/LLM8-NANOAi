import json
import yaml
import os

class KnowledgeBaseManager:
    def __init__(self):
        self.knowledge_bases = {}
        self.registry_path = os.path.join(os.path.dirname(__file__), 'knowledge_registry.json')
        self.load_knowledge_registry()
    
    def load_knowledge_registry(self):
        try:
            if os.path.exists(self.registry_path):
                with open(self.registry_path, 'r') as f:
                    self.knowledge_bases = json.load(f)
            else:
                self.create_default_registry()
        except Exception as e:
            print(f"Error loading knowledge registry: {e}")
            self.create_default_registry()
    
    def create_default_registry(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.knowledge_bases = {
            "Heart Attack Knowledge": {
                "path": os.path.join(base_dir, "knowledge_bases", "heart_attack_knowledge.py"),
                "type": "heart_conditions",
                "loaded": False
            },
            "Comprehensive Medical": {
                "path": os.path.join(base_dir, "knowledge_bases", "create_comprehensive_knowledge_base.py"),
                "type": "general_medical",
                "loaded": False
            }
        }
        self.save_knowledge_registry()
    
    def save_knowledge_registry(self):
        try:
            with open(self.registry_path, 'w') as f:
                json.dump(self.knowledge_bases, f, indent=2)
        except Exception as e:
            print(f"Error saving knowledge registry: {e}")
    
    def add_knowledge_base(self, kb_name, kb_path, kb_type="custom"):
        self.knowledge_bases[kb_name] = {
            "path": kb_path,
            "type": kb_type,
            "loaded": False
        }
        self.save_knowledge_registry()
        return True
    
    def get_knowledge_base_list(self):
        return list(self.knowledge_bases.keys())