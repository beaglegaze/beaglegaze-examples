from beaglegaze-python-sdk.batch_mode import BatchMode
from beaglegaze-python-sdk.contract_consumer import ContractConsumer
from beaglegaze-python-sdk.pay_per_call import pay_per_call, set_processor
from beaglegaze-python-sdk.async_batch_processor import AsyncBatchProcessor
from beaglegaze-python-sdk.smart_contract import SmartContract

HARDHAT_URL = "http://localhost:8545"

CONTRACT_ADDRESS = "0x289B72CEeaB48832261626D62E3daA87Fd90B024"

class MonetizedLibrary:
    """
    Initializes the MonetizedLibrary instance.
    """
    def __init__(self, client_account: str = None):
        async_processor = AsyncBatchProcessor(BatchMode.OFF)
        smart_contract = SmartContract(
            CONTRACT_ADDRESS,
            HARDHAT_URL,
            client_account, 
            10
        )
        contract_consumer = ContractConsumer(smart_contract)
        async_processor.add_observer(contract_consumer)
        set_processor(async_processor)

    """
    A demo class with a method that is monetized using the @pay_per_call decorator.
    """
    @pay_per_call(price=1000000, contract_address="0x289B72CEeaB48832261626D62E3daA87Fd90B024", network_url="http://localhost:8545")
    def important_function(self, *args, **kwargs):
        """
        This function costs 1000000 wei per call.
        """
        print(f"Executing important_function with args={args} and kwargs={kwargs}")
        return "Success"
