import random
import time
import requests
from web3 import Web3
from dotenv import load_dotenv
import os

# Muat private key dari file .env
load_dotenv()
sepolia_private_key = os.getenv("PRIVATE_KEY")

# Setup jaringan Ethereum Sepolia
sepolia_rpc_url = 'https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID'  # Ganti dengan RPC Sepolia Anda
sepolia_chain_id = 11155111  # Sepolia Chain ID
w3_sepolia = Web3(Web3.HTTPProvider(sepolia_rpc_url))

# Setup jaringan OnlyLayer
onlylayer_rpc_url = 'https://onlylayer.org'
onlylayer_chain_id = 5816452
w3_onlylayer = Web3(Web3.HTTPProvider(onlylayer_rpc_url))

# Bridge URL
bridge_url = 'https://only-layer-dxypre7nhx-2ded73e84a7ab687.testnets.rollbridge.app/'

# Alamat wallet Sepolia dari private key
sepolia_account = w3_sepolia.eth.account.privateKeyToAccount(sepolia_private_key)
sepolia_address = sepolia_account.address

# Fungsi untuk mengecek saldo di Sepolia
def check_balance():
    balance = w3_sepolia.eth.get_balance(sepolia_address)
    return w3_sepolia.fromWei(balance, 'ether')

# Fungsi untuk mengirimkan transaksi ke bridge
def send_to_bridge(amount):
    headers = {'Content-Type': 'application/json'}
    data = {
        'fromChainId': sepolia_chain_id,
        'toChainId': onlylayer_chain_id,
        'fromAddress': sepolia_address,
        'toAddress': sepolia_address,  # Ganti dengan alamat tujuan di OnlyLayer
        'amount': str(amount)
    }

    try:
        response = requests.post(bridge_url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Transaksi berhasil: {response.json()}")
            return True  # Kembali True jika berhasil
        else:
            print(f"Gagal mengirim transaksi: {response.status_code} - {response.text}")
            return False  # Kembali False jika gagal
    except Exception as e:
        print(f"Terjadi kesalahan saat mengirim transaksi: {str(e)}")
        return False  # Kembali False jika error

# Fungsi untuk mengirimkan transaksi dari Sepolia
def send_transaction(amount):
    nonce = w3_sepolia.eth.getTransactionCount(sepolia_address)
    gas_price = w3_sepolia.eth.gas_price
    gas_limit = 21000  # Gas limit untuk transaksi standar

    tx = {
        'nonce': nonce,
        'to': sepolia_address,  # Ganti dengan alamat tujuan yang sesuai
        'value': w3_sepolia.toWei(amount, 'ether'),
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': sepolia_chain_id
    }

    signed_tx = w3_sepolia.eth.account.sign_transaction(tx, private_key=sepolia_private_key)
    try:
        tx_hash = w3_sepolia.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaksi dikirim dengan hash: {tx_hash.hex()}")
        return True  # Kembali True jika berhasil
    except Exception as e:
        print(f"Gagal mengirim transaksi: {str(e)}")
        return False  # Kembali False jika error

# Fungsi utama untuk melakukan auto-bridge
def auto_bridge():
    while True:
        balance = check_balance()
        print(f"Saldo di Sepolia: {balance} ETH")
        
        if balance > 0:
            # Tentukan jumlah yang akan di-bridge secara acak
            min_amount = 0.01  # Minimum jumlah yang ingin dibridge (misalnya 0.01 ETH)
            max_amount = min(balance, 0.1)  # Maksimum jumlah yang ingin dibridge (misalnya 0.1 ETH)
            amount_to_bridge = round(random.uniform(min_amount, max_amount), 4)
            
            print(f"Mencoba mengirim {amount_to_bridge} ETH ke OnlyLayer Testnet melalui bridge.")
            
            # Kirim transaksi ke bridge
            success = send_to_bridge(amount_to_bridge)
            
            # Jika gagal, coba lagi
            retry_attempts = 0
            while not success and retry_attempts < 5:
                print("Retrying transaction...")
                success = send_to_bridge(amount_to_bridge)
                retry_attempts += 1
                time.sleep(5)  # Delay 5 detik sebelum mencoba lagi

            if success:
                # Kirim transaksi dari Sepolia jika bridge berhasil
                send_transaction(amount_to_bridge)
            
            print("Berikutnya dalam 5 detik...")
            time.sleep(5)  # Delay 5 detik sebelum menjalankan transaksi berikutnya
        else:
            print("Saldo tidak cukup untuk melakukan bridge.")
            time.sleep(5)  # Delay 5 detik sebelum mencoba lagi jika saldo tidak cukup

# Jalankan bot
if __name__ == "__main__":
    auto_bridge()
