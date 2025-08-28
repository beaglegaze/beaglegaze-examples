import json
import os
import subprocess
import time
from web3 import Web3

from beaglegaze-python-sdk.pay_per_call import pay_per_call
from beaglegaze-python-sdk.smart_contract import SmartContract

# --- Configuration ---
HARDHAT_URL = "http://localhost:8545"
CONTRACTS_DIR = "contracts/"
ABI_FILE = os.path.join(CONTRACTS_DIR, "UsageContract.abi")
BIN_FILE = os.path.join(CONTRACTS_DIR, "UsageContract.bin")
SOL_FILE = os.path.join(CONTRACTS_DIR, "UsageContract.sol")

# Private keys from the hardhat testnet
DEVELOPER_PRIVATE_KEY = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
CLIENT_PRIVATE_KEY = "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

# --- Demo Class ---
class MonetizedLibrary:
    """
    A demo class with a method that is monetized using the @pay_per_call decorator.
    """
    @pay_per_call(price=100)
    def important_function(self, *args, **kwargs):
        """
        This function costs 100 wei per call.
        """
        print(f"Executing important_function with args={args} and kwargs={kwargs}")
        return "Success"

def fund_contract(w3, contract_address, client_account):
    print("Funding contract from client account...")
    with open(ABI_FILE, 'r') as f:
        abi = json.load(f)

    contract = w3.eth.contract(address="0x289B72CEeaB48832261626D62E3daA87Fd90B024", abi=abi)

    tx_hash = contract.functions.fund().build_transaction({
        'from': client_account.address,
        'nonce': w3.eth.get_transaction_count(client_account.address),
        'value': w3.to_wei(0.1, 'ether')  # Fund with 0.1 ETH
    })

    signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=client_account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Funding transaction successful. Hash: {receipt.transactionHash.hex()}")

def get_client_funding(w3, contract_address, client_address):
    """Gets the client's funding from the smart contract."""
    with open(ABI_FILE, 'r') as f:
        abi = json.load(f)
    contract = w3.eth.contract(address=contract_address, abi=abi)
    balance = contract.functions.getClientFunding().call({'from': client_address})
    return balance

# --- Main Demo Logic ---
def main():
    """Main function to run the demo."""

    # 2. Connect to Web3
    w3 = Web3(Web3.HTTPProvider(HARDHAT_URL))
    if not w3.is_connected():
        print("Failed to connect to Hardhat node.")
        return

    developer_account = w3.eth.account.from_key(DEVELOPER_PRIVATE_KEY)
    client_account = w3.eth.account.from_key(CLIENT_PRIVATE_KEY)

    # 4. Fund contract
    fund_contract(w3, contract_address, client_account)
    initial_funding = get_client_funding(w3, contract_address, client_account.address)
    print(f"client funding: {w3.from_wei(initial_funding, 'ether')} ETH")

    # 6. Use the monetized library
    lib = MonetizedLibrary()
    print("\n--- Calling monetized function ---")
    for i in range(5):
        print(f"\nCall {i+1}:")
        lib.important_function(i)
        time.sleep(1) # Give some time for events to be processed

    # The batch processor runs in the background. We need to wait for it to process the payments.
    # In a real application, this would happen asynchronously.
    print("\nWaiting for payments to be processed...")
    time.sleep(10)

    # 7. Check final funding
    final_funding = get_client_funding(w3, contract_address, client_account.address)
    print(f"\nFinal client funding: {w3.from_wei(final_funding, 'ether')} ETH")

    expected_cost = 5 * 100 # 5 calls * 100 wei
    funding_difference = initial_funding - final_funding

    print(f"Total cost of calls: {funding_difference} wei")
    print(f"Expected cost of calls: {expected_cost} wei")

    # The actual cost might differ slightly due to the async nature of the library
    # but it should be close to the expected cost.

if __name__ == "__main__":
    main()
