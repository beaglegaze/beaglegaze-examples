# 💰 Beaglegaze Python Sample

This Python sample demonstrates how to integrate Beaglegaze's blockchain-powered fee collection into your Python libraries. The example shows a monetized library where function calls automatically trigger micro-payments through a smart contract.

## 📋 What's Included

- `demo.py` - Main demonstration of a monetized library with pay-per-call functionality
- `fund.py` - Script to fund the smart contract with ETH for testing
- `requirements.txt` - Python dependencies (references local beaglegaze-python-sdk)
- `contracts/` - Smart contract ABI and binary files

## 🔧 Prerequisites

1. **Python 3.8+** with pip
2. **Docker** for running the local Ethereum testnet
3. **Git** for cloning repositories
4. **Beaglegaze Python SDK** (needs to be cloned separately - see setup steps)

## 🚀 Quick Start

### Step 0: Clone Required Repositories

First, ensure you have both the examples and the Python SDK:

```bash
# Clone the examples repository (if not already done)
git clone https://github.com/beaglegaze/beaglegaze-examples.git
cd beaglegaze-examples

# Clone the Python SDK (required dependency)
git clone https://github.com/beaglegaze/beaglegaze-python-sdk.git
```

**Important:** The Python sample expects the SDK to be located at `../../beaglegaze-python-sdk` relative to the `python/` directory. Your directory structure should look like:

```
your-workspace/
├── beaglegaze-examples/
│   └── python/
│       ├── demo.py
│       ├── fund.py
│       └── requirements.txt
└── beaglegaze-python-sdk/
    ├── setup.py
    └── beaglegaze/
```

### Step 1: Set Up the Ethereum Testnet

First, start a local Hardhat testnet with the deployed smart contract:

```bash
# From the root of beaglegaze-examples repository
docker buildx build -t hardhat-testnet deploy/hardhat-testnet/.
docker run -d -p 8545:8545 --rm --name hardhat-testnet hardhat-testnet
```

The testnet will deploy the contract at address: `0x289B72CEeaB48832261626D62E3daA87Fd90B024`

### Step 2: Install Dependencies

```bash
cd beaglegaze-examples/python
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** The `requirements.txt` file installs the beaglegaze SDK from the local clone using `-e ../../beaglegaze-python-sdk`. If you get import errors, verify that:
1. The beaglegaze-python-sdk directory exists at the correct relative path
2. Your virtual environment is activated
3. The SDK was installed successfully (you should see it listed in `pip list`)

### Step 3: Try the Demo (Will Fail Initially)

Run the demo without funding first to see the expected failure:

```bash
python demo.py
```

**Expected output:**
```
--- Calling monetized function ---

Call 1:
Processing batch with sum 10000...
Error: Insufficient client funding
```

### Step 4: Fund the Smart Contract

Fund the contract with ETH so the client can make paid function calls:

```bash
python fund.py
```

This script sends 0.1 ETH to the smart contract on behalf of the client account.

### Step 5: Run the Demo Successfully

Now run the demo again:

```bash
python demo.py
```

**Expected output:**
```
--- Calling monetized function ---

Call 1:
Executing important_function with args=(0,) and kwargs={}

Call 2:
Executing important_function with args=(1,) and kwargs={}

Call 3:
Executing important_function with args=(2,) and kwargs={}

Call 4:
Executing important_function with args=(3,) and kwargs={}

Call 5:
Executing important_function with args=(4,) and kwargs={}

--- Demo complete ---
```

## 📖 How It Works

### The Monetized Library

The `MonetizedLibrary` class in `demo.py` demonstrates how to integrate Beaglegaze:

```python
class MonetizedLibrary:
    def __init__(self, network_url: str, client_private_key: str):
        # Set up async batch processor
        async_processor = AsyncBatchProcessor(BatchMode.OFF)
        
        # Create smart contract instance
        smart_contract = SmartContract(
            "0x289B72CEeaB48832261626D62E3daA87Fd90B024",  # Contract address
            network_url,
            client_private_key,
            10  # batch size
        )
        
        # Set up contract consumer and global processor
        contract_consumer = ContractConsumer(smart_contract)
        async_processor.add_observer(contract_consumer)
        set_processor(async_processor)

    @pay_per_call(price=10000)  # 10,000 wei per call
    def important_function(self, *args, **kwargs):
        """This function costs 10,000 wei per call."""
        print(f"Executing important_function with args={args} and kwargs={kwargs}")
        return "Success"
```

### Key Components

- **`@pay_per_call(price=10000)`**: Decorator that makes the function cost 10,000 wei per call
- **`AsyncBatchProcessor`**: Handles asynchronous fee collection
- **`SmartContract`**: Interface to the Ethereum smart contract
- **`ContractConsumer`**: Processes fee collection events

### Configuration

The demo uses these default values:
- **Network URL**: `http://localhost:8545` (local Hardhat testnet)
- **Client Private Key**: `0xcccc...cccc` (pre-funded test account)
- **Contract Address**: `0x289B72CEeaB48832261626D62E3daA87Fd90B024`
- **Price per call**: 10,000 wei

## 🔍 Understanding the Workflow

1. **Client Setup**: The library initializes with a client private key and connects to the smart contract
2. **Fee Collection**: When `important_function()` is called, the `@pay_per_call` decorator triggers a fee collection event
3. **Asynchronous Processing**: The `AsyncBatchProcessor` batches multiple calls for efficiency
4. **Smart Contract Interaction**: The `ContractConsumer` processes the batch and deducts fees from the client's pre-funded account

## 🎯 Customizing for Your Library

To integrate Beaglegaze into your own Python library:

1. **Add the decorator** to functions you want to monetize:
   ```python
   @pay_per_call(price=50000)  # Set your price in wei
   def your_expensive_function(self):
       # Your implementation here
       pass
   ```

2. **Initialize the processor** in your library's constructor:
   ```python
   def __init__(self, client_private_key: str):
       # Set up the same components as in the demo
       async_processor = AsyncBatchProcessor(BatchMode.OFF)
       smart_contract = SmartContract(contract_address, network_url, client_private_key, batch_size)
       contract_consumer = ContractConsumer(smart_contract)
       async_processor.add_observer(contract_consumer)
       set_processor(async_processor)
   ```

3. **Deploy your smart contract** or use an existing one for your service

## 📚 Additional Resources

- [Beaglegaze Examples Repository](https://github.com/beaglegaze/beaglegaze-examples)
- [Java SDK Documentation](../java/README.md)
- [Smart Contract Documentation](../../beaglegaze-web3/README.md)

## ⚠️ Important Notes

- Due to asynchronous processing, not every method invocation is immediately charged
- Some calls may execute even with insufficient funding, but the library will eventually block when funds are depleted
- Always test with a local testnet before deploying to mainnet
- Ensure clients understand the fee structure of your library

## 🐛 Troubleshooting

**"Insufficient client funding" error:**
- Run `python fund.py` to add more ETH to the client account
- Check that the Hardhat testnet is running on port 8545

**Import errors:**
- Ensure the beaglegaze-python-sdk is properly installed: `pip install -e ../../beaglegaze-python-sdk`
- Check that the beaglegaze-python-sdk directory exists at the correct relative path
- Verify your virtual environment is activated: `which python` should point to your venv

**Connection errors:**
- Verify the Hardhat testnet is running: `docker ps`
- Ensure no firewall is blocking port 8545
