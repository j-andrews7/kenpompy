import pytest
import kenpompy.misc as kpmisc
import pandas as pd
import os

def test_get_trends(browser):
	expected = ('  Season Efficiency Tempo  eFG%   TO%   OR% FTRate   2P%   3P%  3PA%   FT%    A% Blk% Stl% NST% AvgHt'
				'  Cont HomeWin%   PPG\n1   2019      103.2  69.0  50.7  18.5  28.4   33.0  50.1  34.4  38.7  70.7'
				'  51.9  9.3  8.9  9.7  76.8  47.8     59.0  71.9')
	print(os.environ["EMAIL"])
	print(os.environ["PASSWORD"])
	df = kpmisc.get_trends(browser)
	assert df.to_string() == expected