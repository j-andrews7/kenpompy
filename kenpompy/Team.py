"""
This module contains the Team class for scraping the Team kenpom.com pages into more
usable objects with pandas dataframes as attributes.
"""

import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup

class Team:

	url = 'https://kenpom.com/team.php'

	def __init__(self, name, browser, season=None, conf=False):
		self.name = name
		self.url = url + '?team=' + self.name
		self.season = season

		if self.season:
			if int(self.season) < 2002:
				raise ValueError(
					'season cannot be less than 2002, as data only goes back that far.')
			self.url = self.url + '?y=' + str(self.season)

		browser.open(self.url)
		self.page = browser.get_current_page()

		# Parse title information.
		self.parse_title(page)


	def parse_title(self, page):
		coach = page.find_all(class_ = "coach")[0]
		coach = coach.get_text()
		self.coach = coach.lstrip('Head coach: ')

		info = page.find_all(id = "title-container")[0]
		info = info.get_text()
		info = info.split("\n")[2]
		self.mascot = info.split(' · ')[0]
		self.location = info.split(' · ')[1]

		title = page.find_all("h5")[0]
		title = title.get_text()
		self.rank = title.split()[0]
		self.record = title.split()[-1]
		self.wins = record.strip('()').split('-')[0]
		self.losses = record.strip('()').split('-')[1]

		conference = page.find_all(class_ = "otherinfo")[0]
		conference = conference.get_text()
		self.conference = conference.split("\n")[0]
