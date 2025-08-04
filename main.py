from alpaca.trading.client import TradingClient
from config import *

trading_client: TradingClient = TradingClient(API_KEY, SECRET_KEY, paper=True)

account = trading_client.get_account()
