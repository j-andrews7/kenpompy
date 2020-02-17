import pytest
import kenpompy.misc as kpmisc
from kenpompy.FanMatch import FanMatch
import pandas as pd

def test_get_trends(browser):
	expected = ["2019","103.2","69.0","50.7","18.5","28.4","33.0","50.1","34.4","38.7","70.7","51.9","9.3","8.9","9.7",
				"76.8","47.8","59.0","71.9"]

	df = kpmisc.get_trends(browser)
	assert [str(i) for i in df[df.Season == "2019"].iloc[0].to_list()] == expected


def test_get_refs(browser):
	expected = ["2",
				"Keith Kimble",
				"67.08",
				"107",
				"Sat 4/6",
				"1 Virginia 63, 11 Auburn 62 (Minneapolis, MN)"]
	df = kpmisc.get_refs(browser, season = "2019")
	assert [str(i) for i in df[df.Name == "Keith Kimble"].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpmisc.get_refs(browser, season = "2014")


def test_get_hca(browser):
	expected = len(['Louisville', 'ACC', '3.4', '119', '-4.1','44', '4.5', '269',
		'-2.1', '14', '1.1', '228', '400', '185'])

	df = kpmisc.get_hca(browser)
	assert len(df[df.Team == "Louisville"].iloc[0].to_list()) == expected


def test_get_arenas(browser):
	expected = ["3", "Louisville", "ACC", "KFC Yum! Center", "nan", "22,000", "nan"]

	df = kpmisc.get_arenas(browser, season = "2019")
	assert [str(i) for i in df[df.Team == "Louisville"].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpmisc.get_arenas(browser, season = "2009")


def test_get_gameattribs(browser):
	expected = ["1",
				"Tue Feb 26",
				"126 West Virginia 104, 42 TCU 96 (3OT)",
				"Morgantown, WV",
				"B12",
				"4.08",
				"WVU Coliseum"]
	df = kpmisc.get_gameattribs(browser, season = "2019")
	assert [str(i) for i in df.iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpmisc.get_gameattribs(browser, season = "2009")

	with pytest.raises(KeyError):
		kpmisc.get_gameattribs(browser, season = "2019", metric = "yeet")

	with pytest.raises(ValueError):
		kpmisc.get_gameattribs(browser, season = "2010", metric = "BUSTS")


def test_get_program_ratings(browser):
	expected = (352, 16)

	df = kpmisc.get_program_ratings(browser)
	assert df.shape == expected

