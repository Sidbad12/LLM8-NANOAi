#!/usr/bin/env python3
import os
import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel

def test_model_files():
    model_path = "models/heart_attack_specialized_complete/model"
    
    print("Checking model files...")
    
    # Check if files exist
    required_files = ['config.json', 'model.safetensors', 'vocab.json', 'merges.txt', 'tokenizer_config.json']
    for file in required_files:
        file_path = os.path.join(model_path, file)
        if os.path.exists(file_path):
            print(f"✅ {file} exists")
            # Check if file is not empty
            if os.path.getsize(file_path) == 0:
                print(f"❌ {file} is empty!")
            else:
                print(f"✅ {file} has content")
        else:
            print(f"❌ {file} missing!")
    
    # Test loading tokenizer
    try:
        print("\nTesting tokenizer...")
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        print("✅ Tokenizer loaded successfully")
    except Exception as e:
        print(f"❌ Tokenizer error: {e}")
    
    # Test loading model
    try:
        print("\nTesting model...")
        model = GPT2LMHeadModel.from_pretrained(model_path)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Model error: {e}")

if __name__ == "__main__":
    test_model_files()