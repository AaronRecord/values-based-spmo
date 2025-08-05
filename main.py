from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import os
import json
from decimal import Decimal
import requests

import config
from tools.generate_holdings import generate_holdings
from tools.scrape_ensign_peak import scrape as scrape_ensign_peak
from tools.scrape_spmo import scrape as scrape_spmo


def main():
	previous_ensign_peak = None
	previous_spmo = None
	previous_holdings = None
	if os.listdir('data'):
		with open('data/ensign_peak.json', encoding='utf-8') as f:
			previous_ensign_peak = json.load(f)
			previous_ensign_peak['holdings'] = { k: Decimal(v) for k, v in previous_ensign_peak['holdings'].items() }
		with open('data/spmo.json', encoding='utf-8') as f:
			previous_spmo = json.load(f)
			previous_spmo['holdings'] = { k: Decimal(v) for k, v in previous_spmo['holdings'].items() }
		with open('data/holdings.json', encoding='utf-8') as f:
			previous_holdings = json.load(f)
			previous_holdings = { k: Decimal(v) for k, v in previous_holdings.items() }

	ensign_peak = scrape_ensign_peak(config.EMAIL_ADDRESS)
	with open('data/ensign_peak.json', 'w') as f:
		json.dump(ensign_peak, f, indent='\t', ensure_ascii=False, default=str)

	spmo = scrape_spmo()
	with open('data/spmo.json', 'w') as f:
		json.dump(spmo, f, indent='\t', ensure_ascii=False, default=str)

	holdings: dict[str, Decimal] = generate_holdings(ensign_peak, spmo)
	with open('data/holdings.json', 'w') as f:
		json.dump(holdings, f, indent='\t', ensure_ascii=False, default=str)

	order_notional = Decimal('0.0')
	trading_client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=config.PAPER)
	if previous_holdings != None and previous_holdings != holdings:
		update_existing_holdings = input('The holdings are not the same as last time, would you like to update your existing holdings? (Y/N)\n').upper() == 'Y'
		if update_existing_holdings:
			trading_client.close_all_positions(True)
			order_notional = Decimal(trading_client.get_account().non_marginable_buying_power)

	order_notional += round(Decimal(input('How much would you like to invest? E.g. $1,000.00\n$').strip().replace(',', '')), 2)
	if order_notional == Decimal('0.0'):
		return

	total = Decimal('0.0')
	notionalized_holdings: dict[str, Decimal] = {}

	# Lowest weights first
	holdings_list: list[tuple[str, Decimal]] = list(reversed(holdings.items()))
	deleted_holdings = 0

	while True:
		weight = holdings_list[0][1]
		amount = round(order_notional * weight, 2)
		if amount > Decimal('1.0'):
			break

		print(f'Skipping {holdings_list[0][0]}, can\'t purchase ${amount} (less than $1.00)')
		deleted_holdings += 1
		del holdings_list[0]

	if deleted_holdings > 0:
		total_weight: Decimal = sum(map(lambda holding: holding[1], holdings_list))
		balance_factor: Decimal = Decimal('1.0') / total_weight

		holdings_list = [ (ticker, weight * balance_factor) for ticker, weight in holdings_list ]

		assert sum(map(lambda holding: holding[1], holdings_list)) == Decimal('1.0')

	for ticker, weight in holdings_list[:-1]:
		amount: Decimal = round(order_notional * weight, 2)
		total += amount
		notionalized_holdings[ticker] = amount

	final_holding = holdings_list[-1]
	amount = order_notional - total

	notionalized_holdings[final_holding[0]] = amount

	assert sum(notionalized_holdings.values()) == order_notional

	for ticker, notional in notionalized_holdings.items():
		market_order_data = MarketOrderRequest(
				symbol=ticker,
				notional=notional,
				side=OrderSide.BUY,
				time_in_force=TimeInForce.DAY
		)

		trading_client.submit_order(
			order_data=market_order_data
		)

		print(f'Order placed for ${notional} of {ticker}')


main()
