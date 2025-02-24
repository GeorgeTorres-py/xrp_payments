from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import submit_and_wait
import logging

class PaymentDistributor:
    def __init__(self, seed, network='testnet'):
        self.network = network
        if network == 'testnet':
            self.client = JsonRpcClient('https://s.altnet.rippletest.net:51234')
        else:
            self.client = JsonRpcClient('https://xrplcluster.com')
        
        self.wallet = Wallet.from_seed(seed)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def prepare_payment(self, destination, amount):
        return Payment(
            account=self.wallet.classic_address,
            destination=destination,
            amount=xrp_to_drops(amount)
        )

    def distribute_payments(self, payments):
        self.logger.info(f"Starting payment distribution for {len(payments)} recipients")
        
        for payment in payments:
            try:
                transaction = self.prepare_payment(
                    payment['destination'],
                    payment['amount']
                )
                
                response = submit_and_wait(
                    transaction=transaction,
                    client=self.client,
                    wallet=self.wallet
                )
                
                if response.is_successful():
                    self.logger.info(
                        f"Payment successful: {payment['amount']} XRP to {payment['destination']}"
                    )
                else:
                    self.logger.error(
                        f"Payment failed: {payment['amount']} XRP to {payment['destination']}"
                    )
                    self.logger.error(f"Error: {response.result}")
                    
            except Exception as e:
                self.logger.error(f"Error processing payment: {str(e)}")

    def get_balance(self):
        response = self.client.request(
            {
                "command": "account_info",
                "account": self.wallet.classic_address,
                "ledger_index": "validated"
            }
        )
        return int(response.result['account_data']['Balance']) / 1000000
