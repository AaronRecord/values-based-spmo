import os
import json
from decimal import Decimal
from datetime import datetime
from pandas import DataFrame

import config

from tools.generate_holdings import generate_holdings
from tools.scrape_ensign_peak import scrape as scrape_ensign_peak
from tools.scrape_spmo import scrape as scrape_spmo


if config.BROKERAGE == 'Fidelity':
	import fidelity

if config.BROKERAGE == 'Alpaca':
	import alpaca


def main():
	previous_ensign_peak = None
	previous_spmo = None
	previous_holdings = None
	if len(os.listdir('data')) > 1:
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

	holdings: dict[str, Decimal] = generate_holdings(ensign_peak, spmo, config.MANUAL_EXCLUDE)
	with open('data/holdings.json', 'w') as f:
		json.dump(holdings, f, indent='\t', ensure_ascii=False, default=str)

	order_notional = Decimal('0.0')

	if previous_holdings != None and previous_holdings != holdings:
		print('The generated holdings have changed, consider liquidating your existing holdings (using liquidate_all.py)')

	order_notional += round(Decimal(input('How much would you like to invest? E.g. $1,000.00\n$').strip().replace(',', '')), 2)
	if order_notional == Decimal('0.0'):
		return

	total = Decimal('0.0')

	# Lowest weights first
	holdings_list: list[tuple[str, Decimal]] = list(reversed(holdings.items()))
	original_holding_count = len(holdings_list)

	# Remove stocks whose amount is less than $1.00
	while True:
		weight = holdings_list[0][1]
		amount = round(order_notional * weight, 2)
		if amount > Decimal('1.0'):
			break

		print(f'Skipping {holdings_list[0][0]}, can\'t purchase ${amount} (less than $1.00)')
		del holdings_list[0]

	# Rebalance the weights.
	if len(holdings_list) < original_holding_count:
		total_weight: Decimal = sum(map(lambda holding: holding[1], holdings_list))
		balance_factor: Decimal = Decimal('1.0') / total_weight

		holdings_list = [ (ticker, weight * balance_factor) for ticker, weight in holdings_list ]

		assert abs(sum(map(lambda holding: holding[1], holdings_list)) - Decimal('1.0')) < Decimal('0.0001')

	# Calculate the exact amount of money to spend on each stock.
	notionalized_holdings: dict[str, Decimal] = {}

	for ticker, weight in holdings_list[:-1]:
		amount: Decimal = round(order_notional * weight, 2)
		total += amount
		notionalized_holdings[ticker] = amount

	# Whatever's left, invest in the stock with the highest weight.
	# This way, if rounding leads there to be a couples cents above or below `order_notional`
	# it won't cause there to actually be more money spent than the exact desired amount.
	final_holding = holdings_list[-1]
	amount = order_notional - total

	notionalized_holdings[final_holding[0]] = amount

	assert sum(notionalized_holdings.values()) == order_notional

	if config.EXPORT_CSV:
		file_path = f'data/order_{round(datetime.now().timestamp())}.json'
		with open(file_path, 'w', encoding='utf-8') as f:
			d: DataFrame = DataFrame({
				'Ticker': [ holding[0] for holding in holdings_list ],
				'Weight': [ holding[1] for holding in holdings_list ],
				'Notional': [ notional for _ticker, notional in notionalized_holdings.items() ]
			})

			d.to_csv(f, encoding='utf-8')

		print(f'Order information has been saved to {file_path}')

		match config.BROKERAGE.title():
			case 'Fidelity':
				fidelity.fill_order(notionalized_holdings)
			case 'Alpaca':
				alpaca.fill_order(notionalized_holdings)

main()
