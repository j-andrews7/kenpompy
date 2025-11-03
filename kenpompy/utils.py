"""
The utils module provides utility functions, such as logging in.
"""

import cloudscraper
from cloudscraper import CloudScraper
from typing import Optional

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
	if 'Logged in as' not in home_page.text:
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

def validate_season(browser: CloudScraper, current_season, season: Optional[int]=None):

	if season:
		if int(season) < 1999:
			raise ValueError(
				'season cannot be less than 1999, as data only goes back that far.')
		if int(season) > current_season:
			raise ValueError(
				'season cannot be greater than the current year.')
	else:
		season = int(current_season)
	return season
