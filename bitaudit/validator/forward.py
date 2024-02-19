# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 3itSmartLife

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import bittensor as bt
import time

from bitaudit.protocol import Audit
from bitaudit.validator.reward import get_rewards
from bitaudit.validator.dataset import lowercase_dict, generate_labels, generate_random_path
from bitaudit.validator.refactor import refactor_codes
from bitaudit.utils.uids import get_random_uids

def read_contract_code(file_path):
    # Read the contract code file in local
    with open(file_path, 'rt', encoding='utf8') as f:
        contract_code = f.readlines()

    # Filter out empty lines
    contract_code = [line for line in contract_code if line.strip()!='']
    
    return ''.join(contract_code)

async def forward(self):
    """
    The forward function is called by the validator every time step.

    It is responsible for querying the network and scoring the responses.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

    """
    # Check if it's time to query miners
    if self.step % self.config.neuron.query_steps > 0:
        return

    try:
        smart_contract_path, file_no = generate_random_path(self.config.neuron.dataset_path)
        smart_contract = read_contract_code(smart_contract_path)
        label = generate_labels(self.config.neuron.dataset_path, file_no)
    except Exception as e:
        bt.logging.error("Error loading smart contract code randomly from the dataset")
        bt.logging.error(e)
        return

    try:
        bt.logging.debug("Refactoring smart contract ...")
        result = refactor_codes(smart_contract)
        new_smart_contract = result['new_codes']
        refactor_table = result['refactor_table']
        if refactor_table != {}:
            new_label = {refactor_table[key]:label[key] for key in label.keys()}
            bt.logging.debug("Refactored Label: %s"%str(new_label))
            label = new_label
            smart_contract = new_smart_contract
    except Exception as e:
        bt.logging.warning("Failed to refactor the code, returning the original one.")


    available_axon_count = len(self.metagraph.axons) - 1 #Exclude itself

    # Selects available miners randomly
    miner_selection_size = min(available_axon_count, self.config.neuron.sample_size)
    miner_uids = get_random_uids(self, k=miner_selection_size)

    # The dendrite client queries the network.
    if miner_selection_size == 0:
        bt.logging.info("No available miners at the moment.")
        return

    bt.logging.info('Querying %d random miners at step %d'%(miner_selection_size, self.step))
    bt.logging.info('Recommended Response: %s'%str(label))

    try:
        start_time = time.time()
        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],

            # Construct a Vulnerability query. This simply contains a single string.
            synapse=Audit(smart_contract_input=smart_contract),

            # All responses have the deserialize function called on them before returning.
            # You are encouraged to define your own deserialization function.
            # deserialize=True,
            timeout=self.config.neuron.timeout,
        )

        exec_time = time.time() - start_time
        bt.logging.info("Execution time: %s" % str(exec_time))

        # Extract audit results
        audit_results = [elem[0] for elem in responses]
        execute_times = [elem[1] for elem in responses]

        try:
            # Extract unique elements from the responses
            if not responses:
                bt.logging.info("Null or empty responses received, exiting function")
                return
        except:
            return

        # Log the results for monitoring purposes.
        bt.logging.info(f"Received responses: {str(audit_results)}")

    except Exception as e:
        bt.logging.error("Error handling queries from miner's side: %str" % str(e))

    try:
        # Preprocess the json data
        label = lowercase_dict(label)
        audit_results = [lowercase_dict(result) for result in audit_results]

        # Score miners based on responses from miners.
        rewards = get_rewards(self, label=label, responses=audit_results, response_times=execute_times)

        bt.logging.info(f"Scored responses: {rewards}")
        bt.logging.info(f"Corresponding uids: {miner_uids}")
        # Update the scores based on the rewards. You may want to define your own update_scores function for custom behavior.
        self.update_scores(rewards, miner_uids)
    except Exception as e:
        bt.logging.error("Error scoring miners: %s"%e)