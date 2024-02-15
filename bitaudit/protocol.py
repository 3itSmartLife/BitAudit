# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 <3itSmartLife>

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

import typing
import bittensor as bt


class Audit(bt.Synapse):
    """
    This protocol helps in handling audit request and response communication between
    the miner and the validator.

    Attributes:
    - smart_contract_input: An string representing the input request sent by the validator.
    - vulnerability_output: A string value which, when filled, represents the response from the miner.
    """

    # Required request input, filled by sending dendrite caller.
    smart_contract_input: str = ''

    # Optional request output, filled by recieving axon.
    vulnerability_output: typing.Dict = {}

    # execution_time: typing.Optional[float] = None

    # TODO: Should redefine return value
    def deserialize(self) -> dict:
        """
        Deserialize the output. This method retrieves the response from
        the miner in the form of vulnerability_output, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - dict: The deserialized response, which in this case is the value of vulnerability_output.
        - float: Query execution time.

        Example:
        Assuming a Audit instance has a vulnerability_output value of 5:
        >>> audit_instance = Audit(smart_contract_input="...")
        >>> audit_instance.vulnerability_output = {
                "DutchExchangeProxy": "Dangerous Delegatecall",
                "Proxied": "Integer Overflow"
            }
        >>> audit_instance.deserialize()
        """
        return self.vulnerability_output, self.dendrite.process_time
