# # llama_model.py
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch
# import ast

# # Use Flan-T5 Small model (public, lightweight, no login needed)
# model_name = "google/flan-t5-base"

# # Load tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(
#     model_name,
#     device_map="cpu",  # Use "auto" if you have GPU
#     torch_dtype=torch.float32
# )

# def process_symptom_text(input_text):
#     prompt = (
#     "You are a medical assistant. Extract only the symptoms from the input text. "
#     "Respond strictly in this format: [\"symptom1\", \"symptom2\"] with no extra text.\n\n"
#     "Example 1:\n"
#     "Input: \"I have a fever and chills.\"\n"
#     "Output: [\"fever\", \"chills\"]\n\n"
#     "Example 2:\n"
#     "Input: \"There’s nausea, vomiting, and chest pain.\"\n"
#     "Output: [\"nausea\", \"vomiting\", \"chest pain\"]\n\n"
#     "Example 3:\n"
#     "Example 3:\n"
#     "Input: \"My stomach has been hurting and I feel dizzy with shortness of breath.\"\n"
#     "Output: [\"stomach pain\", \"dizziness\", \"shortness of breath\"]\n\n"
#     f"Input: \"{input_text}\"\n"
#     f"Output:"
# )

#     # Tokenize and move to model device
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#     # Generate output
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=100,
#         temperature=0.7,
#         do_sample=True
#     )

#     output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     print("Flan-T5 raw output:", output_text)

#     # Try to parse the model's output as a list
#     try:
#         # Try to safely parse as a Python list
#         if output_text.strip().startswith("["):
#             symptom_list = ast.literal_eval(output_text)
#         else:
#             # Otherwise treat it as a single symptom string
#             symptom_list = [output_text.strip().strip('"').strip("'")]
#     except Exception:
#         symptom_list = []

#     # Clean and return
#     return [s.strip().lower() for s in symptom_list if isinstance(s, str) and s.strip()]


# llama_model.py
# llama_model.py


import requests
import ast
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "gemma2-9b-it"

def process_symptom_text(input_text):
    prompt = (
        "You are a medical assistant. Extract only the symptoms from the input text. "
        "Preserve multi-word symptoms (e.g., 'stomach pain', 'shortness of breath'). "
        "Respond strictly as a JSON list of strings with no extra text.\n\n"
        "Example 1:\n"
        "Input: \"I have a fever and chills.\"\n"
        "Output: [\"fever\", \"chills\"]\n\n"
        "Example 2:\n"
        "Input: \"There’s nausea, vomiting, and chest tightness.\"\n"
        "Output: [\"nausea\", \"vomiting\", \"chest tightness\"]\n\n"
        "Example 3:\n"
        "Input: \"My stomach has been hurting and I feel dizzy with shortness of breath.\"\n"
        "Output: [\"stomach pain\", \"dizziness\", \"shortness of breath\"]\n\n"
        f"Input: \"{input_text}\"\n"
        "Output:"
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100,
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)
    response.raise_for_status()

    output_text = response.json()["choices"][0]["message"]["content"]
    print("Groq LLM output:", output_text)

    try:
        if output_text.strip().startswith("["):
            symptom_list = ast.literal_eval(output_text)
        else:
            symptom_list = [output_text.strip().strip('"').strip("'")]
    except Exception:
        symptom_list = []

    return [sym.lower().strip() for sym in symptom_list if isinstance(sym, str) and sym.strip()]

if __name__ == "__main__":
    test_input = "I have stomach pain and shortness of breath."
    symptoms = process_symptom_text(test_input)
    print("Extracted symptoms:", symptoms)
