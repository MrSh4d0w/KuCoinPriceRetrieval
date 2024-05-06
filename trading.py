import os
from dotenv import load_dotenv

# Load information from the .env file
load_dotenv()

# Account details (especified in the .env file)
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
api_passphrase = os.getenv("API_PASSPHRASE")

# Trading

from kucoin.client import Trade
client = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase, is_sandbox=False)

# place a limit buy order
order_id = client.create_limit_order('BTC-USDT', 'buy', '1', '30000')

# NO RECOMMENDED: place a market buy order (It will buy at the current market price)
# order_id = client.create_market_order('BTC-USDT', 'buy', size='1')

# cancel limit order 
client.cancel_order(order_id)

order_id = client.create_limit_order('BTC-USDT', 'sell', '1', '40000')

client.cancel.order(order_id)
