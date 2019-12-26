import pytest
import kenpompy.summary as kpsum
import pandas as pd

def test_get_efficiency(browser):
	expected = ['Louisville', 'ACC', '67.2', '199', '68.3', '217', '17.6', '183', '17.5', '175', '113.7', '28', '107.6',
				'75', '94.4', '24', '98.8', '62']

	df = kpsum.get_efficiency(browser, season = "2019")
	assert [str(i) for i in df[df.Team == "Louisville"].iloc[0].to_list()] == expected

	expected = ['Louisville', 'BE', '65.3', '160', '67.1', '169', '113.1', '40', '107.3', '67', '87.7', '4', '91.2', 
				'7']

	df = kpsum.get_efficiency(browser, season = "2008")
	assert [str(i) for i in df[df.Team == "Louisville"].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_efficiency(browser, season = "2001")


def test_get_fourfactors(browser):
	expected = ['Louisville', 'ACC', '67.2', '199', '113.7', '28', '50.9', '165', '17.4', '106', '29.2', '137', '34.9', '115', 
				'94.4', '24', '46.8', '25', '16.1', '313', '25.9', '74', '32.0', '156']

	df = kpsum.get_fourfactors(browser, season = "2019")
	assert [str(i) for i in df[df.Team == "Louisville"].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_fourfactors(browser, season = "2001")


def test_get_teamstats(browser):
	expected = ['Louisville', 'ACC', '34.2', '177', '50.6', '161', '77.7', '8', '10.6', '272', '8.3', '101', '9.2', 
				'128', '53.6', '122', '43.7', '56']

	df = kpsum.get_teamstats(browser, season = "2019")
	assert [str(i) for i in df[df.Team == "Louisville"].iloc[0].to_list()] == expected

	expected = ['Louisville', 'ACC', '32.0', '53', '46.0', '25', '69.5', '107', '7.9', '234', '6.3', '340', '9.8', 
				'153', '47.9', '70', '37.2', '129']

	df = kpsum.get_teamstats(browser, season = "2019", defense = True)
	assert [str(i) for i in df[df.Team == "Louisville"].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_teamstats(browser, season = "2001")

