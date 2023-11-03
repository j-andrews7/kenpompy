"""
This module contains functions for scraping the team page kenpom.com tables into
pandas dataframes
"""

import pandas as pd
import datetime
from io import StringIO
import re
from bs4 import BeautifulSoup
from codecs import encode, decode

def get_valid_teams(browser, season=None):
	"""
	Scrapes the teams (https://kenpom.com) into a list.

	Args:
		browser (mechanicalsoul StatefulBrowser): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		season (str, optional): Used to define different seasons. 2002 is the earliest available season.

	Returns:
		team_list (list): List containing all valid teams for the given season on kenpom.com.
	"""

	url = "https://kenpom.com"
	url = url + '?y=' + str(season)

	browser.open(url)
	teams = browser.get_current_page()
	table = teams.find_all('table')[0]
	team_df = pd.read_html(StringIO(str(table)))
	# Get only the team column.
	team_df = team_df[0].iloc[:, 1]
 	# Remove NCAA tourny seeds for previous seasons.
	team_df = team_df.str.replace(r'\d+', '', regex=True)
	team_df = team_df.str.rstrip()
	team_df = team_df.dropna()
	# Remove leftover team headers
	team_list = team_df.values.tolist()
	team_list = [team for team in team_df if team != "Team"]

	return team_list

def get_schedule(browser, team=None, season=None):
	"""
	Scrapes a team's schedule from (https://kenpom.com/team.php) into a dataframe.

	Args:
		browser (mechanicalsoul StatefulBrowser): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		team: Used to determine which team to scrape for schedule.
		season (str, optional): Used to define different seasons. 2002 is the earliest available season.

	Returns:
		team_df (pandas dataframe): Dataframe containing a team's schedule for the given season.

	Raises:
		ValueError if `season` is less than 2002.
		ValueError if `season` is greater than the current year.
		ValueError if `team` is not in the valid team list.
	"""

	url = 'https://kenpom.com/team.php'

	date = datetime.date.today()
	currentYear = date.strftime("%Y")

	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		if int(season) > int(currentYear):
			raise ValueError(
				'season cannot be greater than the current year.')
	else:
		season = int(currentYear)

	if team==None or team not in get_valid_teams(browser, season):
			raise ValueError(
				'the team does not exist in kenpom in the given year.  Check that the spelling matches (https://kenpom.com) exactly.')
	
	# Sanitize team name
	team = team.replace(" ", "+")
	team = team.replace("&", "%26")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	browser.open(url)
	schedule = browser.get_current_page()
	table = schedule.find_all('table')[1]
	schedule_df = pd.read_html(StringIO(str(table)))

	# Dataframe Tidying
	schedule_df = schedule_df[0]
	schedule_df.columns = ['Date', 'Team Rank', 'Opponent Rank', 'Opponent Name', 'Result', 'Possession Number',
					  'A', 'Location', 'Record', 'Conference', 'B']
	schedule_df = schedule_df.drop(columns = ['A', 'B'])
	schedule_df = schedule_df.fillna('')
	schedule_df = schedule_df[schedule_df['Date'] != schedule_df['Team Rank']]
	schedule_df = schedule_df[schedule_df['Date'] != 'Date']

	return schedule_df

def get_scouting_report(browser, team=None, season=None, conference_only=False):
	url = 'https://kenpom.com/team.php'

	date = datetime.date.today()
	currentYear = date.strftime("%Y")

	if season:
		if int(season) < 2002:
			raise ValueError(
				'season cannot be less than 2002, as data only goes back that far.')
		if int(season) > int(currentYear):
			raise ValueError(
				'season cannot be greater than the current year.')
	else:
		season = int(currentYear)

	if team==None or team not in get_valid_teams(browser, season):
			raise ValueError(
				'the team does not exist in kenpom in the given year.  Check that the spelling matches (https://kenpom.com) exactly.')
	
	# Sanitize team name
	team = team.replace(" ", "+")
	team = team.replace("&", "%26")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	browser.open(url)
	scouting_report_scripts = browser.page.find("script", { "type": "text/javascript", "src": ""} )

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