"""
A simple, yet comprehensive web scraper for kenpom.com.

This module provides functions for scraping kenpom.com pages into more
usable pandas dataframes.
"""

import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup


def login(email, password):
    """
    Logs in to kenpom.com using user credentials.
    """

    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://kenpom.com/index.php")

    # Response page actually throws an error but further navigation works and will show you as logged in.
    browser.get_current_page()
    browser.select_form('form[action="handlers/login_handler.php"]')
    browser["email"] = email
    browser["password"] = password

    response = browser.submit_selected()

    if response.status_code != 200:
        raise Exception(
            'Logging in to kenpom.com failed - check that the site is available and your credentials are correct.')
