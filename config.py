import json
import os
from dotenv import load_dotenv

def load_config(config_path):
    load_dotenv()
    
    # First try to load from environment variables
    config = {
        'wallet_seed': os.getenv('XRPL_WALLET_SEED'),
        'network': os.getenv('XRPL_NETWORK', 'testnet'),
    }
    
    # Then load from config file if it exists
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    return config
