import pytest
import kenpompy.summary as kpsum

def test_get_efficiency(browser):
	expected = ['Louisville', 'ACC', '67.2', '199', '68.3', '217', '17.6', '183', '17.5', '175', '113.7', '28', '107.6',
				'75', '94.4', '24', '98.8', '62']

	df = kpsum.get_efficiency(browser, season = '2019')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected
	assert df.loc[44]['Team'] == 'Cal St. Northridge'

	expected = ['Louisville', 'BE', '65.3', '160', '67.1', '169', '113.1', '40', '107.3', '67', '87.7', '4', '91.2', 
				'7']

	df = kpsum.get_efficiency(browser, season = '2008')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_efficiency(browser, season = '2001')


def test_get_fourfactors(browser):
	expected = ['Louisville', 'ACC', '67.2', '199', '113.7', '28', '50.9', '165', '17.4', '106', '29.2', '137', '34.9', '115', 
				'94.4', '24', '46.8', '25', '16.1', '313', '25.9', '74', '32.0', '156']

	df = kpsum.get_fourfactors(browser, season = '2019')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_fourfactors(browser, season = '2001')


def test_get_teamstats(browser):
	expected = ['Louisville', 'ACC', '34.2', '177', '50.6', '161', '77.7', '8', '10.6', '272', '8.3', '101', '9.2', 
				'128', '53.6', '122', '43.7', '56', '113.7', '28']

	df = kpsum.get_teamstats(browser, season = '2019')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	expected = ['Louisville', 'ACC', '32.0', '53', '46.0', '25', '69.5', '107', '7.9', '234', '6.3', '340', '9.8', 
				'153', '47.9', '70', '37.2', '129', '94.4', '24']

	df = kpsum.get_teamstats(browser, season = '2019', defense = True)
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_teamstats(browser, season = '2001')


def test_get_pointdist(browser):
	expected = ['Louisville', 'ACC', '21.1', '60', '44.2', '311', '34.8', '105', '19.2', '137', '49.9', '161', '30.9', 
				'211']

	df = kpsum.get_pointdist(browser, season = '2019')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_pointdist(browser, season = '2001')


def test_get_height(browser):
	expected = ['Louisville', 'ACC', '76.8', '181', '+0.6', '87', '+1.3', '44', '-0.1', '190', '-0.1', '189', '-0.9', 
				'272', '-0.5', '233', '2.18', '29', '33.3', '97', '36.7', '273']

	df = kpsum.get_height(browser, season = '2019')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	expected = ['Louisville', 'BE', '77.1', '90', '+2.2', '56', '+1.3', '49', '+0.8', '83', '-0.6', '225', '-0.8', 
				'226', '+0.7', '99', '1.45', '161', '34.8', '66']

	df = kpsum.get_height(browser, season = '2007')
	assert [str(i) for i in df[df.Team == 'Louisville'].iloc[0].to_list()] == expected

	with pytest.raises(ValueError):
		kpsum.get_height(browser, season = '2006')


def test_get_playerstats(browser):
	expected = ['35', 'Montrezl Harrell', 'Louisville', '61.2', '6-8', '235', 'So']

	df = kpsum.get_playerstats(browser, season = '2014')
	assert [str(i) for i in df[df.Player == 'Montrezl Harrell'].iloc[0].to_list()] == expected

	expected = ['2', 'Montrezl Harrell', 'Louisville', '61.2', '6-8', '235', 'So']

	df = kpsum.get_playerstats(browser, season = '2014', conf = "AMER")
	assert [str(i) for i in df[df.Player == 'Montrezl Harrell'].iloc[0].to_list()] == expected

	expected = ['2', 'Montrezl Harrell', 'Louisville', '59.8', '6-8', '235', 'So']

	df = kpsum.get_playerstats(browser, season = '2014', conf = "AMER", conf_only = True)
	assert [str(i) for i in df[df.Player == 'Montrezl Harrell'].iloc[0].to_list()] == expected

	expected = ['22', 'Russ Smith', 'Louisville', '108.9', '6-0', '165', 'Jr', '32.0']

	dfs = kpsum.get_playerstats(browser, season = '2013', metric = "ORTG")
	df = dfs[0]
	assert [str(i) for i in df[df.Player == 'Russ Smith'].iloc[0].to_list()] == expected


	with pytest.raises(ValueError):
		kpsum.get_playerstats(browser, season = '2003')

	with pytest.raises(ValueError):
		kpsum.get_playerstats(browser, season = '2012', conf_only = True)

	with pytest.raises(KeyError):
		kpsum.get_playerstats(browser, metric = "yeet")


def test_get_kpoy(browser):
	expected = ['1', 'Russ Smith', '2.636', '165', 'Jr', 'Briarwood, NY', 'Louisville ', '6-0']

	dfs = kpsum.get_kpoy(browser, season = '2013')
	df = dfs[0]
	assert [str(i) for i in df[df.Player == 'Russ Smith'].iloc[0].to_list()] == expected

	expected = ['10.0', 'Russ Smith', '15', '165', 'Jr', 'Briarwood, NY', 'Louisville ', '6-0']

	df = dfs[1]
	assert [str(i) for i in df[df.Player == 'Russ Smith'].iloc[0].to_list()] == expected

	dfs = kpsum.get_kpoy(browser, season = '2011')
	df = dfs[0]
	assert len(dfs) == 1

	with pytest.raises(ValueError):
		kpsum.get_kpoy(browser, season = '2010')
