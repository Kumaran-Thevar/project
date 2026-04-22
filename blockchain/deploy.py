from web3 import Web3
from solcx import compile_standard, install_solc
import json

install_solc("0.8.0")

with open("blockchain/contract.sol", "r") as file:
    contract_source = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"contract.sol": {"content": contract_source}},
    "settings": {
        "outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode"]}}
    }
}, solc_version="0.8.0")

bytecode = compiled_sol["contracts"]["contract.sol"]["CertificateStore"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["contract.sol"]["CertificateStore"]["abi"]

with open("blockchain/abi.json", "w") as f:
    json.dump(abi, f)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

account = w3.eth.accounts[0]

Certificate = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = Certificate.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract Address:", tx_receipt.contractAddress)