import pytest
import datetime
import kenpompy.conference as kpconf
import pandas as pd

def test_get_valid_conferences(browser):
	expected = 32

	confs_2021 = kpconf.get_valid_conferences(browser, season = '2021')
	assert len(confs_2021) == expected

	valid_2021_confs = ['B12', 'P12', 'Pat']
	for team in valid_2021_confs:
		assert team in confs_2021
	assert confs_2021[0] == 'A10'
	assert confs_2021[-1] == 'WCC'

	confs_2003 = kpconf.get_valid_conferences(browser, season = '2003')
	assert len(confs_2003) == 32

	valid_2003_confs = ['MEAC', 'CAA']
	for team in valid_2003_confs:
		assert team in confs_2003
	assert confs_2003[0] == 'A10'
	assert confs_2003[-1] == 'ind'


def test_get_aggregate_stats(browser):
	expectedTempo = 67.9
	expectedTempoRank = 20
	expectedHomeWinPercent = 60.3
	expectedHomeWinPercentRank = 8

	confs_2021 = kpconf.get_aggregate_stats(browser, 'B10', season = '2021')
	assert confs_2021.loc['Tempo', 'Value'] == expectedTempo
	assert confs_2021.loc['Tempo', 'Rank'] == expectedTempoRank
	assert confs_2021.loc['Home win%', 'Value'] == expectedHomeWinPercent
	assert confs_2021.loc['Home win%', 'Rank'] == expectedHomeWinPercentRank
	
	expectedTempo = 65.5
	expectedTempoRank = 27
	expectedHomeWinPercent = 71.6
	expectedHomeWinPercentRank = 2

	confs_2003 = kpconf.get_aggregate_stats(browser, 'B10', season = '2003')
	assert confs_2003.loc['Tempo', 'Value'] == expectedTempo
	assert confs_2003.loc['Tempo', 'Rank'] == expectedTempoRank
	assert confs_2003.loc['Home win%', 'Value'] == expectedHomeWinPercent
	assert confs_2003.loc['Home win%', 'Rank'] == expectedHomeWinPercentRank

	expectedTempo = 67
	expectedTempoRank = 28

	confs_2021 = kpconf.get_aggregate_stats(browser, season = '2021')
	assert confs_2021.loc['AE', 'Tempo'] == expectedTempo
	assert confs_2021.loc['AE', 'Tempo.Rank'] == expectedTempoRank

	expectedTempo = 67.2
	expectedTempoRank = 20

	confs_2003 = kpconf.get_aggregate_stats(browser, season = '2003')
	assert confs_2003.loc['AE', 'Tempo'] == expectedTempo
	assert confs_2003.loc['AE', 'Tempo.Rank'] == expectedTempoRank


def test_get_standings(browser):
	expectedTeam1 = 'Michigan'
	expectedTeam1AdjO = 117.6
	expectedTeam1AdjORank = 9
	
	confs_2021 = kpconf.get_standings(browser, 'B10', season = '2021')
	assert confs_2021.iloc[0, :]['Team'] == expectedTeam1
	assert confs_2021.iloc[0, :]['AdjO'] == expectedTeam1AdjO
	assert confs_2021.iloc[0, :]['AdjO.Rank'] == expectedTeam1AdjORank

	expectedTeam1 = 'Wisconsin'
	expectedTeam1AdjO = 114.4
	expectedTeam1AdjORank = 16	

	confs_2003 = kpconf.get_standings(browser, 'B10', season = '2003')
	assert confs_2003.iloc[0, :]['Team'] == expectedTeam1
	assert confs_2003.iloc[0, :]['AdjO'] == expectedTeam1AdjO
	assert confs_2003.iloc[0, :]['AdjO.Rank'] == expectedTeam1AdjORank


def test_get_offense(browser):
	expectedTeam1 = 'Iowa'
	expectedTeam1Tempo = 69
	expectedTeam1TempoRank = 4
	
	confs_2021 = kpconf.get_offense(browser, 'B10', season = '2021')
	assert confs_2021.iloc[0, :]['Team'] == expectedTeam1
	assert confs_2021.iloc[0, :]['Tempo'] == expectedTeam1Tempo
	assert confs_2021.iloc[0, :]['Tempo.Rank'] == expectedTeam1TempoRank

	expectedTeam1 = 'Wisconsin'
	expectedTeam1Tempo = 61.5
	expectedTeam1TempoRank = 11	

	confs_2003 = kpconf.get_offense(browser, 'B10', season = '2003')
	assert confs_2003.iloc[0, :]['Team'] == expectedTeam1
	assert confs_2003.iloc[0, :]['Tempo'] == expectedTeam1Tempo
	assert confs_2003.iloc[0, :]['Tempo.Rank'] == expectedTeam1TempoRank


def test_get_defense(browser):
	expectedTeam1 = 'Michigan'
	expectedTeam1Stl = 6.4
	expectedTeam1StlRank = 12
	
	confs_2021 = kpconf.get_defense(browser, 'B10', season = '2021')
	assert confs_2021.iloc[0, :]['Team'] == expectedTeam1
	assert confs_2021.iloc[0, :]['Stl%'] == expectedTeam1Stl
	assert confs_2021.iloc[0, :]['Stl%.Rank'] == expectedTeam1StlRank

	expectedTeam1 = 'Illinois'
	expectedTeam1Stl = 9.7
	expectedTeam1StlRank = 6

	confs_2003 = kpconf.get_defense(browser, 'B10', season = '2003')
	assert confs_2003.iloc[0, :]['Team'] == expectedTeam1
	assert confs_2003.iloc[0, :]['Stl%'] == expectedTeam1Stl
	assert confs_2003.iloc[0, :]['Stl%.Rank'] == expectedTeam1StlRank
