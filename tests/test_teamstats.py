import pytest
from kenpompy.teamstats import get_team_stats

def test_get_team_stats(browser):
    team_stats_2022 = get_team_stats(browser, season=2022)
    assert team_stats_2022.shape == (358, 21)
    expected = ['Villanova', 'BE', '35.9', '57', '49.5', '187', '83.0', '1', '11.2', '323', '7.4', '22', '8.1', '83', '48.9', '227', '46.3', '17', '117.5', '9', '2']
    assert team_stats_2022.iloc[56] == expected

    team_stats_2022 = get_team_stats(browser, season=2022, defense=True)
    assert team_stats_2022.shape == (358, 21)
    expected = ['Villanova', 'BE', '30.8', '40', '48.1', '114', '73.4', '276', '6.9', '277', '9.4', '159', '9.0', '186', '49.9', '149', '42.2', '308', '92.9', '23', '2']
    assert team_stats_2022.iloc[39].to_list() == expected
