<div align="center">

# **BitAudit - Blockchain Network Audit Subnet** <!-- omit in toc -->

[![bitAudit](/docs/BitAudit.png)](https://github.com/3itSmartlife/BitAudit/tree/main/docs)
[![Bittensor](/docs/taologo.png)](https://bittensor.com/)

---

[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.gg/bittensor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

---

## Towards A Secure and Resilient Blockchain Network <!-- omit in toc -->

[Discord](https://discord.gg/bittensor) • [Network](https://taostats.io/) • [Research](https://bittensor.com/whitepaper)
</div>

---

## Introduction

> **Note:** The following documentation assumes you are familiar with basic Bittensor concepts: Miners, Validators, and incentives. If you need a primer, please check out https://docs.bittensor.com/learn/bittensor-building-blocks.

The objective of this subnet is to conduct audits on smart contracts, aiming to detect security vulnerabilities, address poor coding practices, and optimize inefficient code through the utilization of artificial intelligence (AI). \
This aims to offer a service that safeguards users against potential financial losses, compromised data, and reputational damage, thereby bolstering the security, reliability, and performance of blockchain networks utilizing Bittensor Ecosystem. \
This will be further extended to audit blockchain networks.\
Additionally, it is the first Bittensor subnet to handle software security using AI.

The mechanism works like this:

    1. Miners audit smart contracts.
    2. Validators continuously evaluate the result from miners, setting weights based on the miner responses against the labelled dataset.
    3. The Bittensor chain aggregates weights from all active validators using Yuma Consensus to determine the proportion of TAO emission rewarded to miners and validators.

## Installation

### Before you proceed
Before you proceed with the installation of the subnet, note the following: 

- Use these instructions to run your subnet locally for your development and testing, or on Bittensor testnet or on Bittensor mainnet. 
- **IMPORTANT**: We **strongly recommend** that you first run your subnet locally and complete your development and testing before running the subnet on Bittensor testnet. Furthermore, make sure that you next run your subnet on Bittensor testnet before running it on the Bittensor mainnet.
- You can run your subnet either as a subnet owner, or as a subnet validator or as a subnet miner. 
- **IMPORTANT:** Make sure you are aware of the minimum compute requirements for your subnet. See the [Minimum compute YAML configuration](./min_compute.yml).
- Note that installation instructions differ based on your situation: For example, installing for local development and testing will require a few additional steps compared to installing for testnet. Similarly, installation instructions differ for a subnet owner vs a validator or a miner. 

### Install
This repository requires python3.8 or higher. To install, simply clone this repository and install the requirements.

#### Bittensor
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/opentensor/bittensor/master/scripts/install.sh)"
```

#### Clone the repository from Github
```bash
git clone https://github.com/3itSmartLife/bitaudit.git
```

#### Install package dependencies for the repository
```bash
cd bitaudit
apt install python3-pip -y
python3 -m pip install -e .
```

#### Install `pm2`
```bash
apt update && apt upgrade -y
apt install nodejs npm -y
npm i -g pm2
```

## Running Miners and Validators on BitAudit
### Running subtensor locally
#### Install Docker
```bash
apt install docker.io -y
apt install docker-compose -y
```

#### Run Subtensor locally
```bash
git clone https://github.com/opentensor/subtensor.git
cd subtensor
docker compose up mainnet-lite
```

### Running miner
Miners audit smart contracts written in Solidity utilizing various LLMs. \
They have the flexibility to implement various AI algorithms for smart contract auditing. Their responses will be validated and be rewarded according to the accuracy. \
Smart contract auditing using CodeLlama from Meta is working currently. 

#### Run the miner with `pm2`
```bash
pm2 start neurons/miners/codellama/miner.py --name miner --interpreter python3 --  
--netuid <your netuid> 
--subtensor.network <your chain url> # the bittensor chain endpoint, running a subtensor locally is highly recommended 
--wallet.name <your miner wallet> 
--wallet.hotkey <your miner hotkey>
--axon.port <an open port to serve the bittensor axon on>
--neuron.model_name <LLM model name on huggingface> # codellama/CodeLlama-13b-Instruct-hf is set as default
--neuron.model.load_in_8bit # if set, the miner will load the model in 8bit mode
--logging.debug # run in debug mode, alternatively --logging.trace for trace mode
```
### Running validator
Validating miners are a crucial part in analyzing the performance of the subnet and incentivize miners for continuous improvement. Validators query miners with prepared validation dataset and validate responses from miners with labels on the validation dataset. \
Currently, validators are designed to use OpenAI API to refactor smart contract code from validation dataset to prevent exploits.
Validators are highly encouraged to use their own validation data to validate miners.

#### Run the validator with `pm2`
```bash
export OPENAI_API_KEY='sk-.....'
pm2 start neurons/validator.py --name validator --interpreter python3 --
--netuid <your netuid>
--subtensor.network <your chain url> # running a subtensor locally is highly recommended
--wallet.name <your validator wallet>
--wallet.hotkey <your validator hotkey>
--axon.port <an open port to serve the bittensor axon on>
--logging.debug # run in debug mode, alternatively --logging.trace for trace mode
--neuron.device cpu # set the device as cpu for validators to run without gpu
```

## License
This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

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
```
