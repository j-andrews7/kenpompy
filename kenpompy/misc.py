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
	trends_df.drop(trends_df.tail(5).index, inplace=True)

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

	url = 'https://kenpom.com/officials.php'

	if season:
		if int(season) < 2016:
			raise ValueError(
				'season cannot be less than 2016, as data only goes back that far.')
		url = url + '?y=' + str(season)

	browser.open(url)
	refs = browser.get_current_page()
	table = refs.find_all('table')[0]
	refs_df = pd.read_html(str(table))

	# Dataframe tidying.
	refs_df = refs_df[0]
	refs_df.drop(refs_df.head(1).index, inplace=True)
	refs_df.columns = ['Rank', 'Name', 'Rating', 'Games', 'Last Game', 'Game Score', 'Box']
	refs_df = refs_df[refs_df.Rating != 'Rating']
	refs_df = refs_df.drop(['Box'], axis=1)

	return refs_df


def get_hca(browser):
	"""
	Scrapes the home court advantage table (https://kenpom.com/hca.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2010 is the earliest available season.

	Returns:
			hca_df (pandas dataframe): Pandas dataframe containing the home court advantage table from kenpom.com.
	"""

	url = 'https://kenpom.com/hca.php'

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


def get_arenas(browser, season=None):
	"""
	Scrapes the arenas table (https://kenpom.com/arenas.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2010 is the earliest available season.

	Returns:
			arenas_df (pandas dataframe): Pandas dataframe containing the arenas table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2010.
	"""

	url = 'https://kenpom.com/arenas.php'

	if season:
		if int(season) < 2010:
			raise ValueError(
				'season cannot be less than 2010, as data only goes back that far.')
		url = url + '?y=' + str(season)

	browser.open(url)
	arenas = browser.get_current_page()
	table = arenas.find_all('table')[0]
	arenas_df = pd.read_html(str(table))

	# Dataframe tidying.
	arenas_df = arenas_df[0]
	arenas_df.columns = ['Team', 'Conference', 'Arena', 'Alternate']
	arenas_df['Arena'], arenas_df['Arena.Capacity'] = arenas_df['Arena'].str.split(' \(').str
	arenas_df['Arena.Capacity'] = arenas_df['Arena.Capacity'].str.rstrip(')')
	arenas_df['Alternate'], arenas_df['Alternate.Capacity'] = arenas_df['Alternate'].str.split(' \(').str
	arenas_df['Alternate.Capacity'] = arenas_df['Alternate.Capacity'].str.rstrip(')')

	return arenas_df


def get_gameattribs(browser, season=None, metric='Excitement'):
	"""
	Scrapes the Game Attributes tables (https://kenpom.com/game_attrs.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2010 is the earliest available season. Current
				season is the default.
			metric (str, optional): Used to get highest ranking games for different metrics. Available values are:
				'Excitement', 'Tension', 'Dominance', 'ComeBack', 'FanMatch', 'Upsets', and 'Busts'. Default is
				'Excitement'. 'FanMatch', 'Upsets', and 'Busts' are only valid for seasons after 2010.

	Returns:
			ga_df (pandas dataframe): Pandas dataframe containing the Game Attributes table from kenpom.com for a
				given metric.

	Raises:
			ValueError: If `season` is less than 2010.
			KeyError: If `metric` is invalid.
	"""

	# `metric` parameter checking.
	metric = metric.upper()
	metrics = {'EXCITEMENT': 'Excitement', 'TENSION': 'Tension', 'DOMINANCE': 'Dominance', 'COMEBACK': 'MinWP',
				'FANMATCH': 'FanMatch', 'UPSETS': 'Upsets', 'BUSTS': 'Busts'}
	if metric not in metrics:
		raise KeyError(
			"""Metric is invalid, must be one of: 'Excitement',
				'Tension', 'Dominance', 'ComeBack', 'FanMatch', 'Upsets', and 'Busts'""")
	else:
		met_url = 's=' + metrics[metric]

	url = 'https://kenpom.com/game_attrs.php?' + met_url

	# Season selection and an additional check.
	if season:
		if int(season) < 2010:
			raise ValueError(
				'Season cannot be less than 2010, as data only goes back that far.')
		elif int(season) < 2011 and metric.upper() in ['FANMATCH', 'UPSETS', 'BUSTS']:
			raise ValueError(
				'FanMatch, Upsets, and Busts tables only available for seasons after 2010.'
			)
		url = url + '&y=' + str(season)

	browser.open(url)
	playerstats = browser.get_current_page()

	table = playerstats.find_all('table')[0]
	ga_df = pd.read_html(str(table))

	# Dataframe tidying.
	ga_df = ga_df[0]
	ga_df.columns = ['Rank', 'Date', 'Game', 'Box', 'Location', 'Conf.Matchup', 'Value']
	ga_df = ga_df.drop(['Box'], axis=1)
	ga_df['Location'], ga_df['Arena'] = ga_df['Location'].str.split(' \(').str
	ga_df['Arena'] = ga_df['Arena'].str.rstrip(')')

	return ga_df
