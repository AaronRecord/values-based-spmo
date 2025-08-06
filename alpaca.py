from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from decimal import Decimal
import config

trading_client = TradingClient(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=config.DRY_RUN)

def fill_order(stocks: dict[str, Decimal]):
	print('Attempting to complete order through Alpaca...')


	for ticker, notional in stocks.items():
		market_order_data = MarketOrderRequest(
				symbol=ticker,
				notional=notional,
				side=OrderSide.BUY,
				time_in_force=TimeInForce.DAY
		)

		trading_client.submit_order(market_order_data)

		print(f'Order placed for ${notional} of {ticker}')

	print('Order complete!')


def liquidate_all():
	trading_client.close_all_positions(True)
