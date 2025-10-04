import json
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chat_data")
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_chat_history(self, history, session_id=None):
        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = os.path.join(self.data_dir, f"chat_{session_id}.json")
        try:
            with open(filename, 'w') as f:
                json.dump(history, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
    
    def load_chat_histories(self):
        histories = []
        try:
            for file in os.listdir(self.data_dir):
                if file.startswith('chat_') and file.endswith('.json'):
                    with open(os.path.join(self.data_dir, file), 'r') as f:
                        histories.append({
                            'filename': file,
                            'data': json.load(f),
                            'timestamp': file.replace('chat_', '').replace('.json', '')
                        })
        except Exception as e:
            print(f"Error loading chat histories: {e}")
        return histories
    
    def get_chat_data_dir(self):
        return self.data_dir