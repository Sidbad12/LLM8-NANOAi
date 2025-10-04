import re
from typing import Dict, List, Optional

class HeartAttackKnowledgeSystem:
    def __init__(self):
        # Comprehensive, pre-verified heart attack knowledge base
        # Reordered to prioritize more specific patterns first
        self.medical_knowledge = {
            "heart_attack_emergency": {
                "response": "EMERGENCY RESPONSE: 1. Call emergency services immediately (108 in India, 911 in US) 2. Chew aspirin (160-325mg) if not allergic 3. Stay calm and rest 4. Loosen tight clothing 5. Do NOT drive to hospital 6. If trained, perform CPR if person is unconscious",
                "keywords": ["emergency", "now", "immediate", "right now", "what should i do", "help", "during a heart attack"]
            },
            "heart_attack_symptoms": {
                "response": "Common symptoms include: chest pain or discomfort, pain in arms/neck/jaw/back, shortness of breath, cold sweat, nausea, lightheadedness. Women may experience atypical symptoms like fatigue, indigestion, or anxiety.",
                "keywords": ["symptoms", "signs", "warning signs", "feel like", "recognize"]
            },
            "heart_attack_prevention": {
                "response": "Prevention strategies: Quit smoking, exercise regularly, eat heart-healthy diet, maintain healthy weight, control blood pressure/cholesterol, manage diabetes, reduce stress, limit alcohol, get regular check-ups.",
                "keywords": ["prevent", "avoid", "reduce risk", "prevention", "healthy lifestyle", "how can i prevent"]
            },
            "heart_attack_causes": {
                "response": "Main causes: Coronary artery disease (plaque buildup), blood clots, coronary artery spasm. Risk factors include smoking, high blood pressure, high cholesterol, diabetes, family history, obesity, and sedentary lifestyle.",
                "keywords": ["causes", "why happen", "reason", "risk factors", "caused by"]
            },
            "heart_attack_treatment": {
                "response": "Treatments include: Medications (clot-busters, blood thinners, pain relievers), angioplasty and stenting, coronary artery bypass surgery, cardiac rehabilitation, and lifestyle changes.",
                "keywords": ["treatment", "cure", "medication", "therapy", "hospital treatment", "how are heart attacks treated", "treated"]
            },
            "heart_attack_recovery": {
                "response": "Recovery typically involves: Cardiac rehabilitation, medication adherence, gradual return to activities, dietary changes, regular follow-ups, and emotional support. Most people return to normal activities in 2 weeks to 3 months.",
                "keywords": ["recovery", "after care", "rehab", "healing", "after hospital", "recovery like", "after a heart attack"]
            },
            "heart_attack_indian_context": {
                "response": "In India: Heart attacks occur 10-15 years earlier than Western populations, high urban prevalence, increasing in younger adults (30-40 years), linked to genetic factors, diabetes, metabolic syndrome, and lifestyle changes.",
                "keywords": ["india", "indian", "asian", "south asian", "genetic", "ethnic"]
            },
            "heart_attack_vs_cardiac_arrest": {
                "response": "Difference: Heart attack = blood flow blockage to heart. Cardiac arrest = heart stops beating. A heart attack can lead to cardiac arrest, but they are different conditions.",
                "keywords": ["difference", "vs", "versus", "compared to", "cardiac arrest"]
            },
            "heart_attack_women": {
                "response": "Women's symptoms may differ: More likely to experience shortness of breath, nausea/vomiting, back/jaw pain, fatigue. Often mistaken for indigestion, anxiety, or flu.",
                "keywords": ["women", "female", "gender differences", "women symptoms"]
            },
            "heart_attack_definition": {
                "response": "A heart attack (myocardial infarction) occurs when blood flow to the heart muscle is blocked, usually by a blood clot. This deprives the heart muscle of oxygen, causing tissue damage or death.",
                "keywords": ["what is", "definition", "mean by"]
            }
        }
        
        self.safety_disclaimer = "\n\n[Disclaimer: This is general medical information. For personal advice, consult a healthcare professional. In emergencies, call local emergency services immediately.]"
        
    def query_knowledge_base(self, user_input: str) -> Optional[str]:
        """Query the knowledge base for relevant heart attack information"""
        user_input = user_input.lower()
        
        # Check each category in order of priority
        for category, data in self.medical_knowledge.items():
            for keyword in data["keywords"]:
                if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                    return data["response"] + self.safety_disclaimer
        
        return None

# Create a helper function for easy integration
def get_heart_attack_response(user_query):
    """Get a response from the heart attack knowledge system"""
    system = HeartAttackKnowledgeSystem()
    return system.query_knowledge_base(user_query)
