from decimal import Decimal

#from playwright.sync_api import sync_playwright, Playwright, Browser



def fill_order(stocks: dict[str, Decimal]):
	print('Upload the order .json to the Fidelity Chrome Extension to place the order.')

#	print('Attemption to complete order through Fidelity, make sure the market is open.')
#
#	with sync_playwright() as playwright:
#		browser: Browser = playwright.chromium.launch_persistent_context('data/chrome-profile', headless=False)
#
#		page = browser.pages[0] if browser.pages else browser.new_page()
#
#		# Let the user login if they need to.
#		page.goto('https://digital.fidelity.com/ftgw/digital/portfolio/summary')
#		page.wait_for_url('https://digital.fidelity.com/ftgw/digital/portfolio/summary', timeout=60000)
#
#		for ticker, notional in stocks.items():
#			page.goto(f'https://digital.fidelity.com/ftgw/digital/trade-equity?ACCOUNT={config.FIDELITY_ACCOUNT_NUMBER}&SYMBOL={ticker}')
#
#			page.wait_for_timeout(1000)
#			page.wait_for_selector('#buy-segment').click()
#			page.click('#dollars-segment')
#			page.fill('#shareAmount')
#			page.click('#market-yes-segment')
#			page.click('#previewOrderBtn')
#
#			if not config.DRY_RUN:
#				page.wait_for_selector('#placeOrderBtn').click()
#
#			page.wait_for_timeout(1000)
#
#			print(f'Order placed for ${notional} of {ticker}')
#
#		browser.close()
#		print('Order complete!')


def liquidate_all():
	print('Upload the order .json to the Fidelity Chrome Extension to place the order.')


