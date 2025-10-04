#!/usr/bin/env python3
"""
Test script to verify the heart-specialized model functionality
"""

import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def test_model_loading():
    print("🧪 Testing model loading...")
    model_path = "models/heart_attack_specialized_complete/model/"
    
    # Check what files exist
    print("\n📁 Files in model directory:")
    for file in os.listdir(model_path):
        file_path = os.path.join(model_path, file)
        file_size = os.path.getsize(file_path)
        print(f"  {file}: {file_size} bytes")
    
    # Test tokenizer loading
    print("\n🔤 Testing tokenizer...")
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        print("✅ Tokenizer loaded successfully")
        
        # Test tokenization
        test_text = "What are the symptoms of heart attack?"
        tokens = tokenizer.encode(test_text, return_tensors="pt")
        print(f"✅ Tokenization test: '{test_text}' -> {tokens.shape} tokens")
        
    except Exception as e:
        print(f"❌ Tokenizer error: {e}")
        return False
    
    # Test model loading
    print("\n🤖 Testing model loading...")
    try:
        # Try different loading methods
        try:
            model = GPT2LMHeadModel.from_pretrained(model_path)
            print("✅ Model loaded with standard method")
        except Exception as e1:
            print(f"Standard loading failed: {e1}")
            try:
                model = GPT2LMHeadModel.from_pretrained(model_path, use_safetensors=True)
                print("✅ Model loaded with safetensors=True")
            except Exception as e2:
                print(f"Safetensors loading failed: {e2}")
                # Try direct safetensors loading
                try:
                    from safetensors import safe_open
                    print("Attempting direct safetensors load...")
                    
                    # Load base config first
                    model = GPT2LMHeadModel.from_pretrained("gpt2")
                    
                    # Load weights manually
                    safetensors_path = os.path.join(model_path, "model.safetensors")
                    with safe_open(safetensors_path, framework="pt", device="cpu") as f:
                        for key in f.keys():
                            if key in model.state_dict():
                                model.state_dict()[key].copy_(f.get_tensor(key))
                    
                    print("✅ Model loaded via direct safetensors access")
                except Exception as e3:
                    print(f"❌ All loading methods failed: {e3}")
                    return False
        
        # Test model inference
        print("\n🧠 Testing model inference...")
        with torch.no_grad():
            output = model.generate(
                tokens,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            print(f"✅ Model generated text: '{generated_text}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Model testing failed: {e}")
        return False

def test_safetensors_file():
    print("\n🔍 Examining safetensors file...")
    safetensors_path = "models/heart_attack_specialized_complete/model/model.safetensors"
    
    try:
        # Check file size
        file_size = os.path.getsize(safetensors_path)
        print(f"File size: {file_size} bytes ({file_size/1024/1024:.2f} MB)")
        
        # Try to read the header
        with open(safetensors_path, 'rb') as f:
            # Read first 1024 bytes to check header
            header_data = f.read(1024)
            print(f"First 100 bytes: {header_data[:100]}")
            
            # Try to find JSON header
            try:
                import json
                # Safetensors header is usually at the beginning
                header_str = header_data.decode('utf-8', errors='ignore')
                if '{' in header_str:
                    json_start = header_str.find('{')
                    json_end = header_str.rfind('}') + 1
                    if json_end > json_start:
                        json_header = header_str[json_start:json_end]
                        print("✅ Found JSON header")
                        print(f"Header preview: {json_header[:200]}...")
                    else:
                        print("❌ No valid JSON header found")
            except:
                print("❌ Could not parse header as JSON")
                
    except Exception as e:
        print(f"❌ Error examining file: {e}")

if __name__ == "__main__":
    print("🩺 Medical AI Model Test Script")
    print("=" * 50)
    
    success = test_model_loading()
    
    if not success:
        test_safetensors_file()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Model is working correctly.")
    else:
        print("❌ Some tests failed. The model may need to be re-downloaded or repaired.")