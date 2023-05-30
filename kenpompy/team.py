"""
This module contains functions for scraping the team page kenpom.com tables into
pandas dataframes
"""

import pandas as pd
import datetime
import tempfile
import sys

from requests_html import HTMLSession, AsyncHTMLSession
from requests_file import FileAdapter


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

	if team == None or team not in get_valid_teams(browser, season):
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
	schedule_df = pd.read_html(str(table))

	# Dataframe Tidying
	schedule_df = schedule_df[0]
	schedule_df.columns = ['Date', 'Team Rank', 'Opponent Rank', 'Opponent Name', 'Result', 'Possession Number',
						'A', 'Location', 'Record', 'Conference', 'B']
	schedule_df = schedule_df.drop(columns=['A', 'B'])
	schedule_df = schedule_df.fillna('')
	schedule_df = schedule_df[schedule_df['Date'] != schedule_df['Team Rank']]
	schedule_df = schedule_df[schedule_df['Date'] != 'Date']

	return schedule_df


async def get_stats(browser, team=None, season=None, _async=False):
	"""
	Scrapes a team's stats from (https://kenpom.com/team.php) into a dataframe.

	Args:
		browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
			by the `login` function
		team: Used to determine which team to scrape for stats.
		season (str, optional): Used to define different seasons. 2002 is the earliest available season.
		_async (bool, optional): Used to run asynchronous HTMLSession()

	Returns:
		stats_df (pandas dataframe): Dataframe containing a team's stats for the given season.

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

	if team == None or team not in get_valid_teams(browser, season):
		raise ValueError(
			'the team does not exist in kenpom in the given year.  Check that the spelling matches (https://kenpom.com) exactly.')

	# Sanitize team name
	team = team.replace(" ", "+")
	team = team.replace("&", "%26")
	url = url + "?team=" + str(team)
	url = url + "&y=" + str(season)

	browser.open(url)
	team_page = browser.get_current_page()

	# Save page to temporarily
	with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as file:
		file.write(team_page.encode())

	# Correct filename format based on platform
	if sys.platform == 'win32':
		filename = file.name.replace('\\', '//')
	else:
		filename = file.name

	# Open saved paged with requests_html session
	"""
	If _async is True, use AsyncHTMLSession() and 
	await on the session to get() and arender() the html page
	""" 
	if _async:
		sess = AsyncHTMLSession()
		sess.mount('file://', FileAdapter())
		r = await sess.get(f'file:///{filename}')
		await r.html.arender()
	else:
		sess = HTMLSession()
		sess.mount('file://', FileAdapter())
		r = sess.get(f'file:///{filename}')
		r.html.render()
		
	# Create soup object from rendered page
	soup = BeautifulSoup(r.html.html, 'html.parser')

	# Retrieve stats table and parse into DataFrame
	statsTable = soup.findAll('table')[0]
	stats_df = pd.read_html(str(statsTable))[0]

	# DataFrame cleaning, drop repeated column names
	stats_df.drop([3, 8, 15, 18, 22, 26], inplace=True)

	# Split Off/Def stats and rankings into their own columns
	stats_df['OffenseRank'] = stats_df['Offense'].str.split().str[1]
	stats_df['Offense'] = stats_df['Offense'].str.split().str[0]
	stats_df['DefenseRank'] = stats_df['Defense'].str.split().str[1]
	stats_df['Defense'] = stats_df['Defense'].str.split().str[0]

	return stats_df