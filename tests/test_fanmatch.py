import os
from kenpompy.FanMatch import FanMatch


def load_html_file(filename):
    """Load HTML content from test files."""
    file_path = os.path.join(os.path.dirname(__file__), "html_dumps", filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def test_fanmatch_past_games_basic(browser):
    """Test basic attributes for completed games."""
    html_content = load_html_file("20251103_fm.html")
    fm = FanMatch(browser, date="2025-11-03", html_str=html_content)

    assert fm.date == "2025-11-03"
    assert fm.url == "https://kenpom.com/fanmatch.php?d=2025-11-03"
    assert fm.fm_df is not None
    assert len(fm.fm_df) > 0


def test_fanmatch_dataframe_structure(browser):
    """Test that the dataframe has all expected columns."""
    html_content = load_html_file("20251103_fm.html")
    fm = FanMatch(browser, date="2025-11-03", html_str=html_content)
    df = fm.fm_df
    assert df is not None

    expected_columns = [
        "Game",
        "Team1",
        "Team2",
        "Team1Rank",
        "Team2Rank",
        "Conference",
        "PredictedWinner",
        "PredictedLoser",
        "PredictedScore",
        "WinProbability",
        "PredictedPossessions",
        "PredictedMOV",
        "ThrillScore",
        "ThrillScoreRank",
        "Tournament",
        "City",
        "State",
        "Arena",
        "Time",
        "Network",
        "OT",
        "Winner",
        "WinnerScore",
        "Loser",
        "LoserScore",
        "ActualMOV",
        "Comeback",
        "ComebackRank",
        "Excitement",
        "ExcitementRank",
        "MVP",
        "Possessions",
    ]

    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"


def test_fanmatch_arizona_florida_game(browser):
    """Test parsing of the Arizona vs Florida game."""
    html_content = load_html_file("20251103_fm.html")
    fm = FanMatch(browser, date="2025-11-03", html_str=html_content)
    df = fm.fm_df
    assert df is not None
    game = df.iloc[0]

    # Game string construction
    assert game["Game"] == "15 Arizona 2 Florida"

    # Team information
    assert game["Team1"] == "Arizona"
    assert game["Team2"] == "Florida"
    assert game["Team1Rank"] == "15"
    assert game["Team2Rank"] == "2"

    # Predictions
    assert game["PredictedWinner"] == "Florida"
    assert game["PredictedLoser"] == "Arizona"
    assert game["PredictedScore"] == "84-79"
    assert game["WinProbability"] == "65%"
    assert game["PredictedPossessions"] == 75.0
    assert game["PredictedMOV"] == 5.0

    # Location
    assert game["City"] == "Las Vegas"
    assert game["State"] == "NV"
    assert game["Arena"] == "T-Mobile Arena"

    # Actual game results
    assert game["OT"] == False
    assert game["Winner"] == "Arizona"
    assert game["WinnerScore"] == 93
    assert game["Loser"] == "Florida"
    assert game["LoserScore"] == 87
    assert game["ActualMOV"] == 6.0

    # Excitement metrics
    assert game["Comeback"] == "12"
    assert game["ComebackRank"] == "5"
    assert game["Excitement"] == "2.19"
    assert game["ExcitementRank"] == "18"

    # MVP
    assert game["MVP"] == "Koa Peat (30p/7r/5a/1b/3s)"

    # Possessions
    assert game["Possessions"] == "82"


def test_fanmatch_overtime_games(browser):
    """Test parsing of overtime games."""
    html_content = load_html_file("20251103_fm.html")
    fm = FanMatch(browser, date="2025-11-03", html_str=html_content)
    df = fm.fm_df
    assert df is not None

    ot_games = df[df["OT"] == True]
    assert len(ot_games) > 0

    ot_game = ot_games.iloc[0]
    assert ot_game["OT"] == True
    assert ot_game["Winner"] is not None
    assert ot_game["Loser"] is not None


def test_fanmatch_summary_statistics(browser):
    """Test that summary statistics are parsed correctly."""
    html_content = load_html_file("20251103_fm.html")
    fm = FanMatch(browser, date="2025-11-03", html_str=html_content)

    assert fm.ppg is not None
    assert fm.avg_eff is not None
    assert fm.pos_40 is not None
    assert fm.mean_abs_err_pred_total_score is not None
    assert fm.bias_pred_total_score is not None
    assert fm.mean_abs_err_pred_mov is not None
    assert fm.record_favs is not None
    assert fm.expected_record_favs is not None
    assert fm.exact_mov is not None

    # Test that values are reasonable types
    assert isinstance(fm.ppg, float)
    assert isinstance(fm.avg_eff, float)
    assert isinstance(fm.pos_40, float)
    assert isinstance(fm.record_favs, str)
    assert "-" in fm.record_favs


def test_fanmatch_lines_of_night(browser):
    """Test that lines of the night are parsed."""
    html_content = load_html_file("20251103_fm.html")
    fm = FanMatch(browser, date="2025-11-03", html_str=html_content)

    if fm.lines_of_night is not None:
        assert isinstance(fm.lines_of_night, list)
        assert len(fm.lines_of_night) > 0
        for line in fm.lines_of_night:
            assert isinstance(line, str)
            assert len(line) > 0


def test_fanmatch_future_games_basic(browser):
    """Test basic attributes for future games."""
    html_content = load_html_file("20251210_fm.html")
    fm = FanMatch(browser, date="2025-12-10", html_str=html_content)

    assert fm.date == "2025-12-10"
    assert fm.url == "https://kenpom.com/fanmatch.php?d=2025-12-10"
    assert fm.fm_df is not None
    assert len(fm.fm_df) > 0


def test_fanmatch_future_game_structure(browser):
    """Test that future games have predictions but no results."""
    html_content = load_html_file("20251210_fm.html")
    fm = FanMatch(browser, date="2025-12-10", html_str=html_content)
    df = fm.fm_df
    assert df is not None

    regular_games = df[df["PredictedWinner"].notna()]
    assert len(regular_games) > 0

    game = regular_games.iloc[0]

    # Should have predictions
    assert game["PredictedWinner"] is not None
    assert game["PredictedScore"] is not None
    assert game["WinProbability"] is not None

    # Should NOT have actual results
    assert game["Winner"] is None
    assert game["WinnerScore"] is None
    assert game["Loser"] is None
    assert game["LoserScore"] is None
    assert game["ActualMOV"] is None
    assert game["Comeback"] is None
    assert game["Excitement"] is None
    assert game["MVP"] is None
    assert game["Possessions"] is None


def test_fanmatch_wisconsin_nebraska_game(browser):
    """Test parsing of the Wisconsin at Nebraska game."""
    html_content = load_html_file("20251210_fm.html")
    fm = FanMatch(browser, date="2025-12-10", html_str=html_content)
    df = fm.fm_df
    assert df is not None

    game = df[df["Game"] == "18 Wisconsin at 50 Nebraska"].iloc[0]

    # Team information
    assert game["Team1"] == "Wisconsin"
    assert game["Team2"] == "Nebraska"
    assert game["Team1Rank"] == "18"
    assert game["Team2Rank"] == "50"

    # Conference
    assert game["Conference"] == "B10"

    # Predictions
    assert game["PredictedWinner"] == "Wisconsin"
    assert game["PredictedLoser"] == "Nebraska"
    assert game["PredictedScore"] == "79-78"
    assert game["WinProbability"] == "55%"
    assert game["PredictedPossessions"] == 72.0
    assert game["PredictedMOV"] == 1.0

    # Thrill score
    assert game["ThrillScore"] == "78.0"
    assert game["ThrillScoreRank"] == "1"

    # Location
    assert game["City"] == "Lincoln"
    assert game["State"] == "NE"
    assert game["Arena"] == "Pinnacle Bank Arena"

    # Time/network
    assert game["Time"] == "9:00 pm"
    assert game["Network"] == "Big Ten Network"

    # No actual results
    assert game["Winner"] is None
    assert game["WinnerScore"] is None


def test_fanmatch_future_exhibition_games(browser):
    """Test parsing of future exhibition games."""
    html_content = load_html_file("20251210_fm.html")
    fm = FanMatch(browser, date="2025-12-10", html_str=html_content)
    df = fm.fm_df
    assert df is not None

    exhibition_games = df[df["Team2Rank"].isna()]

    if len(exhibition_games) > 0:
        exh_game = exhibition_games.iloc[0]

        # Exhibition games should have no predictions
        assert exh_game["PredictedWinner"] is None
        assert exh_game["PredictedScore"] is None
        assert exh_game["ThrillScore"] == "0.0"


def test_fanmatch_no_games_day(browser):
    """Test handling of a day with no games."""
    html_content = load_html_file("20251225_fm.html")
    fm = FanMatch(browser, date="2025-12-25", html_str=html_content)
    assert fm.fm_df is None


def test_fanmatch_conference_games(browser):
    """Test that conference games are properly identified."""
    html_content = load_html_file("20251210_fm.html")
    fm = FanMatch(browser, date="2025-12-10", html_str=html_content)
    df = fm.fm_df
    assert df is not None

    conf_games = df[df["Conference"].notna()]
    if len(conf_games) > 0:
        assert all(isinstance(conf, str) for conf in conf_games["Conference"])
