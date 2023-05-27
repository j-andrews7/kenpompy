"""
This module contains functions for scraping the team stats page table into
pandas dataframes
"""

import pandas as pd
import datetime
import re

def get_team_stats(browser, season=None, defense=False):
	"""
	Scrapes the team-level statistics (https://kenpom.com/teamstats.php) into a DataFrame.

	Args:
		browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		season (str, optional): Used to define different seasons. 2001 is the earliest available season.
		defense (bool): Whether to return defensive stats instead of the default offensive

	Returns:
		teamstats_df (pandas dataframe): A dataframe representation of the requested season's stats
	"""
	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		if int(season) > int(datetime.date.today().strftime("%Y")):
			raise ValueError(
				'season cannot be greater than the current year.')

	url = "https://kenpom.com/teamstats.php?y=" + str(season or '')
	if defense:
		url = url + '&od=d'
		
	browser.open(url)
	teamstats = browser.get_current_page()
	table = teamstats.find('table')
	teamstats_df = pd.read_html(str(table), header=0)[0]
	teamstats_df = teamstats_df[teamstats_df["Team"] != "Team"]
	teamstats_df.columns = teamstats_df.columns.str.replace(r'\.1$', '.Rank', regex=True)
	teamstats_df.reset_index(drop=True, inplace=True)
	
	# Parse NCAA tournament seed from Team name
	teamstats_df[['Team', 'Seed']] = teamstats_df['Team'].str.extract(r'^(?P<Team>[A-Za-z\s]+)(?:\s?(?P<Rank>\d{1,2}))?', expand=True)
	teamstats_df['Team'] = teamstats_df['Team'].str.strip()

	return teamstats_df