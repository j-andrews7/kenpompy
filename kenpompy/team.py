"""
This module contains functions for scraping the team page kenpom.com tables into
pandas dataframes
"""

import mechanicalsoup
import pandas as pd
import re
from bs4 import BeautifulSoup
import datetime


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
	team_df = pd.read_html(str(table))
	# Get only the team column.
	team_df = team_df[0].iloc[:, 1]
 	# Remove NCAA tourny seeds for previous seasons.
	team_df = team_df.str.replace(r'\d+', '')
	team_df = team_df.str.rstrip()
	team_df = team_df.dropna()
	# Remove leftover team headers
	team_list = team_df.values.tolist()
	team_list = [team for team in team_df if team != "Team"]

	return team_list

def get_schedule(browser, team=None, season=None):
	"""
	Scrapes the teams (https://kenpom.com) into a list.

	Args:
		browser (mechanicalsoul StatefulBrowser): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		team: Used to determine which team to scrape for schedule.
		season (str, optional): Used to define different seasons. 2002 is the earliest available season.

	Returns:
		team_list (list): List containing all valid teams for the given season on kenpom.com.

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
	
	# Sanatize team name
	team = team.replace(" ", "+")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	browser.open(url)
	schedule = browser.get_current_page()
	table = schedule.find_all('table')[1]
	schedule_df = pd.read_html(str(table))

	# Dataframe Tidying
	schedule_df = schedule_df[0]
	schedule_df.columns = ['Date', 'Team Rank', 'Opponent Rank', 'Opponent Name', 'Result', 'Possession Number',
					  'A', 'Location', 'Record', 'Conference', 'B']
	schedule_df = schedule_df.drop(columns = ['A', 'B'])
	schedule_df = schedule_df.fillna('')


	print(schedule_df.iloc[10])

	return schedule_df