"""
This module provides functions for scraping the team kenpom.com pages into more
usable pandas dataframes.
"""

import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup