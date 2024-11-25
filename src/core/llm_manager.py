from transformers import AutoModelForCausalLM, AutoTokenizer
from src.config.settings import API_SETTINGS
import torch

class LLMManager:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            API_SETTINGS["model_id"],
            token=API_SETTINGS["huggingface_token"]
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            API_SETTINGS["model_id"],
            token=API_SETTINGS["huggingface_token"]
        )

    def generate_content(self, prompt, max_length=1000):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            no_repeat_ngram_size=2
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)