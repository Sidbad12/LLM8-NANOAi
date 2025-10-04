# create_comprehensive_knowledge_base.py
import json
import os

def create_comprehensive_knowledge_base():
    """Create comprehensive knowledge base JSON files including Mayo Clinic info"""
    
    # Create directory if it doesn't exist
    os.makedirs('knowledge_bases/verified', exist_ok=True)
    
    # WHO Cardiovascular Diseases Knowledge
    who_cvd_knowledge = {
        "cardiovascular diseases facts": "Cardiovascular diseases (CVDs) are the leading cause of death globally. An estimated 19.8 million people died from CVDs in 2022, representing approximately 32% of all global deaths. Of these deaths, 85% were due to heart attack and stroke. Over three quarters of CVD deaths take place in low- and middle-income countries. [Source: World Health Organization, 2025]",
        
        "types of cardiovascular diseases": "Cardiovascular diseases include: 1. Coronary heart disease - disease of blood vessels supplying the heart muscle. 2. Cerebrovascular disease - disease of blood vessels supplying the brain. 3. Peripheral arterial disease - disease of blood vessels supplying arms and legs. 4. Rheumatic heart disease - damage to heart from rheumatic fever. 5. Congenital heart disease - birth defects affecting heart structure. 6. Deep vein thrombosis and pulmonary embolism - blood clots in leg veins. [Source: World Health Organization]",
        
        "cardiovascular disease risk factors": "Behavioral risk factors: unhealthy diet, physical inactivity, tobacco use, harmful alcohol use. Environmental risk factors: air pollution. These may lead to raised blood pressure, blood glucose, blood lipids, and overweight/obesity. Underlying determinants include globalization, urbanization, population aging, poverty, stress, and hereditary factors. [Source: World Health Organization]",
        
        "heart attack symptoms who": "Symptoms of a heart attack include: 1. Pain or discomfort in the centre of the chest. 2. Pain or discomfort in the arms, left shoulder, elbows, jaw, or back. Additional symptoms: difficulty breathing, nausea, vomiting, light-headedness, cold sweat, pale appearance. Women are more likely to have shortness of breath, nausea, vomiting, and back or jaw pain. [Source: World Health Organization]",
        
        "stroke symptoms": "Stroke symptoms include: 1. Sudden weakness of face, arm, or leg (often on one side). 2. Numbness of face, arm, or leg. 3. Confusion, difficulty speaking or understanding. 4. Difficulty seeing with one or both eyes. 5. Difficulty walking, dizziness, loss of balance. 6. Severe headache with no known cause. 7. Fainting or unconsciousness. [Source: World Health Organization]",
        
        "prevent cardiovascular diseases": "Prevention strategies: 1. Cessation of tobacco use. 2. Reduction of salt in diet. 3. Eating more fruits and vegetables. 4. Regular physical activity. 5. Avoiding harmful use of alcohol. 6. Drug treatment of hypertension, diabetes, and high blood lipids. 7. Health policies creating conducive environments for healthy choices. [Source: World Health Organization]",
        
        "cardiovascular diseases global impact": "Approximately 80% of CVD deaths occur in low- and middle-income countries. People in these countries often lack access to early detection and treatment. CVDs contribute to poverty due to catastrophic health spending. CVDs place a heavy burden on economies of low- and middle-income countries. [Source: World Health Organization]",
        
        "cardiovascular disease treatment": "Essential medicines for CVDs include: 1. Aspirin 2. Beta-blockers 3. Calcium channel blockers 4. Angiotensin-converting enzyme inhibitors 5. Diuretics 6. Statins. Surgical operations may include coronary artery bypass, balloon angioplasty, valve repair/replacement, heart transplantation. [Source: World Health Organization]",
        
        "rheumatic heart disease": "Rheumatic heart disease is caused by damage to heart valves and muscle from rheumatic fever. Symptoms include: shortness of breath, fatigue, irregular heartbeats, chest pain, fainting. Rheumatic fever symptoms: fever, pain and swelling of joints, nausea, stomach cramps, vomiting. Globally, about 2% of CVD deaths are related to rheumatic heart disease. [Source: World Health Organization]",
        
        "who cardiovascular disease initiatives": "WHO initiatives for CVD prevention and control: 1. Evidence-based guidelines and tools 2. Norms and standards for cardiovascular risk assessment 3. Global HEARTS Initiative to strengthen CVD prevention 4. Global action plan to reduce premature NCD deaths by 25% by 2025 5. Targets to reduce raised blood pressure and increase drug therapy access. [Source: World Health Organization]"
    }
    
    # Mayo Clinic Heart Attack Knowledge
    mayo_clinic_knowledge = {
        "what is a heart attack": "A heart attack (myocardial infarction) occurs when the flow of blood to the heart is severely reduced or blocked. The blockage is usually due to a buildup of fat, cholesterol and other substances in the coronary arteries called plaques. The process of plaque buildup is called atherosclerosis. Sometimes, a plaque can rupture and form a clot that blocks blood flow, which can damage or destroy part of the heart muscle. [Source: Mayo Clinic]",
        
        "detailed heart attack symptoms": "Symptoms of a heart attack vary: 1. Chest pain that may feel like pressure, tightness, pain, squeezing or aching. 2. Pain or discomfort that spreads to the shoulder, arm, back, neck, jaw, teeth or sometimes the upper belly. 3. Cold sweat, fatigue, heartburn or indigestion. 4. Lightheadedness or sudden dizziness, nausea, shortness of breath. Women may have atypical symptoms such as brief or sharp pain felt in the neck, arm or back. Sometimes, the first symptom sign of a heart attack is sudden cardiac arrest. [Source: Mayo Clinic]",
        
        "heart attack emergency response detailed": "If you think you're having a heart attack: 1. Call for emergency medical help immediately (911 or local emergency number). 2. Take nitroglycerin, if prescribed by a healthcare provider. 3. Take aspirin if recommended, but only if emergency personnel say to do so. 4. If someone is unconscious, call emergency services first, then check breathing and pulse. 5. If no breathing or pulse, begin CPR (100-120 chest compressions per minute). [Source: Mayo Clinic]",
        
        "heart attack causes types": "Coronary artery disease causes most heart attacks. Types include: 1. ST elevation myocardial infarction (STEMI) - acute complete blockage of a medium or large heart artery. 2. Non-ST elevation myocardial infarction (NSTEMI) - partial blockage. Other causes: Coronary artery spasm, certain infections (like COVID-19), spontaneous coronary artery dissection (SCAD). [Source: Mayo Clinic]",
        
        "heart attack risk factors detailed": "Heart attack risk factors include: 1. Age: Men 45+, Women 55+. 2. Tobacco use (smoking and secondhand smoke exposure). 3. High blood pressure, high cholesterol or triglycerides. 4. Obesity, diabetes, metabolic syndrome. 5. Family history of heart attacks. 6. Lack of exercise, unhealthy diet. 7. Stress, illegal drug use (cocaine, amphetamines). 8. History of preeclampsia, autoimmune conditions. [Source: Mayo Clinic]",
        
        "heart attack complications": "Potential complications of a heart attack: 1. Irregular heart rhythms (arrhythmias). 2. Cardiogenic shock (heart suddenly unable to pump blood). 3. Heart failure (temporary or chronic). 4. Inflammation of the sac surrounding the heart (pericarditis). 5. Cardiac arrest (sudden stopping of the heart). [Source: Mayo Clinic]",
        
        "heart attack prevention detailed": "Prevention strategies: 1. Follow a healthy lifestyle: Don't smoke, maintain healthy weight, heart-healthy diet, regular exercise, manage stress. 2. Manage other health conditions: High blood pressure, diabetes. 3. Take medications as directed. 4. Learn CPR and how to use an automated external defibrillator (AED). [Source: Mayo Clinic]",
        
        "secondhand smoke heart attack risk": "Yes, secondhand smoke increases heart attack risk. Secondhand smoke makes platelets sticky, increasing clotting risk. It causes endothelial dysfunction (arteries unable to widen) and inflammation. Heart attack rates decrease in areas with smoke-free laws. To avoid secondhand smoke: Choose smoke-free places, avoid areas with smoking, ask smokers to smoke outside. [Source: Mayo Clinic]",
        
        "calcium supplements heart attack risk": "Some evidence suggests calcium supplements may increase heart attack risk, particularly in people with diabetes and healthy postmenopausal women. More research is needed. Calcium from food sources (dairy, leafy greens) is not a concern. Consult your healthcare professional about whether calcium supplements are right for you. [Source: Mayo Clinic]"
    }
    
    # Combined knowledge base
    comprehensive_knowledge = {**who_cvd_knowledge, **mayo_clinic_knowledge}
    
    # Save to JSON files
    with open('knowledge_bases/verified/who_cardiovascular.json', 'w', encoding='utf-8') as f:
        json.dump(who_cvd_knowledge, f, indent=2, ensure_ascii=False)
    
    with open('knowledge_bases/verified/mayo_clinic_heart_attack.json', 'w', encoding='utf-8') as f:
        json.dump(mayo_clinic_knowledge, f, indent=2, ensure_ascii=False)
    
    with open('knowledge_bases/verified/comprehensive_heart_health.json', 'w', encoding='utf-8') as f:
        json.dump(comprehensive_knowledge, f, indent=2, ensure_ascii=False)
    
    print("Comprehensive heart health knowledge base created successfully")

if __name__ == "__main__":
    create_comprehensive_knowledge_base()