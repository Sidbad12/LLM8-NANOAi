
# LLM8 - Medical AI Assistant 

LLM8 is an edge-optimized medical assistant designed to provide reliable, real-time medical Q&A and knowledge retrieval — even on low-power hardware like the NVIDIA Jetson Nano.
It’s built for researchers, healthcare developers, and AI engineers who want to explore medical large language models (LLMs) in constrained environments.

The system combines a fine-tuned DistilGPT2 model (specialized in cardiac medical knowledge) with a Flask-based web interface, enabling users to interact through any browser without requiring heavy desktop GUIs.

## Overview
LLM8 is an intelligent, edge-deployable conversational system built to deliver accurate, domain-specific medical insights—with a particular focus on cardiac health and general medical knowledge. It integrates a fine-tuned DistilGPT2 model alongside a heart attack–specialized language model, providing precise, medically contextualized responses for users and researchers.

Originally built with a PyQt5 GUI, the project faced library incompatibilities on the Jetson Nano due to Python 3.6 and CUDA version constraints.To overcome these challenges, the system was redesigned into a Flask-based web architecture, ensuring lightweight, platform-independent deployment and compatibility with JetPack 4.6.1 (L4T 32.7.1).

The application features:

- A Flask web server managing API routes and user interactions.
- A responsive frontend (HTML, CSS, and JavaScript) for browser-based communication.
- Persistent chat history stored locally for contextual recall.
- A knowledge manager that dynamically switches between general and specialized knowledge bases for accuracy and reliability.

This architecture enables seamless cross-platform access, efficient edge inference, and scalable integration for future medical AI applications, all while running efficiently on resource-constrained hardware like the Jetson Nano.
## System Architecture


| **Component** | **Description** |
|----------------|-----------------|
| **Flask Web Server (`web_app.py`)** | Hosts the backend and serves the browser-based UI. |
| **API Routes (`api/routes.py`)** | Defines endpoints for chat interaction, model loading, and data persistence. |
| **Frontend (HTML + CSS + JS)** | Responsive interface located in `templates/` and `static/`. |
| **Knowledge Manager (`knowledge_manager.py`)** | Loads structured medical knowledge bases for reference responses. |
| **Model Manager (`model_manager.py`)** | Handles model registration, switching, and validation. |
| **Heart Attack Specialist (`heart_attack_specialist.py`)** | Provides domain-specific cardiac responses. |
| **Chat History (`chat_history.json`)** | Stores Q&A context locally for conversation continuity. |

## Project Structure
```bash
LLM8_Jetson/
│
├── app/
│   ├── __init__.py
│   ├── README.md
│   ├── requirements_nano.txt
│   ├── chat_history.json
│   ├── knowledge_registry.json
│   ├── model_registry.json
│   ├── basic_model.py
│   ├── data_manager.py
│   ├── heart_attack_knowledge.py
│   ├── heart_attack_specialist.py
│   ├── knowledge_manager.py
│   ├── learn.py
│   ├── main.py
│   ├── model_manager.py
│   ├── model_manager_dialog.py
│   ├── validate_models.py
│   ├── verified_medical_knowledge.py
│   ├── web_app.py
│   ├── webb_app.py
│   ├── test_gui.py
│   ├── testt.py
│   ├── testtt.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   ├── models/
│   │   ├── heart_attack_specialized_complete/
│   │   │   ├── heart_attack_knowledge.py
│   │   │   ├── README.md
│   │   │   └── model/
│   │   │       ├── config.json
│   │   │       ├── generation_config.json
│   │   │       ├── merges.txt
│   │   │       ├── pytorch_model.bin
│   │   │       ├── special_tokens_map.json
│   │   │       ├── tokenizer_config.json
│   │   │       └── vocab.json
│   │   │
│   │   └── medical_distilgpt2_complete/
│   │       └── model/
│   │           ├── config.json
│   │           ├── generation_config.json
│   │           ├── merges.txt
│   │           ├── model.safetensors
│   │           ├── special_tokens_map.json
│   │           ├── tokenizer_config.json
│   │           └── vocab.json
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   ├── templates/
│   │   └── index.html
│   └── __pycache__/
└── deploy_to_nano.ps1
```
## Environment Setup

### Windows Development Environment


#### Clone the repository and navigate to the app folder

```bash
git clone https://github.com/Sidbad12/LLM8_Jetson.git
cd LLM8_Jetson/app
```
#### Create virtual environment
```bash
python -m venv venv
```
#### Activate virtual environment
```bash
venv\Scripts\activate
```
#### Install required dependencies
```bash
pip install -r requirements_windows.txt\
```
#### Start the Flask application
```bash
python web_app.py
```
#### Access the web interface

Open your browser and go to:
```bash
http://127.0.0.1:5000
```

### Jetson Nano Edge Deployment
#### JetPack 4.6.1 Compatibility
- CUDA: 10.2
- Python: 3.6
- PyTorch: 1.10.0 (latest compatible version)

#### Deployment Steps
- Transfer project files via PowerShell script or scp.
- SSH into the Jetson Nano and install dependencies:
```bash
pip3 install -r requirements_nano.txt
```
- Run the web server:
```bash
python3 web_app.py
```
- Access from another device on the same network:
```bash
http://<jetson-nano-ip>:5000
```


## Jetson Nano Limitations
### Software Constraints

- JetPack Lock-In: JetPack 4.6.1 (L4T 32.7.1) restricts CUDA to version 10.2.
- PyTorch Ceiling: The Nano supports PyTorch up to 1.10.0 only, blocking newer LLMs that require CUDA ≥ 11.x.
- Python Version Lock: System Python is 3.6, limiting compatibility with modern tokenizers and models (e.g., FLAN-T5, DeepSeek).

### Hardware Constraints
- Memory: 4 GB shared RAM/VRAM cannot host models larger than ~500M parameters.
- GPU: The 128-core Maxwell GPU lacks Tensor Cores and modern optimizations, resulting in slower inference.
- Mitigation: Optimized DistilGPT2 and domain-specific models ensure acceptable latency.
## Migration: PyQt5 to Flask



| **Challenge**        | **Root Cause**                                       | **Resolution**                             |
|----------------------|------------------------------------------------------|--------------------------------------------|
| Dependency Conflicts | PyQt5 GUI packages incompatible with Jetson’s Python 3.6 | Replaced with Flask and Jinja2 web interface |
| CUDA / PyYAML Issues | GUI dependencies clashed with JetPack libraries      | Transitioned to a pure web backend         |
| Limited Performance  | GUI overhead on constrained hardware                 | Flask web server minimizes system load     |

### Advantages
- Browser-based interaction with no local GUI dependencies
- Compatible with any platform (Windows, Linux, Jetson Nano)
- Clean, extensible backend structure
- Lightweight and suitable for embedded inference

## **Models and Knowledge Bases**

### **Heart Attack Specialized Model**
- Fine-tuned version of **DistilGPT2-Nano**, optimized for cardiac Q&A, symptom detection, and emergency response.  
- Designed for real-time, low-latency inference on edge hardware (**Jetson Nano**).

### **DistilGPT2 Medical Model**
- General medical dialogue model with integrated fallback knowledge and conversational persistence.  
- Provides broad medical coverage beyond cardiac-specific contexts.

### **Knowledge Bases**
- **heart_attack_knowledge.py** – Curated data for heart-related emergencies and treatment guidance.  
- **create_comprehensive_knowledge_base.py** – Broader medical knowledge compilation for general health reasoning.

---

## **Training Data and Knowledge Sources**

### **1. Core Fine-Tuning Datasets**

| **Dataset** | **Description** | **Purpose** |
|--------------|-----------------|--------------|
| **MedAlpaca** | Derived from Stanford Alpaca, specialized for medical dialogues. | Doctor–patient interactions, symptom and treatment reasoning. |
| **MediQA** | Benchmark dataset by NLM. | Medical Q&A and clinical reasoning. |
| **Medical Meadow** | Community-curated clinical Q&A set. | Diagnostic decisions and symptom correlation. |

These datasets collectively enabled contextual awareness and improved clinical response generation.

---

### **2. Knowledge Base Integration**

| **Source** | **Focus Area** | **Use** |
|-------------|----------------|----------|
| **Mayo Clinic** | Clinical and patient guidance | Symptom–treatment mapping and emergency procedures. |
| **World Health Organization (WHO)** | Preventive and epidemiological data | Risk factor analysis and lifestyle recommendations. |
| **American Heart Association (AHA)** | Emergency and procedural standards | CPR and treatment priority logic. |

---

### **3. Data Verification**

All data sources were:
- Cross-checked with **PubMed** and **NIH Medline** abstracts.  
- Validated using **UMLS** medical terminology standards.  
- Reviewed for factual consistency and safety compliance.

---

### **4. Summary**

| **Layer** | **Source** | **Purpose** | **Verified By** |
|------------|-------------|--------------|-----------------|
| **Core Model** | MedAlpaca, MediQA, Medical Meadow | Fine-tuning medical dialogue | NLM, Stanford |
| **Knowledge Base** | Mayo Clinic, WHO, AHA | Clinical accuracy and emergency logic | Human & Institutional Review |
| **Cross-check** | PubMed, UMLS | Medical consistency | NIH Verified |

---

### **Outcome**
The fine-tuned model accurately identifies and explains cardiac symptoms, prioritizes emergencies like myocardial infarction, and provides reliable medical guidance while maintaining efficiency for real-time use.

## Features

- Browser-based conversational interface
- Model validation and registry management
- Local persistence of chat and knowledge data
- Cross-platform deployment
- Optimized for resource-constrained edge devices

## Testing
To validate functionality:
```bash
pytest
```

## Future Enhancements
- Integration with speech-to-text and text-to-speech modules
- REST API for external integration
- Support for Jetson Orin and Xavier series
- Edge TPU or TensorRT acceleration for faster inference

## License


This project is licensed under the **MIT License**.  

**You are free to:**

- Use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software  
- Include this software in your personal, educational, or commercial projects  

**Conditions:**  

- Include the original copyright and license notice in all copies or substantial portions of the Software.  
- The software is provided “as-is”, without any warranty of any kind.

For more details, see [LICENSE](./LICENSE) file in the repository.

---


## Resources & References
- **NVIDIA Jetson Nano Developer Kit** – [Official Documentation](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)  
- **JetPack SDK & L4T** – [Download and Installation Guide](https://developer.nvidia.com/embedded/jetpack)  
- **PyTorch for Jetson** – [Prebuilt Wheels & Installation Instructions](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)  
- **Transformers Library Documentation** – [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)  
- **Flask Web Framework** – [Official Flask Documentation](https://flask.palletsprojects.com/)  
- **DistilGPT2 Model** – [Hugging Face Model Hub](https://huggingface.co/distilgpt2)

> These resources were used for model development, deployment setup, and reference implementation.