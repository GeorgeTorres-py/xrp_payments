from datetime import datetime
import json

def validate_xrp_address(address):
    # Basic validation - should be enhanced for production
    return len(address) == 34 and address.startswith('r')

def load_payment_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Validate payment data
    for payment in data['payments']:
        if not validate_xrp_address(payment['destination']):
            raise ValueError(f"Invalid XRP address: {payment['destination']}")
        if not isinstance(payment['amount'], (int, float)) or payment['amount'] <= 0:
            raise ValueError(f"Invalid amount for {payment['destination']}")
    
    return data

def save_payment_history(payment_data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"payment_history_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(payment_data, f, indent=2)
    
    return filename
