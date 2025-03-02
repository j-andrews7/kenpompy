"""
This module contains functions for scraping the team page kenpom.com tables into
pandas dataframes
"""

import pandas as pd
from io import StringIO
from .misc import get_current_season
import re
from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
from codecs import encode, decode
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

	report = BeautifulSoup(get_html(browser, url), "html.parser")
	scouting_report_scripts = report.find("script", { "type": "text/javascript", "src": ""} )

	extraction_pattern = re.compile(r"\$\(\"td#(?P<token>[A-Za-z0-9]+)\"\)\.html\(\"(.+)\"\);")
	if conference_only:
		pattern = re.compile(r"\$\(':checkbox'\).click\(function\(\) \{([^\}]+)}")
	else:
		pattern = re.compile(r"function tableStart\(\) \{([^\}]+)}")

	stats = extraction_pattern.findall(decode(encode(pattern.search(str(scouting_report_scripts.contents[0])).groups()[0], 'latin-1', 'backslashreplace'), 'unicode-escape'))
	stats = list(map(lambda x: (x[0], float(BeautifulSoup(x[1], "lxml").find('a').contents[0]), int(str(BeautifulSoup(x[1], "lxml").find('span', { "class": "seed" }).contents[0]))), stats[2:]))
	# Defaulting each stat to '' for earlier years which might not have all the stats
	stats_df = {'OE': '', 'OE.Rank': '', 'DE': '', 'DE.Rank': '', 'Tempo': '', 'Tempo.Rank': '', 'APLO': '', 'APLO.Rank': '', 'APLD': '', 'APLD.Rank': '', 'eFG': '', 'eFG.Rank': '', 'DeFG': '', 'DeFG.Rank': '', 'TOPct': '', 'TOPct.Rank': '', 'DTOPct': '', 'DTOPct.Rank': '', 'ORPct': '', 'ORPct.Rank': '', 'DORPct': '', 'DORPct.Rank': '', 'FTR': '', 'FTR.Rank': '', 'DFTR': '', 'DFTR.Rank': '', '3Pct': '', '3Pct.Rank': '', 'D3Pct': '', 'D3Pct.Rank': '', '2Pct': '', '2Pct.Rank': '', 'D2Pct': '', 'D2Pct.Rank': '', 'FTPct': '', 'FTPct.Rank': '', 'DFTPct': '', 'DFTPct.Rank': '', 'BlockPct': '', 'BlockPct.Rank': '', 'DBlockPct': '', 'DBlockPct.Rank': '', 'StlRate': '', 'StlRate.Rank': '', 'DStlRate': '', 'DStlRate.Rank': '', 'NSTRate': '', 'NSTRate.Rank': '', 'DNSTRate': '', 'DNSTRate.Rank': '', '3PARate': '', '3PARate.Rank': '', 'D3PARate': '', 'D3PARate.Rank': '', 'ARate': '', 'ARate.Rank': '', 'DARate': '', 'DARate.Rank': '', 'PD3': '', 'PD3.Rank': '', 'DPD3': '', 'DPD3.Rank': '', 'PD2': '', 'PD2.Rank': '', 'DPD2': '', 'DPD2.Rank': '', 'PD1': '', 'PD1.Rank': '', 'DPD1': '', 'DPD1.Rank': ''}	
	for stat in stats:
		stats_df[stat[0]] = stat[1]
		stats_df[stat[0]+'.Rank'] = stat[2]
	return stats_df

def get_player_stats(browser: CloudScraper, team: str, season: Optional[int]=None, conference_only: bool=False):

	url = 'https://kenpom.com/team.php'

	validate_arguments(browser, team, season)

	# Sanitize team name
	team = team.replace(" ", "+")
	team = team.replace("&", "%26")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	players = BeautifulSoup(get_html(browser, url), "html.parser")
	table = players.find("table", id="player-table")
	player_df = pd.read_html(StringIO(str(table)))[0]
	player_df = player_df.rename(columns={'Unnamed: 0': 'Number', 'Unnamed: 1': 'Name'})

	player_categories = [
		"Go-to guys (>28% of possessions used)",
		"Major Contributors (24-28% of possessions used)",
		"Significant Contributors (20-24% of possessions used)",
		"Role Players (16-20% of possessions used)",
		"Limited roles (12-16% of possessions used)",
		"Nearly invisible (<12% of possessions used)",
		"Benchwarmers (played in fewer than 10% of team's minutes)"

	]
	player_df = player_df[~player_df["Name"].isin(player_categories)]
	return player_df

def validate_arguments(browser: CloudScraper, team: str, season: Optional[int]=None):
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

	if team == None or team not in get_valid_teams(browser, season):
		raise ValueError(
			'the team does not exist in kenpom in the given year.  Check that the spelling matches (https://kenpom.com) exactly.')

