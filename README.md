# What is it? 🤔
A couple of scripts to invest in the same positions as the SPMO Momentum ETF, except those not also held by Ensign Peak Investors, so that companies whose values don't generally align with the Church of Jesus Christ of Latter-day Saints (e.g. tobacco, alcohol, gambling, and objectionable entertainment companies) aren't included.

Many values-based ETFs already exist, but most of them offer relatively poor returns. The idea is to achieve the high returns of Invesco's SPMO ETF, while not investing in companies that are immoral (not to say that any company is perfect).

Currently the following brokerages are supported: [Fidelity](fidelity.com) (using Playwright) and [Alpaca](https://alpaca.markets/). You will need to open an account with one of them (if you haven't already).

# How to use 🔧
Create a file named `config.py`, and then fill in all the required information and your desired settings (see the documentation below).

```py
# config.py

# Options are 'Fidelity', 'Alpaca', and 'None'
BROKERAGE: str = None

# Exports a CSV with each stock's ticker, weight, and dollar amount.
EXPORT_CSV: bool = True

# Any stocks you want to manually exclude, e.g. { 'FOX' }
# Alternatively, just set this to None
MANUAL_EXCLUDE: set = None

# Your email address (needed to scrape SEC website)
EMAIL_ADDRESS: str = '...'

# Only needed if `BROKERAGE` is set to 'Alpaca'
ALPACA_API_KEY: str = '...'
ALPACA_SECRET_KEY: str = '...'

# Only needed if `BROKERAGE` is set to 'Fidelity'.
# Note that if you're using Fidelity, you will also need to set up a 2FA authenticator app,
# and input your TOTP code as prompted by `main.py`.
FIDELITY_USERNAME: str = '...'
FIDELITY_PASSWORD: str = '...'

# The name/nickname of the Fidelity account you'd like to use, e.g. ROTH IRA
FIDELITY_ACCOUNT: str = '...'
```

Then run `invest.py` and input how much you would like to invest.

# ⚠️ Use at your own risk!!! ⚠️
I intend the best, but this tool is provided as-is with no warranty 🙂

