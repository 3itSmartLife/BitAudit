from transformers import AutoTokenizer, AutoModelForCausalLM
from bitaudit.utils.const import *
import bittensor as bt
import json
import time
import gc
import torch

class AuditModel:
    def __init__(self, config):
        self.config = config
        
        # Load LLM for smart contract auditing
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.neuron.model_name,
                device_map=self.config.neuron.device
            )
            if not self.tokenizer.eos_token_id:
                self.tokenizer.eos_token_id = self.tokenizer.pad_token_id
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.neuron.model_name,
                device_map=self.config.neuron.device,
                load_in_8bit=self.config.neuron.model.load_in_8bit,
                )
            bt.logging.info("Audit model loaded successfully.")
        except:
            bt.logging.error("Error loading audit model.")

    def audit(self, contract_codes):
        prompt = PROMPT_TEMPLATE%contract_codes
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.config.neuron.device)

        # Check if smart contract code length doesn't exceed the model's max token length
        if len(inputs.input_ids[0]) > self.config.neuron.model.max_token_length - 100:
            bt.logging.warning("Smart Contract code length exceeds the model's max token length")
            return {}

        # Audit the contract code and generate responses
        try:
            generate_ids = self.model.generate(
                inputs.input_ids,
                eos_token_id=self.tokenizer.eos_token_id,
                max_length=self.config.neuron.model.max_token_length,
                temperature=1e-10
                )

            output = self.tokenizer.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
                )[0][len(prompt):]
        except:
            try:
                gc.collect()
                torch.cuda.empty_cache()
            except:
                pass
        try:
            gc.collect()
            torch.cuda.empty_cache()
        except:
            pass


        return json.loads(output)
