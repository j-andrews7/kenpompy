"""
This module provides functions for scraping the miscellaneous stats kenpom.com pages into more
usable pandas dataframes.
"""

import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup


def get_trends(browser):
	"""
	Scrapes the statistical trends table (https://kenpom.com/trends.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.

	Returns:
			trends_df (pandas dataframe): Pandas dataframe containing the statistical trends table from kenpom.com.
	"""

	url = 'https://kenpom.com/trends.php'

	browser.open(url)
	trends = browser.get_current_page()
	table = trends.find_all('table')[0]
	trends_df = pd.read_html(str(table))

	# Dataframe tidying.
	trends_df = trends_df[0]
	trends_df.drop(trends_df.tail(5).index,inplace=True)

	return trends_df


def get_refs(browser, season=None):
	"""
	Scrapes the officials rankings table (https://kenpom.com/officials.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2016 is the earliest available season.

	Returns:
			refs_df (pandas dataframe): Pandas dataframe containing the officials rankings table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2016.
	"""

	if season:
		if int(season) < 2016:
			raise ValueError(
				'season cannot be less than 2016, as data only goes back that far.')
		url = url + '?y=' + season

	url = 'https://kenpom.com/officials.php'

	browser.open(url)
	refs = browser.get_current_page()
	table = refs.find_all('table')[0]
	refs_df = pd.read_html(str(table))

	# Dataframe tidying.
	refs_df = refs_df[0]
	refs_df.drop(refs_df.head(1).index,inplace=True)
	refs_df.columns = ['Rank', 'Name', 'Rating', 'Games', 'Last Game', 'Game Score', 'Box']
	refs_df = refs_df[refs_df.Rating != 'Rating']
	refs_df = refs_df.drop(['Box'], axis=1)

	return refs_df


def get_courts(browser):
	"""
	Scrapes the home court advantage table (https://kenpom.com/hca.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.

	Returns:
			hca_df (pandas dataframe): Pandas dataframe containing the home court advantage table from kenpom.com.
	"""

	browser.open(url)
	hca = browser.get_current_page()
	table = hca.find_all('table')[0]
	hca_df = pd.read_html(str(table))

	# Dataframe tidying.
	hca_df = hca_df[0]
	hca_df.columns = ['Team', 'Conference', 'HCA', 'HCA.Rank', 'PF', 'PF.Rank', 'Pts', 'Pts.Rank', 'NST', 
	'NST.Rank', 'Blk', 'Blk.Rank', 'Elev', 'Elev.Rank']
	hca_df = hca_df[hca_df.Team != 'Team']

	return hca_df