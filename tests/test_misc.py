import pytest
import kenpompy.misc as kpmisc
import pandas as pd

def test_get_trends(browser):
	expected = ('  Season Efficiency Tempo  eFG%   TO%   OR% FTRate   2P%   3P%  3PA%   FT%    A% Blk% Stl% NST% AvgHt'
				'  Cont HomeWin%   PPG\n1   2019      103.2  69.0  50.7  18.5  28.4   33.0  50.1  34.4  38.7  70.7'
				'  51.9  9.3  8.9  9.7  76.8  47.8     59.0  71.9')
	df = kpmisc.get_trends(browser)
	assert df[df.Season == "2019"].to_string() == expected


def test_get_refs(browser):
	expected = ('   Rank          Name  Rating  Games Last Game                                     Game Score\n1     2'
				'  Keith Kimble   67.08    107   Sat 4/6  1 Virginia 63, 11 Auburn 62 (Minneapolis, MN)')
	df = kpmisc.get_refs(browser, season = "2019")
	assert df[df.Name == "Keith Kimble"].to_string() == expected


def test_get_hca(browser):
	expected = ('           Team Conference  HCA HCA.Rank    PF PF.Rank  Pts Pts.Rank   NST NST.Rank  Blk Blk.Rank Elev'
				' Elev.Rank\n120  Louisville        ACC  3.4      119  -4.1      44  4.5      269  -2.1       14  1.1  '
				'    228  400       185')
	df = kpmisc.get_hca(browser)
	assert df[df.Team == "Louisville"].to_string() == expected


def test_get_program_ratings(browser):
	expected = (352, 16)
	df = kpmisc.get_programs_ratings(browser)
	assert df.shape == expected