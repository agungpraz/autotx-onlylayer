import os
import time
import random
import requests
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables from privkey.env file
load_dotenv('privkey.env')

private_key = os.getenv('PRIVATE_KEY')

# Configuration
sepolia_rpc = "https://sepolia.infura.io/v3/<YOUR_INFURA_PROJECT_ID>"
onlylayer_rpc = "https://onlylayer.org"
sepolia_web3 = Web3(Web3.HTTPProvider(sepolia_rpc))
onlylayer_web3 = Web3(Web3.HTTPProvider(onlylayer_rpc))

your_wallet_address = "0xYourWalletAddress"  # ganti dengan alamat wallet kamu
min_amount = 0.01  # Minimal nominal yang ingin dibridge (Ether)
max_amount = 0.1  # Maksimal nominal yang ingin dibridge (Ether)
delay = 5  # Waktu delay dalam detik

def bridge_token(amount):
    try:
        # Logic untuk bridging dari Sepolia ke OnlyLayer via website bridge
        data = {
            "from": "Ethereum Sepolia",
            "to": "OnlyLayer",
            "amount": amount,
            "walletAddress": your_wallet_address
        }
        
        # Menggunakan salah satu bridge website yang diberikan
        response = requests.post("https://only-layer-dxypre7nhx-2ded73e84a7ab687.testnets.rollbridge.app/bridge", json=data)
        
        if response.status_code == 200:
            print(f'Successfully bridged {amount} Ether to OnlyLayer')
        else:
            print(f'Failed to bridge: {response.content}')
    except Exception as e:
        print(f'Error encountered: {e}')
        print(f'Retrying after {delay} seconds...')

if __name__ == "__main__":
    while True:
        amount = random.uniform(min_amount, max_amount)
        bridge_token(amount)
        time.sleep(delay)
