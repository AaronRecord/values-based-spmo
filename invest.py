import os
import json
from decimal import Decimal
from datetime import datetime
from pandas import DataFrame

import config

from tools.generate_holdings import generate_holdings
from tools.scrape_ensign_peak import scrape as scrape_ensign_peak
from tools.scrape_spmo import scrape as scrape_spmo
from tools.rebalance import rebalance

if config.BROKERAGE == 'Alpaca':
	import alpaca_impl


def main():
	previous_holdings = None

	data_folder_empty = len(os.listdir('data')) == 0
	if not data_folder_empty:
		with open('data/holdings.json', encoding='utf-8') as f:
			previous_holdings = json.load(f)
			previous_holdings = { k: Decimal(v) for k, v in previous_holdings.items() }

	if data_folder_empty or config.UPDATE_SCRAPED_DATA:
		ensign_peak = scrape_ensign_peak(config.EMAIL_ADDRESS)
		with open('data/ensign_peak.json', 'w') as f:
			json.dump(ensign_peak, f, indent='\t', ensure_ascii=False, default=str)

		spmo = scrape_spmo()
		with open('data/spmo.json', 'w') as f:
			json.dump(spmo, f, indent='\t', ensure_ascii=False, default=str)
	else:
		with open('data/ensign_peak.json', 'r') as f:
			ensign_peak = json.load(f)
			ensign_peak['holdings'] = { k: Decimal(v) for k, v in ensign_peak['holdings'].items() }
		with open('data/spmo.json', 'r') as f:
			spmo = json.load(f)
			spmo['holdings'] = { k: Decimal(v) for k, v in spmo['holdings'].items() }

	holdings: dict[str, Decimal] = generate_holdings(ensign_peak, spmo)
	with open('data/holdings.json', 'w') as f:
		json.dump(holdings, f, indent='\t', ensure_ascii=False, default=str)

	order_notional = round(Decimal(input('How much would you like to invest? E.g. $1,000.00\n$').strip().replace(',', '')), 2)
	if order_notional == Decimal('0.0'):
		return

	original_holding_count = len(holdings)

	# Remove stocks whose amount is less than $1.00
	for ticker, weight in reversed(list(holdings.items())):
		amount = round(order_notional * weight, 2)
		if amount > Decimal('1.0'):
			break

		print(f'Skipping {ticker}, can\'t purchase ${amount} (less than $1.00)')
		del holdings[ticker]

	if len(holdings) > config.MAX_HOLDINGS:
		holdings = dict(list(holdings.items())[:config.MAX_HOLDINGS])

	# Rebalance the weights.
	if len(holdings) < original_holding_count:
		holdings = rebalance(holdings)

	# Calculate the exact amount of money to spend on each stock.
	notionalized_holdings: dict[str, Decimal] = { ticker: round(order_notional * weight, 2) for ticker, weight in holdings.items() }

	# Take off whatever extra or add whatever's missing to the highest stock to achieve the exact `order_notional`.
	final_holding_ticker = next(iter(holdings))
	notionalized_holdings[final_holding_ticker] -= sum(notionalized_holdings.values()) - order_notional

	assert sum(notionalized_holdings.values()) == order_notional

	d: DataFrame = DataFrame({
		'Ticker': holdings.keys(),
		'Weight': holdings.values(),
		'Notional': notionalized_holdings.values()
	})

	file_name = f'order_{round(datetime.now().timestamp())}'
	os.makedirs(f'data/{file_name}')
	with open(f'data/{file_name}/{file_name}.csv', 'w', encoding='utf-8') as f:
		d.to_csv(f)
	with open(f'data/{file_name}/{file_name}.md', 'w', encoding='utf-8') as f:
		d.to_markdown(f)
	with open(f'data/{file_name}/{file_name}.json', 'w', encoding='utf-8') as f:
		d.to_json(f)

	print(f'Order information has been saved to data/{file_name}')

	match config.BROKERAGE.title():
		case 'Alpaca':
			alpaca_impl.fill_order(notionalized_holdings)

main()
