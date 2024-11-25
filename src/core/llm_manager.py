from transformers import AutoModelForCausalLM, AutoTokenizer
from config.settings import API_SETTINGS, MODEL_SETTINGS


class LLMManager:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            API_SETTINGS["model_id"],
            use_fast=True,
            use_auth_token=API_SETTINGS["huggingface_token"]
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            API_SETTINGS["model_id"],
            use_cache=True,
            use_auth_token=API_SETTINGS["huggingface_token"]
        )
        
        # Set padding token if not already set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.tokenizer.pad_token_id

    def generate_content(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        
        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=MODEL_SETTINGS["max_length"],
            num_return_sequences=1,
            temperature=MODEL_SETTINGS["temperature"],
            do_sample=True,  # Key change here
            no_repeat_ngram_size=2,
            use_cache=True
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)