from urllib.parse import urlparse
from web3 import Web3


def get_provider(type, address):
    if type == 'ipc':
        return Web3(Web3.HTTPProvider(address))
    elif type == 'http':
        return Web3(Web3.HTTPProvider(address))
    elif type == 'websocket':
       return Web3(Web3.WebsocketProvider(address))
    else:
        raise Exception("No valid type of geth provider given, %s", type)

def ping_test(web3):
    if (web3.isConnected()):
        return True
    return False

