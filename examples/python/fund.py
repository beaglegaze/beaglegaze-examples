import os
import json
from web3 import Web3

contract_address = "0x289B72CEeaB48832261626D62E3daA87Fd90B024"
private_key = "0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
CONTRACTS_DIR = "contracts/"
ABI_FILE = os.path.join(CONTRACTS_DIR, "UsageContract.abi")
BIN_FILE = os.path.join(CONTRACTS_DIR, "UsageContract.bin")
SOL_FILE = os.path.join(CONTRACTS_DIR, "UsageContract.sol")

# connect to local hardhat ethereum node
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# load th contract
with open(ABI_FILE, 'r') as f:
    abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=abi)

# import client account with private key
client_account = w3.eth.account.from_key(private_key)

# fund the smart contract by sending eth to it
tx_hash = contract.functions.fund().build_transaction({
    'from': client_account.address,
    'nonce': w3.eth.get_transaction_count(client_account.address),
    'value': w3.to_wei(0.1, 'ether')  # Fund with 0.1 ETH
})
signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=client_account.key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)