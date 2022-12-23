"""
The utils module provides utility functions, such as logging in.
"""

import mechanicalsoup
from bs4 import BeautifulSoup
from requests import Session
from ._DESAdapter import DESAdapter, environment_requires_DES_adapter

def login(email, password):
	"""
	Logs in to kenpom.com using user credentials.

	Args:
		email (str): User e-mail for login to kenpom.com.
		password (str): User password for login to kenpom.com.

	Returns:
		browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com.
	"""

	# Fix for Cloudflare SSL profiling (https://github.com/j-andrews7/kenpompy/issues/33) provided by Nick Ostendorf (@nickostendorf)
	session = Session()
	if environment_requires_DES_adapter():
		session.mount('https://kenpom.com/', DESAdapter())

	browser = mechanicalsoup.StatefulBrowser(session)
	browser.set_user_agent('Mozilla/5.0')
	browser.open('https://kenpom.com/index.php')

	if 'Cloudflare' in browser.page.title.string:
		raise Exception(
			'Opening kenpom.com failed - request was intercepted by Cloudflare protection')

	# Response page actually throws an error but further navigation works and will show you as logged in.
	browser.get_current_page()
	browser.select_form('form[action="handlers/login_handler.php"]')
	browser['email'] = email
	browser['password'] = password

	response = browser.submit_selected()

	if response.status_code != 200 or 'PHPSESSID=' not in response.headers['set-cookie']:
		raise Exception(
			'Logging in to kenpom.com failed - check that the site is available and your credentials are correct.')

	return browser