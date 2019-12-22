"""
The utils module provides utility functions, such as logging in.
"""

import mechanicalsoup
from bs4 import BeautifulSoup


def login(email, password):
	"""
	Logs in to kenpom.com using user credentials.

	Args:
		email (str): User e-mail for login to kenpom.com.
		password (str): User password for login to kenpom.com.

	Returns:
		browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com.
	"""

	browser = mechanicalsoup.StatefulBrowser()
	browser.open('https://kenpom.com/index.php')

	# Response page actually throws an error but further navigation works and will show you as logged in.
	browser.get_current_page()
	browser.select_form('form[action="handlers/login_handler.php"]')
	browser['email'] = email
	browser['password'] = password

	response = browser.submit_selected()

	if response.status_code != 200:
		raise Exception(
			'Logging in to kenpom.com failed - check that the site is available and your credentials are correct.')

	return browser