from decimal import Decimal
from tools.rebalance import rebalance


def generate_holdings(ensign_peak, spmo, manual_exclude: set) -> dict[str, Decimal]:
	UNSHARED_TICKERS = spmo['holdings'].keys() - ensign_peak['holdings'].keys()
	print(f'Removing the following holdings: {UNSHARED_TICKERS}')

	adjusted_holdings: dict[str, Decimal] = spmo['holdings'].copy()

	for ticker in (UNSHARED_TICKERS | manual_exclude):
		del adjusted_holdings[ticker]

	# Just to make sure it's sorted by weight
	holdings = dict(sorted(holdings.items(), key=lambda item: item[1]))

	adjusted_holdings = rebalance(holdings)

	return holdings
