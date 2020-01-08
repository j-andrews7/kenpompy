"""
This module contains the Team class for scraping the Team kenpom.com pages into more
usable objects with pandas dataframes as attributes.
"""

import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup

class Team:

	BASE_URL = 'https://kenpom.com/team.php'

	def __init__(self, name, browser, season=None):
		self.name = name
		self.url = self.base_url + '?team=' + self.name
		self.season = season

		if self.season:
			if int(self.season) < 2002:
				raise ValueError(
					'season cannot be less than 2002, as data only goes back that far.')
			self.final_url = self.final_url + '?y=' + str(self.season)

		browser.open(self.final_url)
		self.page = browser.get_current_page()

		# Parse title information.
		(self.coach, self.mascot, self.location, self.rank, self.record, self.wins, self.losses,
			self.conference) = self.__parse_title()
		(self.scout_overview_all, self.scout_overview_conf, self.scout_four_factors_all, self.scout_four_factors_conf, 
			self.scout_misc_componenets_all, self.scout_misc_components_conf, self.scout_style_components_all, 
			self.scout_style_components_conf, self.scout_point_distribution_all,
			self.scout_point_distribution_conf, self.scout_sos, self.scout_personnel) = self.__parse_scout()


	def __parse_title(self):
		coach = self.page.find_all(class_ = "coach")[0]
		coach = coach.get_text()
		coach = coach.lstrip('Head coach: ')

		info = self.page.find_all(id = "title-container")[0]
		info = info.get_text()
		info = info.split("\n")[2]
		mascot = info.split(' · ')[0]
		location = info.split(' · ')[1]

		title = self.page.find_all("h5")[0]
		title = title.get_text()
		rank = title.split()[0]
		record = title.split()[-1]
		wins = record.strip('()').split('-')[0]
		losses = record.strip('()').split('-')[1]

		conference = page.find_all(class_ = "otherinfo")[0]
		conference = conference.get_text()
		conference = conference.split("\n")[0]

		return (coach, mascot, location, rank, record, wins, losses, conference)


	def __parse_scout(self):
		drop_these = ['Miscellaneous Components', 'Four Factors', 'Style Components', 'Strength of Schedule', 
			'Point Distribution (% of total points)', 'Personnel', 'Category']
		table = page.find_all(id = "report-table")[0]
		scout_all = pd.read_html(str(table))[0]
		scout_all.columns = ['Category', 'Offense', 'Defense', 'D1 Avg']
		scout_all['Category'] = scout_all['Category'].str.rstrip(":")
		scout_all = scout_all[~scout_all['Category'].isin(drop_these)]
		scout_all['Offense'], scout_all['Offense.Rank'] = scout_all['Offense'].str.split(' ', 1).str
		scout_all['Offense.Rank'] = scout_all['Offense.Rank'].str.strip('yrs ')
		scout_all['Defense'], scout_all['Defense.Rank'] = scout_all['Defense'].str.split(' ', 1).str
		scout_all['Defense.Rank'] = scout_all['Defense.Rank'].str.strip('yrs ')

		# Conference only stats copy.
		scout_conf = scout_all.copy()
		scout_conf = scout_conf[0:18]

		scout_all.loc[0, 'Category'] = 'Adj. Efficiency'
		scout_all.loc[1, 'Category'] = 'Adj. Tempo'

		scout_conf.loc[0, 'Category'] = 'Efficiency'
		scout_conf.loc[1, 'Category'] = 'Tempo'

		scout_all = scout_all.set_index(keys = 'Category')
		scout_conf = scout_conf.set_index(keys = 'Category')

		sos = scout_all[18:21]
		personnel = scout_all.iloc[21:, [0, 3, 2]]
		personnel.columns = ['Metric', 'Rank', 'D1 Avg']
		scout_all = scout_all[0:18]

		# Parse javascript.
		scout_js = page.find_all("script")[5].get_text().split('\n')
		scout_js = [y.strip() for y in scout_js]
		scout_js = [z for z in scout_js if ("html" in z) & ("Text" not in z)]

		met_conf = scout_js[0:35]
		met_all = scout_js[35:]

		met_conf_vals = [x.split('>')[1].rstrip("</a") for x in met_conf]
		met_conf_vals[2] = met_conf[2].split('>')[2].rstrip('</a')
		met_conf_ranks = [x.split('>')[3].rstrip("</span") for x in met_conf]
		met_conf_ranks[2] = met_conf[2].split('>')[4].rstrip('</span')

		met_all_vals = [x.split('>')[1].rstrip("</a") for x in met_all]
		met_all_vals[2] = met_all[2].split('>')[2].rstrip('</a')
		met_all_ranks = [x.split('>')[3].rstrip("</span") for x in met_all]
		met_all_ranks[2] = met_all[2].split('>')[4].rstrip('</span')

		offense = met_all_vals[3::2]
		offense = [met_all_vals[0], met_all_vals[2]] + offense
		offense_rk = met_all_ranks[3::2]
		offense_rk = [met_all_ranks[0], met_all_ranks[2]] + offense_rk

		defense = met_all_vals[4::2]
		defense = [met_all_vals[1], met_all_vals[2]] + defense
		defense_rk = met_all_ranks[4::2]
		defense_rk = [met_all_ranks[1], met_all_ranks[2]] + defense_rk

		scout_all['Offense'] = offense
		scout_all['Offense.Rank'] = offense_rk
		scout_all['Defense'] = defense
		scout_all['Defense.Rank'] = defense_rk

		overview_all = scout_all[0:3]
		four_factors_all = scout_all[3:7]
		misc_componenets_all = scout_all[7:13]
		style_components_all = scout_all[13:15]
		point_distribution_all = scout_all[15:]

		# Conference-only table now.
		offense = met_conf_vals[3::2]
		offense = [met_conf_vals[0], met_conf_vals[2]] + offense
		offense_rk = met_conf_ranks[3::2]
		offense_rk = [met_conf_ranks[0], met_conf_ranks[2]] + offense_rk

		defense = met_conf_vals[4::2]
		defense = [met_conf_vals[1], met_conf_vals[2]] + defense
		defense_rk = met_conf_ranks[4::2]
		defense_rk = [met_conf_ranks[1], met_conf_ranks[2]] + defense_rk

		scout_conf['Offense'] = offense
		scout_conf['Offense.Rank'] = offense_rk
		scout_conf['Defense'] = defense
		scout_conf['Defense.Rank'] = defense_rk

		overview_conf = scout_conf[0:3]
		four_factors_conf = scout_conf[3:7]
		misc_components_conf = scout_conf[7:13]
		style_components_conf = scout_conf[13:15]
		point_distribution_conf = scout_conf[15:]

		return (overview_all, overview_conf, four_factors_all, four_factors_conf, misc_componenets_all, 
			misc_components_conf, style_components_all, style_components_conf, point_distribution_all,
			point_distribution_conf, sos, personnel)



