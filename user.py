import os
from dotenv import load_dotenv

# Load information from the .env file
load_dotenv()

# Account details (especified in the .env file)
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
api_passphrase = os.getenv("API_PASSPHRASE")

# USER
from kucoin.client import User
client = User(api_key, api_secret, api_passphrase)

# Get actual fee
print(client.get_actual_fee('BTC-USDT'))

