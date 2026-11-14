"""
This module contains functions for scraping the team page kenpom.com tables into
pandas dataframes
"""

import pandas as pd
from io import StringIO
from .misc import get_current_season
import re
import json
from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
from typing import Optional
from .utils import get_html

def get_valid_teams(browser: CloudScraper, season: Optional[str]=None):
	"""
	Scrapes the teams (https://kenpom.com) into a list.

	Args:
		browser (CloudScraper): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		season (str, optional): Used to define different seasons. 1999 is the earliest available season.

	Returns:
		team_list (list): List containing all valid teams for the given season on kenpom.com.
	"""

	url = "https://kenpom.com"
	url = url + '?y=' + str(season)

	teams = BeautifulSoup(get_html(browser, url), "html.parser")
	table = teams.find_all('table')[0]
	team_df = pd.read_html(StringIO(str(table)))
	# Get only the team column.
	team_df = team_df[0].iloc[:, 1]
 	# Remove NCAA tourny seeds for previous seasons.
	team_df = team_df.str.replace(r'\d+\**', '', regex=True)
	team_df = team_df.str.rstrip()
	team_df = team_df.dropna()
	# Remove leftover team headers
	team_list = team_df.values.tolist()
	team_list = [team for team in team_df if team != "Team"]

	return team_list

def get_schedule(browser: CloudScraper, team: Optional[str]=None, season: Optional[str]=None):
	"""
	Scrapes a team's schedule from (https://kenpom.com/team.php) into a dataframe.

	Args:
		browser (CloudScraper): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		team (str, optional): Used to determine which team to scrape for schedule.
		season (str, optional): Used to define different seasons. 1999 is the earliest available season.

	Returns:
		team_df (pandas dataframe): Dataframe containing a team's schedule for the given season.

	Raises:
		ValueError if `season` is less than 1999.
		ValueError if `season` is greater than the current year.
		ValueError if `team` is not in the valid team list.
	"""

	url = 'https://kenpom.com/team.php'
	current_season = get_current_season(browser)

	if season:
		if int(season) < 1999:
			raise ValueError(
				'season cannot be less than 1999, as data only goes back that far.')
		if int(season) > int(current_season):
			raise ValueError(
				'season cannot be greater than the current year.')
	else:
		season = current_season

	if team==None or team not in get_valid_teams(browser, season):
			raise ValueError(
				'the team does not exist in kenpom in the given year.  Check that the spelling matches (https://kenpom.com) exactly.')
	
	# Sanitize team name
	team = team.replace(" ", "+")
	team = team.replace("&", "%26")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	schedule = BeautifulSoup(get_html(browser, url), "html.parser")
	table = schedule.find_all('table')[1]
	schedule_df = pd.read_html(StringIO(str(table)))

	# Dataframe Tidying
	schedule_df = schedule_df[0]
	# Teams 2010 and earlier do not show their team rank, add column for consistency
	if(len(schedule_df.columns) == 10):
		schedule_df.insert(1, 'Team Rank', '')
	schedule_df.columns = ['Date', 'Team Rank', 'Opponent Rank', 'Opponent Name', 'Result', 'Possession Number',
					  'A', 'Location', 'Record', 'Conference', 'B']
	schedule_df = schedule_df.drop(columns = ['A', 'B'])
	schedule_df = schedule_df.fillna('')

	# Add postseason tournament info to a distinct column
	schedule_df['Postseason'] = None
	# Enumerate tournament names and their row indices
	postseason_labels = schedule_df[(schedule_df['Team Rank'].str.contains('Tournament')) | (schedule_df['Team Rank'].str.contains('Postseason'))].reset_index()[['index', 'Date']].values.tolist()
	# Tournament name preprocessing
	postseason_labels = list(map(lambda x: [x[0], re.sub(r'(?:\sConference)?\sTournament.*?$', '', x[1])], postseason_labels))
	# Loop tournaments in schedule and apply to associated games
	i = 0
	while i < len(postseason_labels):
		if i != len(postseason_labels) - 1:
			schedule_df.loc[postseason_labels[i][0]:postseason_labels[i+1][0]-1, 'Postseason'] = postseason_labels[i][1]
		else:
			schedule_df.loc[postseason_labels[i][0]:, 'Postseason'] = postseason_labels[i][1]
		i += 1
	# Remove table data not corresponding to a scheduled competition
	schedule_df = schedule_df[schedule_df['Date'] != schedule_df['Result']]
	schedule_df = schedule_df[schedule_df['Date'] != 'Date']

	return schedule_df.reset_index(drop=True)

def get_scouting_report(browser: CloudScraper, team: str, season: Optional[int]=None, conference_only: bool=False):
	"""
    Retrieves and parses team scouting report data from (https://kenpom.com/team.php) into a dictionary.

    Args:
    	browser (CloudScraper): The mechanize browser object for web scraping.
    	team (str): team: Used to determine which team to scrape for schedule.
    	season (int, optional): Used to define different seasons. 1999 is the earliest available season.
    	conference_only (bool, optional): When True, only conference-related stats are retrieved; otherwise, all stats are fetched.

    Returns:
    	dict: A dictionary containing various team statistics.

    Raises:
    	ValueError if the provided season is earlier than 1999 or greater than the current year
		ValueError if the team name is invalid or not found in the specified year
	"""

	url = 'https://kenpom.com/team.php'

	current_season = get_current_season(browser)

	if season:
		if int(season) < 1999:
			raise ValueError(
				'season cannot be less than 1999, as data only goes back that far.')
		if int(season) > current_season:
			raise ValueError(
				'season cannot be greater than the current year.')
	else:
		season = int(current_season)

	if team==None or team not in get_valid_teams(browser, season):
			raise ValueError(
				'the team does not exist in kenpom in the given year.  Check that the spelling matches (https://kenpom.com) exactly.')
	
	# Sanitize team name
	team = team.replace(" ", "+")
	team = team.replace("&", "%26")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	html = get_html(browser, url).decode('utf-8', errors='replace')

	# The page embeds the stats as JSON in `allData` (all games) and `confData` (conference games).
	data_name = 'confData' if conference_only else 'allData'
	match = re.search(r'const\s+' + data_name + r'\s*=\s*', html)
	if match is None:
		raise ValueError(f'Could not find {data_name} on the scouting report page.')
	data, _ = json.JSONDecoder().raw_decode(html, match.end())

	# Maps the returned stat names to the keys used in the embedded data.
	stat_keys = {
		'OE': 'AdjOE', 'DE': 'AdjDE', 'Tempo': 'AdjTempo',
		'APLO': 'APL_Off', 'APLD': 'APL_Def',
		'eFG': 'eFG_Pct', 'DeFG': 'OppeFG_Pct',
		'TOPct': 'TO_Pct', 'DTOPct': 'OppTO_Pct',
		'ORPct': 'OR_Pct', 'DORPct': 'OppOR_Pct',
		'FTR': 'FT_Rate', 'DFTR': 'OppFT_Rate',
		'3Pct': 'FG3Pct', 'D3Pct': 'OppFG3Pct',
		'2Pct': 'FG2Pct', 'D2Pct': 'OppFG2Pct',
		'FTPct': 'FTPct', 'DFTPct': 'OppFTPct',
		'BlockPct': 'BlockPct', 'DBlockPct': 'OppBlockPct',
		'StlRate': 'StlRate', 'DStlRate': 'OppStlRate',
		'NSTRate': 'NSTRate', 'DNSTRate': 'OppNSTRate',
		'3PARate': 'F3GRate', 'D3PARate': 'OppF3GRate',
		'ARate': 'ARate', 'DARate': 'OppARate',
		'PD3': 'Off_3', 'DPD3': 'Def_3',
		'PD2': 'Off_2', 'DPD2': 'Def_2',
		'PD1': 'Off_1', 'DPD1': 'Def_1',
	}

	# Stats missing for earlier years default to '' (as before).
	stats_df = {}
	for name, key in stat_keys.items():
		value = data.get(key)
		rank = data.get('Rank' + key)
		if value is None:
			stats_df[name] = ''
		else:
			# Steal rates are stored as fractions but displayed as percentages.
			if key in ('StlRate', 'OppStlRate'):
				value = value * 100
			# Round to match the one-decimal values shown on the page.
			stats_df[name] = round(float(value), 1)
		stats_df[name + '.Rank'] = '' if rank is None else int(rank)
	return stats_df
