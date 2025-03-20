"""
This module contains code to scrape the box page on kenpom.com in order to create pandas
dataframes for boxscores.
"""

import pandas as pd

from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
from .utils import validate_season
from typing import Optional
from .misc import get_current_season, get_html


def get_box_urls_from_schedule(browser: CloudScraper, team):
    url = 'https://kenpom.com/team.php'
    result = []
    team = team.replace(" ", "+")
    team = team.replace("&", "%26")
    url = url + "?team=" + str(team)

    teams_page = BeautifulSoup(get_html(browser, url), "html.parser")
    schedule = teams_page.find("table", id="schedule-table")
    rows = schedule.find("tbody").findAll("tr")
    for row in rows:
        cells = row.findAll("td")
        try:
            result.append(cells[4].contents[0]["href"])
        except Exception as e:
            pass
    return result




def get_box_score(browser: CloudScraper, url: str, season: Optional[str]=None):
    """
    Scrapes the stats and information on a box score page into a dataframe.

    :param browser: A browser object that has been authenticated with a kenpom.com account.
    :param season: The season in which the game occurred, defaults to current.

    :return: box_score_df (pandas dataframe): A dataframe containing the stat information from the game.
    """

    current_season = get_current_season(browser)
    season = validate_season(browser, current_season, season)

