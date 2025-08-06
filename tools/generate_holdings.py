import json
import pandas
from decimal import Decimal

def generate_holdings(ensign_peak, spmo, manual_exclude: set) -> dict[str, Decimal]:
	UNSHARED_TICKERS = spmo['holdings'].keys() - ensign_peak['holdings'].keys()

	for t in (UNSHARED_TICKERS | manual_exclude):
		del spmo['holdings'][t]

	total_weight: Decimal = sum(map(lambda v: Decimal(v), spmo['holdings'].values()))
	balance_factor: Decimal = Decimal('1.0') / total_weight

	holdings = { ticker: weight * balance_factor for ticker, weight in spmo['holdings'].items() }

	assert abs(sum(holdings.values()) - Decimal('1.0')) < Decimal('0.0001')

	# Just to make sure it's sorted by weight
	dict(sorted(holdings.items(), key=lambda item: item[1]))

	return holdings
