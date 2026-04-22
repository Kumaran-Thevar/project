from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("blockchain/abi.json") as f:
    abi = json.load(f)

contract_address = "0xB0e3C5C2B9A44f04C8BD7E59551f69644186fc81"

contract = w3.eth.contract(address=contract_address, abi=abi)

account = w3.eth.accounts[0]

def store_hash(cert_hash):
    tx = contract.functions.addCertificate(cert_hash).transact({"from": account})
    w3.eth.wait_for_transaction_receipt(tx)

def verify_hash(cert_hash):
    return contract.functions.verifyCertificate(cert_hash).call()