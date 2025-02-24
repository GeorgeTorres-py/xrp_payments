import argparse
import schedule
import time
from datetime import datetime
from payment_processor import PaymentDistributor
from config import load_config

def setup_cli():
    parser = argparse.ArgumentParser(description='XRP Ledger Payment Distribution CLI')
    parser.add_argument('--config', type=str, default='config.json',
                       help='Path to configuration file')
    parser.add_argument('--schedule', choices=['hourly', 'daily'],
                       help='Payment distribution schedule')
    parser.add_argument('--run-once', action='store_true',
                       help='Run distribution once and exit')
    return parser.parse_args()

def main():
    args = setup_cli()
    config = load_config(args.config)
    
    distributor = PaymentDistributor(
        seed=config['wallet_seed'],
        network=config['network']
    )

    if args.run_once:
        distributor.distribute_payments(config['payments'])
        return

    if args.schedule == 'hourly':
        schedule.every().hour.do(distributor.distribute_payments, config['payments'])
    elif args.schedule == 'daily':
        schedule.every().day.at("00:00").do(distributor.distribute_payments, config['payments'])
    
    print(f"Payment distribution scheduled: {args.schedule}")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
