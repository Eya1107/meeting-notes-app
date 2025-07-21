# ai/generator.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LocalAIGenerator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

    def generate_summary(self, fields):
        prompt = (
            f"Summarize the following meeting: {fields['project']} with {fields['participants']}. "
            f"Actions: {fields['actions']}. "
            f"Decisions: {fields['decisions']}. "
            f"Remarks: {fields['remarks']}."
        )
        return self._generate(prompt)

    def generate_email(self, fields):
        prompt = (
            f"Write a professional follow-up email based on this meeting: "
            f"{fields['project']} with {fields['participants']}. "
            f"Actions: {fields['actions']}. "
            f"Decisions: {fields['decisions']}. "
            f"Remarks: {fields['remarks']}."
        )
        return self._generate(prompt)

    def _generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            no_repeat_ngram_size=3
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
