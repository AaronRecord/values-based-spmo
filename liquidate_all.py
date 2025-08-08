import config

match config.BROKERAGE:
	case 'Fidelity':
		print('Use the Fidelity Chrome Extension to liquidate all positions.')

	case 'Alpaca':
		import alpaca
		alpaca.liquidate_all()
