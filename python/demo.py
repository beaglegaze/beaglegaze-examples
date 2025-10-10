import os
import time

from beaglegaze.pay_per_call import pay_per_call, set_processor
from beaglegaze.smart_contract import SmartContract
from beaglegaze.async_batch_processor import AsyncBatchProcessor
from beaglegaze.batch_mode import BatchMode
from beaglegaze.contract_consumer import ContractConsumer

# --- Configuration ---
HARDHAT_URL = "http://localhost:8545"

CLIENT_PRIVATE_KEY = "0xcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"

# --- Demo Class ---
class MonetizedLibrary:
    """
    A demo class with a method that is monetized using the @pay_per_call decorator.
    The MonetizedLibrary sets up its own AsyncBatchProcessor and SmartContract instance.
    """
    def __init__(self, network_url: str, client_private_key: str):
        # Set up the async batch processor
        async_processor = AsyncBatchProcessor(BatchMode.OFF)
        
        # Create smart contract instance
        # the smart contract is deployed by the project maintainer(s)
        # and hardcoded in the library 
        smart_contract = SmartContract(
            "0x289B72CEeaB48832261626D62E3daA87Fd90B024",
            network_url,
            client_private_key,
            10  # batch size
        )
        
        # Create contract consumer and add as observer
        contract_consumer = ContractConsumer(smart_contract)
        async_processor.add_observer(contract_consumer)
        
        # Set the global processor
        set_processor(async_processor)

    @pay_per_call(price=10000)
    def important_function(self, *args, **kwargs):
        """
        This function costs 10000 wei per call.
        """
        print(f"Executing important_function with args={args} and kwargs={kwargs}")
        return "Success"

# --- Main Demo Logic ---
def main():
    """Main function to run the demo."""

    # 6. Use the monetized library
    lib = MonetizedLibrary(HARDHAT_URL, CLIENT_PRIVATE_KEY)
    print("\n--- Calling monetized function ---")
    for i in range(5):
        print(f"\nCall {i+1}:")
        lib.important_function(i)
        time.sleep(1) # Give some time for events to be processed
    print("\n--- Demo complete ---")

if __name__ == "__main__":
    main()
