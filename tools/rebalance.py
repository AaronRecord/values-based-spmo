from decimal import Decimal

def rebalance(holdings: dict[str, Decimal]) -> dict[str, Decimal]:
	total_weight: Decimal = sum(holdings.values())
	balance_factor: Decimal = Decimal('1.0') / total_weight

	rebalanced_holdings = { ticker: weight * balance_factor for ticker, weight in holdings.items() }

	assert abs(sum(rebalanced_holdings.values()) - Decimal('1.0')) < Decimal('0.0001')

	return rebalanced_holdings
