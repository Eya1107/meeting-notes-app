# ai_model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Chargement du modèle Flan-T5-Small
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

# Fonction de génération générique
def generate_output(prompt, max_tokens=256):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Résumé de réunion
def generate_summary(fields):
    prompt = f"""
Summarize the following meeting content in a professional and concise way:

Project: {fields.get("Project Name", "")}
Participants: {fields.get("Participants", "")}
Actions: {fields.get("Actions", "")}
Decisions: {fields.get("Decisions", "")}
Remarks: {fields.get("Remarks", "")}

Generate a structured summary suitable for documentation.
"""
    return generate_output(prompt)

# Rédaction d'email
def generate_email(fields):
    prompt = f"""
Write a professional follow-up email based on this meeting information.

Project: {fields.get("Project Name", "")}
Participants: {fields.get("Participants", "")}
Actions to take: {fields.get("Actions", "")}
Decisions made: {fields.get("Decisions", "")}
Remarks and notes: {fields.get("Remarks", "")}
Next meeting details: {fields.get("Next Meeting", "")}
Reminder: {fields.get("Reminder Note", "")}

The tone should be formal and polite. The email should start with a greeting and end with a closing.
"""
    return generate_output(prompt)
