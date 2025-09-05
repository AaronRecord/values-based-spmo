from edgar import *
import json
from decimal import Decimal


def scrape(email_address: str) -> dict:
	# Tell the SEC who you are (required by SEC regulations).
	set_identity(email_address)

	fund: Company = Company(1454984)

	filing: ThirteenF = fund.get_filings(form='13F-HR').latest().obj()
	total: Decimal = sum(map(lambda v: Decimal(v), filing.infotable['Value']))

	holdings = { row['Ticker']: Decimal(row['Value']) / total for _index, row in filing.infotable.iterrows() }

	# Sort by weight
	holdings = dict(sorted(holdings.items(), key=lambda holding: holding[1], reverse=True))

	ensign_peak = {
		'filing_date': filing.filing_date,
		'holdings': holdings,
	}

	return ensign_peak
