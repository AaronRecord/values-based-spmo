import config

match config.BROKERAGE:
	case 'Fidelity':
		import fidelity
		fidelity.liquidate_all()

	case 'Alpaca':
		import alpaca
		alpaca.liquidate_all()
