import config

match config.BROKERAGE:
	case 'Alpaca':
		import alpaca_impl
		alpaca_impl.liquidate()
