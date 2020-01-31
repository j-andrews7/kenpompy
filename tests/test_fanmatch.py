import pytest
import kenpompy.misc as kpmisc
from kenpompy.FanMatch import FanMatch
import pandas as pd

def test_fanmatch(browser):
	date = "2020-01-29"

	expected = ["31 Marquette 84, 59 Xavier 82 (2OT)",
 				"Cincinnati, OH Cintas Center",
 				"68.2",
 				"8",
 				"2.96",
 				"2",
 				nan,
 				nan,
 				"Sacar Anim (28p/5r/2a/1b/4s)",
 				"79",
 				"Marquette",
 				"73-72",
 				"51%",
 				1,
 				"2OT",
 				"Xavier",
 				"59",
 				"82",
 				"Marquette",
 				"31",
 				"84",
 				2]

 	fm = FanMatch(browser, date)
 	assert fm.fm_df.iloc[1,].tolist() == expected
 	assert fm.date == "2020-01-29"
 	assert fm.url == 'https://kenpom.com/fanmatch.php?d=2020-01-29'
 	assert fm.lines_o_night == ["1. Max Mahoney, Boston University • 29 pts (11-15 2's, 7-11 FT's) • 10 Rebs (5 Off) • 4 Assists • 3 Stls",
 								"2. Jordan Nwora, Louisville • 37 pts (4-6 2's, 7-14 3's, 8-9 FT's) • 9 Rebs • 1 Stl • 1 Assist",
 								"3. Maceo Jack, George Washington • 35 pts (5-6 2's, 7-13 3's, 4-6 FT's) • 7 Rebs • 2 Blks • 1 Stl"]
 	assert fm.ppg == 71.5
 	assert fm.avg_eff == 101.8
 	assert fm.poss_40 == 68.7
 	assert fm.mean_abs_err_pred_total_score == 15.8
 	assert fm.bias_pred_total_score == -1.8
 	assert fm.mean_abs_err_pred_mov == 7.8
 	assert fm.record_favs == "40-13"
 	assert fm.expected_record_favs == "38-15"
 	assert fm.exact_mov == "1/53"