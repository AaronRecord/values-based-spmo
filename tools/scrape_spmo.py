import requests
import pandas
import io
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal

def scrape() -> dict:
	URL = 'https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0?audienceType=Investor&action=download&ticker=SPMO'

	response = requests.get(URL)
	response.raise_for_status()

	spmo = pandas.read_csv(io.StringIO(response.text), dtype=str)
	spmo = { row['Holding Ticker'].strip(): Decimal(row['Weight']) / Decimal("100.0") for _index, row in spmo.iterrows() }

	return { 'scrape_date': datetime.now(ZoneInfo("America/New_York")).isoformat(sep=' ', timespec='hours'), 'holdings': spmo }
