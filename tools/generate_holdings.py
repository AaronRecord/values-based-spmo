from decimal import Decimal
from tools.rebalance import rebalance
import config

def generate_holdings(ensign_peak, spmo) -> dict[str, Decimal]:
	UNSHARED_TICKERS = spmo['holdings'].keys() - ensign_peak['holdings'].keys()
	print(f'Removing the following holdings from your investment: {UNSHARED_TICKERS}')

	adjusted_holdings: dict[str, Decimal] = spmo['holdings'].copy()

	for ticker in (UNSHARED_TICKERS | config.MANUAL_EXCLUDE_FROM_INVESTING):
		del adjusted_holdings[ticker]

	# Just to make sure it's sorted by weight
	adjusted_holdings = dict(sorted(adjusted_holdings.items(), key=lambda item: item[1], reverse=True))

	adjusted_holdings = rebalance(adjusted_holdings)

	return adjusted_holdings
