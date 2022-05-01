from dis import Bytecode
from solcx import compile_source
from json import dump
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# Open the contract
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compile the contract
compiled_sol = compile_source(
    simple_storage_file, output_values=['abi', 'bin']
)


# Dump the compiled contract
with open("./SimpleStorage.json", "w") as file:
    dump(compiled_sol, file)


# Get the contract ABI and bytecode
contract_id, contract_interface = compiled_sol.popitem()


# Ganache Setup
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chainId = 5777
my_address = '0x3D0d971536219CE5c75653518780f08BE1d477aF'
private_key = os.getenv("PRIVATE_KEY")


# Get Nonce
nonce = w3.eth.getTransactionCount(my_address)


# Create the contract
SimpleContract = w3.eth.contract(
    abi=contract_interface['abi'], bytecode=contract_interface['bin']
)


# Create The Transaction
print("Deploying the contract...")
tx = SimpleContract.constructor().buildTransaction({
    'chainId': chainId,
    'gas': 2000000,
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce,
    'from': my_address
})


# Sign The Transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
# Send the transaction to chain
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract Deployed")
# Build the contract instance
simple_storage = SimpleContract(tx_receipt.contractAddress)


# Now we can call the contract methods
# Call -> Does not change contract state hence no gas cost
print(simple_storage.functions.retreive().call())

# Transact -> Changes contract state hence gas cost
print("Updating contract...")
set_tx = simple_storage.functions.set(15).buildTransaction({
    'chainId': chainId,
    'gas': 2000000,
    'gasPrice': w3.toWei('40', 'gwei'),
    'nonce': nonce + 1,
})

signed_set_tx = w3.eth.account.sign_transaction(set_tx, private_key)
signed_set_tx_hash = w3.eth.send_raw_transaction(signed_set_tx.rawTransaction)

set_tx_reciept = w3.eth.wait_for_transaction_receipt(signed_set_tx_hash)
print("Contract Updated!")

print(simple_storage.functions.retreive().call())
