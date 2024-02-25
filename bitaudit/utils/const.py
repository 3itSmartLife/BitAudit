MIN_STAKE = 100
PROMPT_TEMPLATE = """
From now on you are the Solidity Smart Contract auditor.
You will be given a smart contract code. Review the given smart contract code and detect the smart contract vulnerabilities if there is any.
All vulnerabilities would be categorized into six classes: "Block Numer Dependency", "Integer Overflow", "Reentrancy", "Dangerous Delegatecall", "Timestamp Dependency", and "Unchecked External Call".
%s
Check the whole code and detect all possible vulnerabilities in it.
Response should include contract names involving vulnerabilities, vulnerability categories they belong, specific function in the contract containing vulnerability, and a detailed reason you detected them as a vulnerability.
Explain the reason in detail.
Return the response in json type with contract names as keys and a list as values whose members are according vulnerability categores, specific function name, reason for detection.
Do not include others in response except the json.
Response:
"""

HUGGINGFACE_REPO_ID = "3it/bitaudit_verification_dataset_v2"
OPENAI_COMPLETIONS_MODEL = "gpt-3.5-turbo"
OPENAI_COMPLETIONS_MAX_TOKENS = 4096
OPENAI_COMPLETIONS_TEMPERATURE = 0
OPENAI_COMPLETIONS_API_KEY = ""

REFACTOR_MODEL="gpt-3.5-turbo-0125"
REFACTOR_TEMPERATURE = 0.5
REFACTOR_RATE = 0.3
REFACTOR_PROMPT="""
You will be given a Solidity smart contract code.
Rewrite the following codes with different variable names and function names.
Follow the coding convention and keep the main functionality.
Return the result in JSON format. Keys are "new_codes" and "refactor_table".
The value for the key "new_codes" should be modified code and the value for the key "refactor_table" should be refactoring table in a dict format.
"""

VULNERABILITY_CATEGORY = ["block number dependency",
                            "dangerous delegatecall",
                            "integer overflow",
                            "reentrancy vulnerability",
                            "timestamp dependency",
                            "unchecked external call"]

VALIDATION_SUBSET = ['benchmark1', 'benchmark2']