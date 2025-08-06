from decimal import Decimal
import getpass

from playwright.sync_api import sync_playwright, Playwright

import config


def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://digital.fidelity.com/prgw/digital/login/full-page')
    page.get_by_label('Username', exact=True).fill(config.FIDELITY_USERNAME)
    page.get_by_label('Password', exact=True).fill(config.FIDELITY_PASSWORD)
    page.get_by_role('button', name='Log In').click()


    page.wait_for_url('https://digital.fidelity.com/ftgw/digital/portfolio/summary', timeout=60000)

    browser.close()

with sync_playwright() as playwright:
    run(playwright)


def fill_order(stocks: dict[str, Decimal]):
    step_1, step_2 = browser.login(config.FIDELITY_USERNAME, config.FIDELITY_PASSWORD, totp_code, False)
    if step_1 and step_2:
        print('Logged in')
    else:
        print('Failed to login to Fidelity.')
        return

    print('Attemption to complete order through Fidelity...')

    for ticker, notional in stocks.items():
        _success, error_message = browser.transaction(ticker, notional, 'buy', config.FIDELITY_ACCOUNT, config.DRY_RUN)
        if error_message != None:
            print(f'Failed to purchase {ticker} for ${notional}: {error_message}')
            return

        browser.page.reload()

        print(f'Order placed for ${notional} of {ticker}')

    browser.close_browser()
    print('Order complete!')


def liquidate_all():
	pass
