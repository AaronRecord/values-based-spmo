# What is it? 🤔
A couple of scripts to invest in the same positions as the SPMO Momentum ETF, except those not also held by Ensign Peak Investors, so that companies whose values don't generally align with the Church of Jesus Christ of Latter-day Saints (e.g. tobacco, alcohol, gambling, and objectionable entertainment companies) aren't included.

Many values-based ETFs already exist (e.g. CATH, PRAY, etc.), but most of them offer relatively poor returns. The idea is to achieve the high returns of Invesco's SPMO ETF, while not investing in companies that are immoral (not to say that any company is perfect).

Currently [Alpaca](https://alpaca.markets/) is the only supported brokerage. You will need to open an account with them (if you haven't already).

The program does however export a `.csv` and `.md` file that you can use as you wish.

# How to use 🔧
Create a file named `config.py`, and then fill in all the required information and your desired settings (see the documentation below).

```py
# config.py

# Options are 'Alpaca', and 'None'
BROKERAGE: str = 'Alpaca'

UPDATE_SCRAPED_DATA: bool = True

DRY_RUN: bool = True

# Any stocks you want to manually exclude from selling, e.g. { 'BWAY' }
MANUAL_EXCLUDE_FROM_LIQUIDATION: set = set()

# Any stocks you want to manually exclude from investing, e.g. { 'FOX' }
MANUAL_EXCLUDE_FROM_INVESTING: set = set()

MAX_HOLDINGS: int = 100

# Your email address (needed to scrape SEC website)
EMAIL_ADDRESS: str = '...'

ALPACA_API_KEY: str = '...'
ALPACA_SECRET_KEY: str = '...'
```

Then run `invest.py` and input how much you would like to invest.

You can use `liquidate.py` to liquidate your holdings if/when you'd like to adjust them.

# ⚠️ Use at your own risk!!! ⚠️
I intend the best, but this tool is provided as-is with no warranty 🙂

