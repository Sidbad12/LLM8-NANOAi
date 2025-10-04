# app/verified_medical_knowledge.py (updated with Mayo Clinic info)

import os
import json
from typing import Dict, Optional

class VerifiedMedicalKnowledgeSystem:
    def __init__(self):
        self.medical_knowledge = {}
        self.initialize_verified_knowledge()
        
    def initialize_verified_knowledge(self):
        """Initialize with empty knowledge base - to be populated with verified sources"""
        self.medical_knowledge = {}
        
    def load_verified_knowledge(self, file_path: str):
        """Load knowledge from a verified source file"""
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    verified_data = json.load(f)
                    self.medical_knowledge.update(verified_data)
            elif file_path.endswith('.txt'):
                # Load from text file with question|answer format
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '|' in line:
                            parts = line.strip().split('|', 1)
                            if len(parts) == 2:
                                self.medical_knowledge[parts[0].lower()] = parts[1]
            print(f"Loaded verified knowledge from {file_path}")
        except Exception as e:
            print(f"Error loading verified knowledge: {e}")
    
    def add_verified_fact(self, question: str, answer: str, source: str):
        """Add a single verified fact with source attribution"""
        verified_answer = f"{answer}\n\n[Source: {source}]"
        self.medical_knowledge[question.lower()] = verified_answer
    
    def get_response(self, question: str) -> Optional[str]:
        """Get a response from verified knowledge base"""
        question_lower = question.lower()
        
        # Exact match
        if question_lower in self.medical_knowledge:
            return self.medical_knowledge[question_lower]
        
        # Partial match
        for key, value in self.medical_knowledge.items():
            if key in question_lower:
                return value
        
        return None

# Create a pre-configured heart attack knowledge system with verified sources
class VerifiedHeartAttackKnowledgeSystem(VerifiedMedicalKnowledgeSystem):
    def __init__(self):
        super().__init__()
        self.initialize_heart_attack_knowledge()
        self.initialize_who_cardiovascular_knowledge()
        self.initialize_mayo_clinic_knowledge()
    
    def initialize_heart_attack_knowledge(self):
        """Initialize with verified heart attack information from authoritative sources"""
        
        # Heart attack symptoms (from CDC/NHS/WHO)
        self.add_verified_fact(
            "heart attack symptoms",
            "Common heart attack symptoms include: chest pain or discomfort, upper body discomfort, shortness of breath, cold sweat, nausea, lightheadedness. Women may experience atypical symptoms like fatigue, indigestion, or anxiety.",
            "CDC: Centers for Disease Control and Prevention"
        )
        
        # Emergency response (from American Heart Association)
        self.add_verified_fact(
            "heart attack emergency what to do",
            "If you suspect a heart attack: 1. Call emergency services immediately 2. Chew and swallow aspirin if not allergic 3. Stay calm and rest 4. Loosen tight clothing 5. Do not drive yourself to the hospital",
            "American Heart Association"
        )
        
        # Prevention (from WHO)
        self.add_verified_fact(
            "prevent heart attack",
            "Heart attack prevention strategies: quit smoking, exercise regularly, eat a heart-healthy diet, maintain healthy weight, control blood pressure and cholesterol, manage diabetes, reduce stress, limit alcohol consumption.",
            "World Health Organization"
        )
    
    def initialize_who_cardiovascular_knowledge(self):
        """Initialize with WHO cardiovascular disease information"""
        
        # Key facts about cardiovascular diseases
        self.add_verified_fact(
            "cardiovascular diseases facts",
            "Cardiovascular diseases (CVDs) are the leading cause of death globally. " +
            "An estimated 19.8 million people died from CVDs in 2022, representing approximately 32% of all global deaths. " +
            "Of these deaths, 85% were due to heart attack and stroke. " +
            "Over three quarters of CVD deaths take place in low- and middle-income countries.",
            "World Health Organization, 2025"
        )
        
        # Types of cardiovascular diseases
        self.add_verified_fact(
            "types of cardiovascular diseases",
            "Cardiovascular diseases include: " +
            "1. Coronary heart disease - disease of blood vessels supplying the heart muscle. " +
            "2. Cerebrovascular disease - disease of blood vessels supplying the brain. " +
            "3. Peripheral arterial disease - disease of blood vessels supplying arms and legs. " +
            "4. Rheumatic heart disease - damage to heart from rheumatic fever. " +
            "5. Congenital heart disease - birth defects affecting heart structure. " +
            "6. Deep vein thrombosis and pulmonary embolism - blood clots in leg veins.",
            "World Health Organization"
        )
        
        # Risk factors
        self.add_verified_fact(
            "cardiovascular disease risk factors",
            "Behavioral risk factors: unhealthy diet, physical inactivity, tobacco use, harmful alcohol use. " +
            "Environmental risk factors: air pollution. " +
            "These may lead to raised blood pressure, blood glucose, blood lipids, and overweight/obesity. " +
            "Underlying determinants include globalization, urbanization, population aging, poverty, stress, and hereditary factors.",
            "World Health Organization"
        )
        
        # Heart attack symptoms (detailed from WHO)
        self.add_verified_fact(
            "heart attack symptoms who",
            "Symptoms of a heart attack include: " +
            "1. Pain or discomfort in the centre of the chest. " +
            "2. Pain or discomfort in the arms, left shoulder, elbows, jaw, or back. " +
            "Additional symptoms: difficulty breathing, nausea, vomiting, light-headedness, cold sweat, pale appearance. " +
            "Women are more likely to have shortness of breath, nausea, vomiting, and back or jaw pain.",
            "World Health Organization"
        )
        
        # Stroke symptoms
        self.add_verified_fact(
            "stroke symptoms",
            "Stroke symptoms include: " +
            "1. Sudden weakness of face, arm, or leg (often on one side). " +
            "2. Numbness of face, arm, or leg. " +
            "3. Confusion, difficulty speaking or understanding. " +
            "4. Difficulty seeing with one or both eyes. " +
            "5. Difficulty walking, dizziness, loss of balance. " +
            "6. Severe headache with no known cause. " +
            "7. Fainting or unconsciousness.",
            "World Health Organization"
        )
        
        # Prevention strategies
        self.add_verified_fact(
            "prevent cardiovascular diseases",
            "Prevention strategies: " +
            "1. Cessation of tobacco use. " +
            "2. Reduction of salt in diet. " +
            "3. Eating more fruits and vegetables. " +
            "4. Regular physical activity. " +
            "5. Avoiding harmful use of alcohol. " +
            "6. Drug treatment of hypertension, diabetes, and high blood lipids. " +
            "7. Health policies creating conducive environments for healthy choices.",
            "World Health Organization"
        )
        
        # Global impact
        self.add_verified_fact(
            "cardiovascular diseases global impact",
            "Approximately 80% of CVD deaths occur in low- and middle-income countries. " +
            "People in these countries often lack access to early detection and treatment. " +
            "CVDs contribute to poverty due to catastrophic health spending. " +
            "CVDs place a heavy burden on economies of low- and middle-income countries.",
            "World Health Organization"
        )
        
        # Treatment and management
        self.add_verified_fact(
            "cardiovascular disease treatment",
            "Essential medicines for CVDs include: " +
            "1. Aspirin " +
            "2. Beta-blockers " +
            "3. Calcium channel blockers " +
            "4. Angiotensin-converting enzyme inhibitors " +
            "5. Diuretics " +
            "6. Statins " +
            "Surgical operations may include coronary artery bypass, balloon angioplasty, valve repair/replacement, heart transplantation.",
            "World Health Organization"
        )
        
        # Rheumatic heart disease
        self.add_verified_fact(
            "rheumatic heart disease",
            "Rheumatic heart disease is caused by damage to heart valves and muscle from rheumatic fever. " +
            "Symptoms include: shortness of breath, fatigue, irregular heartbeats, chest pain, fainting. " +
            "Rheumatic fever symptoms: fever, pain and swelling of joints, nausea, stomach cramps, vomiting. " +
            "Globally, about 2% of CVD deaths are related to rheumatic heart disease.",
            "World Health Organization"
        )
        
        # WHO response and initiatives
        self.add_verified_fact(
            "who cardiovascular disease initiatives",
            "WHO initiatives for CVD prevention and control: " +
            "1. Evidence-based guidelines and tools " +
            "2. Norms and standards for cardiovascular risk assessment " +
            "3. Global HEARTS Initiative to strengthen CVD prevention " +
            "4. Global action plan to reduce premature NCD deaths by 25% by 2025 " +
            "5. Targets to reduce raised blood pressure and increase drug therapy access",
            "World Health Organization"
        )
    
    def initialize_mayo_clinic_knowledge(self):
        """Initialize with Mayo Clinic heart attack information"""
        
        # Heart attack overview
        self.add_verified_fact(
            "what is a heart attack",
            "A heart attack (myocardial infarction) occurs when the flow of blood to the heart is severely reduced or blocked. " +
            "The blockage is usually due to a buildup of fat, cholesterol and other substances in the coronary arteries called plaques. " +
            "The process of plaque buildup is called atherosclerosis. Sometimes, a plaque can rupture and form a clot that blocks blood flow, " +
            "which can damage or destroy part of the heart muscle.",
            "Mayo Clinic"
        )
        
        # Detailed symptoms
        self.add_verified_fact(
            "detailed heart attack symptoms",
            "Symptoms of a heart attack vary: " +
            "1. Chest pain that may feel like pressure, tightness, pain, squeezing or aching. " +
            "2. Pain or discomfort that spreads to the shoulder, arm, back, neck, jaw, teeth or sometimes the upper belly. " +
            "3. Cold sweat, fatigue, heartburn or indigestion. " +
            "4. Lightheadedness or sudden dizziness, nausea, shortness of breath. " +
            "Women may have atypical symptoms such as brief or sharp pain felt in the neck, arm or back. " +
            "Sometimes, the first symptom sign of a heart attack is sudden cardiac arrest.",
            "Mayo Clinic"
        )
        
        # Emergency response details
        self.add_verified_fact(
            "heart attack emergency response detailed",
            "If you think you're having a heart attack: " +
            "1. Call for emergency medical help immediately (911 or local emergency number). " +
            "2. Take nitroglycerin, if prescribed by a healthcare provider. " +
            "3. Take aspirin if recommended, but only if emergency personnel say to do so. " +
            "4. If someone is unconscious, call emergency services first, then check breathing and pulse. " +
            "5. If no breathing or pulse, begin CPR (100-120 chest compressions per minute).",
            "Mayo Clinic"
        )
        
        # Causes and types
        self.add_verified_fact(
            "heart attack causes types",
            "Coronary artery disease causes most heart attacks. Types include: " +
            "1. ST elevation myocardial infarction (STEMI) - acute complete blockage of a medium or large heart artery. " +
            "2. Non-ST elevation myocardial infarction (NSTEMI) - partial blockage. " +
            "Other causes: Coronary artery spasm, certain infections (like COVID-19), spontaneous coronary artery dissection (SCAD).",
            "Mayo Clinic"
        )
        
        # Risk factors
        self.add_verified_fact(
            "heart attack risk factors detailed",
            "Heart attack risk factors include: " +
            "1. Age: Men 45+, Women 55+. " +
            "2. Tobacco use (smoking and secondhand smoke exposure). " +
            "3. High blood pressure, high cholesterol or triglycerides. " +
            "4. Obesity, diabetes, metabolic syndrome. " +
            "5. Family history of heart attacks. " +
            "6. Lack of exercise, unhealthy diet. " +
            "7. Stress, illegal drug use (cocaine, amphetamines). " +
            "8. History of preeclampsia, autoimmune conditions.",
            "Mayo Clinic"
        )
        
        # Complications
        self.add_verified_fact(
            "heart attack complications",
            "Potential complications of a heart attack: " +
            "1. Irregular heart rhythms (arrhythmias). " +
            "2. Cardiogenic shock (heart suddenly unable to pump blood). " +
            "3. Heart failure (temporary or chronic). " +
            "4. Inflammation of the sac surrounding the heart (pericarditis). " +
            "5. Cardiac arrest (sudden stopping of the heart).",
            "Mayo Clinic"
        )
        
        # Prevention strategies
        self.add_verified_fact(
            "heart attack prevention detailed",
            "Prevention strategies: " +
            "1. Follow a healthy lifestyle: Don't smoke, maintain healthy weight, heart-healthy diet, regular exercise, manage stress. " +
            "2. Manage other health conditions: High blood pressure, diabetes. " +
            "3. Take medications as directed. " +
            "4. Learn CPR and how to use an automated external defibrillator (AED).",
            "Mayo Clinic"
        )
        
        # Secondhand smoke
        self.add_verified_fact(
            "secondhand smoke heart attack risk",
            "Yes, secondhand smoke increases heart attack risk. " +
            "Secondhand smoke makes platelets sticky, increasing clotting risk. " +
            "It causes endothelial dysfunction (arteries unable to widen) and inflammation. " +
            "Heart attack rates decrease in areas with smoke-free laws. " +
            "To avoid secondhand smoke: Choose smoke-free places, avoid areas with smoking, ask smokers to smoke outside.",
            "Mayo Clinic"
        )
        
        # Calcium supplements
        self.add_verified_fact(
            "calcium supplements heart attack risk",
            "Some evidence suggests calcium supplements may increase heart attack risk, " +
            "particularly in people with diabetes and healthy postmenopausal women. " +
            "More research is needed. Calcium from food sources (dairy, leafy greens) is not a concern. " +
            "Consult your healthcare professional about whether calcium supplements are right for you.",
            "Mayo Clinic"
        )

# Create a separate WHO-specific knowledge system
class WHOCardiovascularKnowledgeSystem(VerifiedMedicalKnowledgeSystem):
    def __init__(self):
        super().__init__()
        self.initialize_who_cardiovascular_knowledge()
    
    def initialize_who_cardiovascular_knowledge(self):
        """Initialize with comprehensive WHO cardiovascular disease information"""
        # Add all the WHO facts from above
        # (This would contain all the facts from the VerifiedHeartAttackKnowledgeSystem's WHO section)
        pass