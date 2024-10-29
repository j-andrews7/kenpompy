"""
The utils module provides utility functions, such as logging in.
"""

import cloudscraper
from cloudscraper import CloudScraper

def login(email: str, password: str):
	"""
	Logs in to kenpom.com using user credentials.

	Args:
		email (str): User e-mail for login to kenpom.com.
		password (str): User password for login to kenpom.com.

	Returns:
		browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com.
	"""

	browser = cloudscraper.create_scraper()
	browser.get('https://kenpom.com/index.php')

	form_data = {
		'email': email,
		'password': password,
		'submit': 'Login!',
	}

	# Response page actually throws an error but further navigation works and will show you as logged in.
	browser.post(
		'https://kenpom.com/handlers/login_handler.php',
		data=form_data, 
		allow_redirects=True
	)

	home_page = browser.get('https://kenpom.com/')
	if 'Logout' not in home_page.text:
		raise Exception('Logging in failed - check your credentials')

	return browser

def get_html(browser: CloudScraper, url: str):
	"""
	Performs a get request on the specified url.

	Args:
		browser (CloudScraper): Authenticated browser with full access to kenpom.com generated
            by the `login` function.
		url (str): The url to perform the get request on.
	
	Returns:
		html (Bytes | Any): The return content.
	
	Raises:
		Exception if get request gets a non-200 response code.
	"""	
	response = browser.get(url)
	if response.status_code != 200:
		raise Exception(f'Failed to retrieve {url} (status code: {response.status_code})')
	return response.content