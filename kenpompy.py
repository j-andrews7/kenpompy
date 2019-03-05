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


def get_efficiency(browser, season=None):
	"""
	Scrapes the Efficiency stats table (https://kenpom.com/summary.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2002 is the earliest available season but 
				possession length data wasn't available until 2010.

	Returns:
			eff_df (pandas dataframe): Pandas dataframe containing the summary efficiency/tempo table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2002.
	"""

	url = 'https://kenpom.com/summary.php'

	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		url = url + '?y=' + season

	browser.open(url)
	eff = browser.get_current_page()
	table = eff.find_all('table')[0]
	eff_df = pd.read_html(str(table))

	# Dataframe tidying.
	eff_df = eff_df[0]

	# Handle seasons prior to 2010 having fewer columns.
	if len(eff_df.columns) == 34:
		eff_df = eff_df.iloc[:, 0:18]
		eff_df.columns = ['Team', 'Conference', 'Tempo-Adj', 'Tempo-Adj.Rank', 'Tempo-Raw', 'Tempo-Raw.Rank',
						  'Avg. Poss Length-Offense', 'Avg. Poss Length-Offense.Rank', 'Avg. Poss Length-Defense',
						  'Avg. Poss Length-Defense.Rank', 'Off. Efficiency-Adj', 'Off. Efficiency-Adj.Rank',
						  'Off. Efficiency-Raw', 'Off. Efficiency-Raw.Rank', 'Def. Efficiency-Adj',
						  'Def. Efficiency-Adj.Rank', 'Def. Efficiency-Raw', 'Def. Efficiency-Raw.Rank']
	else:
		eff_df = eff_df.iloc[:, 0:14]
		eff_df.columns = ['Team', 'Conference', 'Tempo-Adj', 'Tempo-Adj.Rank', 'Tempo-Raw', 'Tempo-Raw.Rank',
						  'Off. Efficiency-Adj', 'Off. Efficiency-Adj.Rank', 'Off. Efficiency-Raw',
						  'Off. Efficiency-Raw.Rank', 'Def. Efficiency-Adj', 'Def. Efficiency-Adj.Rank',
						  'Def. Efficiency-Raw', 'Def. Efficiency-Raw.Rank']

	# Remove the header rows that are interjected for readability.
	eff_df = eff_df[eff_df.Team != 'Team']
	# Remove NCAA tourny seeds for previous seasons.
	eff_df['Team'] = eff_df['Team'].str.replace('\d+', '')
	eff_df['Team'] = eff_df['Team'].str.rstrip()
	eff_df = eff_df.dropna()

	return eff_df


def get_fourfactors(browser, season=None):
	"""
	Scrapes the Four Factors table (https://kenpom.com/stats.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2002 is the earliest available season.

	Returns:
			ff_df (pandas dataframe): Pandas dataframe containing the summary Four Factors table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2002.
	"""

	url = 'https://kenpom.com/stats.php'

	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		url = url + '?y=' + season

	browser.open(url)
	ff = browser.get_current_page()
	table = ff.find_all('table')[0]
	ff_df = pd.read_html(str(table))

	# Dataframe tidying.
	ff_df = ff_df[0]
	ff_df = ff_df.iloc[:, 0:24]
	ff_df.columns = ['Team', 'Conference', 'AdjTempo', 'AdjTempo.Rank', 'AdjOE', 'AdjOE.Rank', 'Off-eFG%',
					 'Off-eFG%.Rank', 'Off-TO%', 'Off-TO%.Rank', 'Off-OR%', 'Off-OR%.Rank', 'Off-FTRate',
					 'Off-FTRate.Rank', 'AdjDE', 'AdjDE.Rank', 'Def-eFG%', 'Def-eFG%.Rank', 'Def-TO%', 'Def-TO%.Rank',
					 'Def-OR%', 'Def-OR%.Rank', 'Def-FTRate', 'Def-FTRate.Rank']

	# Remove the header rows that are interjected for readability.
	ff_df = ff_df[ff_df.Team != 'Team']
	# Remove NCAA tourny seeds for previous seasons.
	ff_df['Team'] = ff_df['Team'].str.replace('\d+', '')
	ff_df['Team'] = ff_df['Team'].str.rstrip()
	ff_df = ff_df.dropna()

	return ff_df


def get_teamstats(browser, defense=False, season=None):
	"""
	Scrapes the Miscellaneous Team Stats table (https://kenpom.com/teamstats.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			defense (bool, optional): Used to flag whether the defensive teamstats table is wanted or not. False by 
				default.
			season (str, optional): Used to define different seasons. 2002 is the earliest available season.
					Retrieves most current season by default.

	Returns:
			ts_df (pandas dataframe): Pandas dataframe containing the Miscellaneous Team Stats table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2002.
	"""

	url = 'https://kenpom.com/teamstats.php'
	last_cols = ['AdjOE', 'AdjOE.Rank']

	# Create URL.
	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		url = url + '?y=' + season
		if defense:
			url = url + '&od=d'
			last_cols = ['AdjDE', 'AdjDE.Rank']
	elif defense:
		url = url + '?od=d'
		last_cols = ['AdjDE', 'AdjDE.Rank']

	browser.open(url)
	ts = browser.get_current_page()
	table = ts.find_all('table')[0]
	ts_df = pd.read_html(str(table))

	# Dataframe tidying.
	ts_df = ts_df[0]
	ts_df = ts_df.iloc[:, 0:18]
	ts_df.columns = ['Team', 'Conference', '3P%', '3P%.Rank', '2P%', '2P%.Rank', 'FT%', 'FT%.Rank',
					 'Blk%', 'Blk%.Rank', 'Stl%', 'Stl%.Rank', 'A%', 'A%.Rank', '3PA%', '3PA%.Rank',
					 last_cols[0], last_cols[1]]

	# Remove the header rows that are interjected for readability.
	ts_df = ts_df[ts_df.Team != 'Team']
	# Remove NCAA tourny seeds for previous seasons.
	ts_df['Team'] = ts_df['Team'].str.replace('\d+', '')
	ts_df['Team'] = ts_df['Team'].str.rstrip()
	ts_df = ts_df.dropna()

	return ts_df


def get_pointdist(browser, season=None):
	"""
	Scrapes the Team Points Distribution table (https://kenpom.com/pointdist.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2002 is the earliest available season.
					Retrieves most current season by default.

	Returns:
			dist_df (pandas dataframe): Pandas dataframe containing the Team Points Distribution table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2002.
	"""

	url = 'https://kenpom.com/pointdist.php'

	# Create URL.
	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		url = url + '?y=' + season

	browser.open(url)
	dist = browser.get_current_page()
	table = dist.find_all('table')[0]
	dist_df = pd.read_html(str(table))

	# Dataframe tidying.
	dist_df = dist_df[0]
	dist_df = dist_df.iloc[:, 0:14]
	dist_df.columns = ['Team', 'Conference', 'Off-FT', 'Off-FT.Rank', 'Off-2P', 'Off-2P.Rank', 'Off-3P', 'Off-3P.Rank',
					   'Def-FT', 'Def-FT.Rank', 'Def-2P', 'Def-2P.Rank', 'Def-3P', 'Def-3P.Rank']

	# Remove the header rows that are interjected for readability.
	dist_df = dist_df[dist_df.Team != 'Team']
	# Remove NCAA tourny seeds for previous seasons.
	dist_df['Team'] = dist_df['Team'].str.replace('\d+', '')
	dist_df['Team'] = dist_df['Team'].str.rstrip()
	dist_df = dist_df.dropna()

	return dist_df


def get_height(browser, season=None):
	"""
	Scrapes the Height/Experience table (https://kenpom.com/height.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2007 is the earliest available season but 
					continuity data wasn't available until 2008.

	Returns:
			h_df (pandas dataframe): Pandas dataframe containing the Height/Experience table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2007.
	"""

	url = 'https://kenpom.com/height.php'

	if season:
		if int(season) < 2007:
			raise ValueError(
				'Season cannot be less than 2007, as data only goes back that far.')
		url = url + '?y=' + season

	browser.open(url)
	height = browser.get_current_page()
	table = height.find_all('table')[0]
	h_df = pd.read_html(str(table))

	# Dataframe tidying.
	h_df = h_df[0]

	# Handle seasons prior to 2008 having fewer columns.
	if len(h_df.columns) == 22:
		h_df = h_df.iloc[:, 0:22]
		h_df.columns = ['Team', 'Conference', 'AvgHgt', 'AvgHgt.Rank', 'EffHgt', 'EffHgt.Rank',
						'C-Hgt', 'C-Hgt.Rank', 'PF-Hgt', 'PF-Hgt.Rank', 'SF-Hgt', 'SF-Hgt.Rank',
						'SG-Hgt', 'SG-Hgt.Rank', 'PG-Hgt', 'PG-Hgt.Rank', 'Experience', 'Experience.Rank',
						'Bench', 'Bench.Rank', "Continuity", "Continuity.Rank"]
	else:
		h_df = h_df.iloc[:, 0:20]
		h_df.columns = ['Team', 'Conference', 'AvgHgt', 'AvgHgt.Rank', 'EffHgt', 'EffHgt.Rank',
						'C-Hgt', 'C-Hgt.Rank', 'PF-Hgt', 'PF-Hgt.Rank', 'SF-Hgt', 'SF-Hgt.Rank',
						'SG-Hgt', 'SG-Hgt.Rank', 'PG-Hgt', 'PG-Hgt.Rank', 'Experience', 'Experience.Rank',
						'Bench', 'Bench.Rank']

	# Remove the header rows that are interjected for readability.
	h_df = h_df[h_df.Team != 'Team']
	# Remove NCAA tourny seeds for previous seasons.
	h_df['Team'] = h_df['Team'].str.replace('\d+', '')
	h_df['Team'] = h_df['Team'].str.rstrip()
	h_df = h_df.dropna()

	return h_df

def get_playerstats(browser, season=None, metric='EFG', conf=None, conf_only=False):
	"""
	Scrapes the Player Leaders tables (https://kenpom.com/playerstats.php) into a dataframe.

	Args:
			browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
				by the `login` function.
			season (str, optional): Used to define different seasons. 2004 is the earliest available season. Current 
				season is the default.
			metric (str, optional): Used to get leaders for different metrics. Available values are: 'ORtg', 'Min', 
				'eFG', 'Poss', 'Shots', 'OR', 'DR', 'TO', 'ARate', 'Blk', 'FTRate', 'Stl', 'TS', 'FC40', 'FD40', '2P', 
				'3P', 'FT'. Default is 'eFG'. 'ORtg' returns a list of four dataframes, as there are four tables: 
				players that used >28% of possessions, >24% of possessions, >20% of possessions, and with no possession 
				restriction.
			conf (str, optional): Used to limit to players in a specific conference. Allowed values are: 'A10', 'ACC',
				'AE', 'AMER', 'ASUN', 'B10', 'B12', 'BE', 'BSKY', 'BSTH', 'BW', 'CAA', 'CUSA', 'HORZ', 'IND', IVY', 
				'MAAC', 'MAC', 'MEAC', 'MVC', 'MWC', 'NEC', 'OVC', 'P12', 'PAT', 'SB', 'SC', 'SEC', 'SLND', 'SUM', 
				'SWAC', 'WAC', 'WCC'. If you try to use a conference that doesn't exist for a given season, like 'IND'
				and '2018', you'll get an empty table, as kenpom.com doesn't serve 404 pages for invalid table queries
				like that. No filter applied by default.
			conf_only (bool, optional): Used to define whether stats should reflect conference games only. Only
				available if specific conference is defined. Only available for seasons after 2013. False by default.


	Returns:
			ps_df (pandas dataframe): Pandas dataframe containing the Player Leaders table from kenpom.com.

	Raises:
			ValueError: If `season` is less than 2004, `metric` is invalid, or `conf_only` is used with an 
				invalid `season`.
	"""

	# `metric` parameter checking.
	metrics = {'ORTG': 'ORtg', 'MIN': 'PctMin', 'EFG': 'eFG', 'POSS': 'PctPoss', 'SHOTS': 'PctShots', 'OR': 'ORPct', 
			   'DR': 'DRPct', 'TO': 'TORate', 'ARATE': 'ARate', 'BLK': 'PctBlocks', 'FTRATE': 'FTRate', 
			   'STL': 'PctStls', 'TS': 'TS', 'FC40': 'FCper40', 'FD40': 'FDper40', '2P': 'FG2Pct', '3P': 'FG3Pct', 
			   'FT': 'FTPct'}
	if metric.upper() not in metrics:
		raise ValueError(
			"""Metric is invalid, must be one of: 'ORtg', 'Min', 'eFG', 'Poss', 'Shots', 'OR', 'DR', 'TO', 'ARate', 
			'Blk', 'FTRate', 'Stl', 'TS', 'FC40', 'FD40', '2P', '3P', 'FT'""")
	else:
		met_url = 's=' + metrics[metric]


	url = 'https://kenpom.com/playerstats.php?' + met_url

	if season:
		if int(season) < 2004:
			raise ValueError(
				'Season cannot be less than 2004, as data only goes back that far.')
		elif int(season) < 2014 & conf_only:
			raise ValueError(
				'Conference only stats only available for seasons after 2013.'
			)
		url = url + '&y=' + season

	if conf_only:
		url = url + '&c=c'

	if conf:
		url = url + '&f=' + conf

	browser.open(url)
	playerstats = browser.get_current_page()
	if metric.upper() == 'ORTG':
		ps_dfs = []
		tables = playerstats.find_all('table')
		for t in tables:
			ps_df = pd.read_html(str(t))
			ps_df = ps_df[0]
			
			# Split ortg column.
			ps_df.columns = ['Rank', 'Player', 'Team', 'ORtg', 'Ht', 'Wt', 'Yr']
			ps_df['ORtg'], ps_df['Poss%'] = ps_df['ORtg'].str.split(' ', 1).str
			ps_df['Poss%'] = ps_df['Poss%'].str.strip('()')

			ps_df = ps_df[ps_df.Rank != 'Rk']
			ps_df = ps_df.dropna()

			ps_dfs.append(ps_df)
		ps_df = ps_dfs
	else:
		perc_mets = ['Min', 'eFG', 'Poss', 'Shots', 'OR', 'DR', 'TO', 'Blk', 'Stl', 'TS', '2P', '3P', 'FT']
		if metric.upper() in perc_mets:
			metric = metric + '%'
		table = playerstats.find_all('table')[0]
		ps_df = pd.read_html(str(table))

		# Dataframe tidying.
		ps_df = ps_df[0]
		ps_df.columns = ['Rank', 'Player', 'Team', metric, 'Ht', 'Wt', 'Yr'] 

		# Remove the header rows that are interjected for readability.
		ps_df = ps_df[ps_df.Rank != 'Rk']
		ps_df = ps_df.dropna()

	return ps_df