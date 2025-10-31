import pytest
import kenpompy.misc as kpmisc

def test_get_current_season(browser):
	current_season = kpmisc.get_current_season(browser)

	# Test that the current season is indeed published on the homepage
	assert browser.request(url='https://kenpom.com/?y=' + str(current_season), method='GET', allow_redirects=False).status_code == 200

	# Test that there are isn't a season beyond the "current" one (that it is indeed the latest)
	assert browser.request(url='https://kenpom.com/?y=' + str(current_season + 1), method='GET', allow_redirects=False).status_code == 302

def test_get_pomeroy_ratings(browser):
    expected = ['1', 'Virginia', 'ACC', '35-3', '+34.22', '123.4', '2', '89.2', '5', '59.4', '353', '+.050', '62', '+11.18', '22', '109.2', '34', '98.1', '14', '-3.24', '255', '1']
    df = kpmisc.get_pomeroy_ratings(browser, season=2019)
    assert df.iloc[0].to_list() == expected

    expected = ['253', 'Cal St. Northridge', 'BW', '13-21', '-7.74', '104.8', '170', '112.5', '318', '70.9', '43', '-.018', '232', '-4.63', '263', '101.7', '282', '106.3', '225', '-4.09', '279', '']
    assert df.loc[252].to_list() == expected

    # Also test proper handling of team names with special characters like ' and &
    expected = ['31', "Saint Mary's", 'WCC', '22-12', '+17.31', '114.7', '23', '97.4', '55', '62.7', '348', '-.045', '285', '+3.66', '82', '106.6', '76', '103.0', '100', '-0.90', '183', '11']
    assert df.iloc[30].to_list() == expected

	# Shape test to ensure header rows are correctly filtered
    expected = (353, 22)
    assert df.shape == expected

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
	df = kpmisc.get_program_ratings(browser)
	expected = (364, 17)
	assert df.shape[1] == expected[1]