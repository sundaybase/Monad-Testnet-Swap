# Monad-Testnet-Swap
✨ Key Features

🔄 Auto Swap: Automatic conversion of MON to WMON.

💰 Auto Withdraw: Instantly withdraw WMON back to MON after swap.

⚡ Retry Mechanism: If the transaction fails, the bot will retry until it succeeds.

🔥 Multi-wallet Support: Can be used for multiple wallets at once.

📊 Transaction Log: Provides clear transaction reports in the terminal.

## Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)
- `git` [Git Download](https://git-scm.com/downloads) (if you want to easily update your code )(Without git every time your want to get latest version of code you have to manually download the zip file)

## How to Use 

**clone this repository**
```sh
git clone https://github.com/sundaybase/Monad-Testnet-Swap.git
cd Monad-Testnet-Swap
```

**Create a virtual environment:**
 
- **on Linux/Mac**
    ```sh
    python3 -m venv venv
    ```

- **on Windows**
    ```sh
    python -m venv venv
    ```

**Activate the virtual environment:**

- **on Linux/Mac**
    ```sh
    source venv/bin/activate
    ```
    
- **on Windows**
     ```sh
     venv\Scripts\activate
     ```

**Install the required packages:**

- **on Linux/Mac**
    
    ```sh
    pip3 install -r requirements.txt
    ```
    
- **on Windows**
     ```sh
     pip install -r requirements.txt
     ```

**Configuration**
Create a pvkeys.txt file and enter each wallet's private key in a separate line
```sh
nano pvkeys.txt
```

**Run the bot**
- **on Linux/Mac**
    ```sh
    python3 monswap.py
    ```

- **on Windows**
    ```sh
    python monswap.py
    ```

Follow Gwei on https://testnet.monadexplorer website
