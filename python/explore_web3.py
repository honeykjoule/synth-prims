from web3 import Web3

w3 = Web3(Web3.EthereumTesterProvider())

print(w3.eth.accounts)