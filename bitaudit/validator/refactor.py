import os
from openai import OpenAI
from bitaudit.utils.const import *
from typing import Optional, Text
import json
import tiktoken
import bittensor as bt
import random

def refactor_codes(code: Text):
    """
    Refactor smart contract code with different variable names, function names, and contract names.
    This method returns a dict involving refactored code and refactoring table.

    Returns:
    - Dict: {'new_codes': refactored_code, 'refactor_table': refactor_matching_table}
    """
    # Get openai default encoder for gpt models
    encoding = tiktoken.get_encoding("cl100k_base")
    # Check whether code length is bigger than max token limit and return original code
    if len(encoding.encode(code)) > (OPENAI_COMPLETIONS_MAX_TOKENS - 200):
        bt.logging.warning("Skipping refactoring as code length exceeds OpenAI max token limit")
        return {'new_codes': code, 'refactor_table': {}}

    # Refactor contract names, variable names, and function names using GPT-3.5
    if random.random() > REFACTOR_RATE:
        try:
            refactor = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            response = refactor.chat.completions.create(
                model=REFACTOR_MODEL,
                temperature=REFACTOR_TEMPERATURE,
                messages=[
                    {'role': 'system', 'content': REFACTOR_PROMPT},
                    {'role': 'user', 'content': code}
                ],
                max_tokens=OPENAI_COMPLETIONS_MAX_TOKENS
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            bt.logging.error("Got an Error: %s"%e)
            return {'new_codes': code, 'refactor_table': {}}
    else:
        return {'new_codes': code, 'refactor_table': {}}