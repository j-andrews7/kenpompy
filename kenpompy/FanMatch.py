"""
This module contains the FanMatch class for scraping the FanMatch pages into more usable objects.
"""

import pandas as pd
import re
from datetime import datetime
from cloudscraper import CloudScraper
from bs4 import BeautifulSoup
from typing import Any, Dict, Optional, List
from .utils import get_html

# TODO : testing
import os


class FanMatch:
    """Object to hold FanMatch page scraping results.

    This class scrapes the kenpom FanMatch page when a new instance is created.

    Args:
        browser (CloudScraper): Authenticated browser with full access to kenpom.com generated
            by the `login` function.
        date (str or None): Date to scrape, in format "YYYY-MM-DD", such as "2020-01-29".

    Attributes:
        url (str): Full url for the page to be scraped.
        date (str): Date to be scraped.
        fm_date (str): Date extracted from fanmatch page.
        lines_of_night (list): List containing lines of the night if games have taken place.
        ppg (float): Average points per game for the day.
        avg_eff (float): Average efficiency for the day.
        pos_40 (float): Possessions per 40 minutes for the day.
        mean_abs_err_pred_total_score (float): The mean absolute error of predicted total score for the day.
        bias_pred_total_score (float): The bias of predicted total score for the day.
        mean_abs_err_pred_mov (float): The mean absolute error of the predicted margin of victory for the day.
        record_favs (str): Record of favorites for the day.
        expected_record_favs (str): Expected record of favorites for the day.
        exact_mov (str): Number of games where margin of victory was accurately predicted out of total played.
        fm_df (pandas dataframe or None): Pandas dataframe containing parsed FanMatch table. If there are no games that day, fm_df will be None.
    """

    def __init__(self, browser: CloudScraper, date: Optional[str] = None):
        self.url = "https://kenpom.com/fanmatch.php"
        self.date = date
        self.fm_date = None
        self.lines_of_night = None
        self.ppg: Optional[float] = None
        self.avg_eff: Optional[float] = None
        self.pos_40: Optional[float] = None
        self.mean_abs_err_pred_total_score: Optional[float] = None
        self.bias_pred_total_score: Optional[float] = None
        self.mean_abs_err_pred_mov: Optional[float] = None
        self.record_favs: Optional[str] = None
        self.expected_record_favs: Optional[str] = None
        self.exact_mov: Optional[str] = None
        self.fm_df = None

        if self.date is not None:
            self.url = self.url + "?d=" + self.date

        # TODO : testing
        local_file_name = (
            f"{date.replace('-', '')}.html" if date is not None else "output.html"
        )
        html_content: str
        if os.path.exists(local_file_name):
            with open(local_file_name, "r") as f:
                html_content = f.read()
            fm = BeautifulSoup(html_content, "html.parser")
            print("READ FROM LOCAL\n\n")
        else:
            fm = BeautifulSoup(get_html(browser, self.url), "html.parser")
            with open(local_file_name, "w") as f:
                f.write(str(fm))
            print("FETCHED\n\n")

        # fm = BeautifulSoup(get_html(browser, self.url), "html.parser")

        if "Sorry, no games today." in fm.text:
            return

        self.fm_date = self._extract_fm_date(fm)

        if date is not None:
            if not self._validate_date(date, self.fm_date):
                return

        table = fm.find("table", id="fanmatch-table")
        if not table:
            return

        tbody = table.find("tbody")
        if not tbody:
            return

        rows = tbody.find_all("tr")

        games_data = []
        for row in rows:
            game_data = self._parse_game_row(row)
            if game_data:
                games_data.append(game_data)

        if not games_data:
            return

        self.fm_df = pd.DataFrame(games_data)

        self._post_process_df()

        self._parse_summary_stats(fm)

    def _extract_fm_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the date from the fanmatch page."""
        date_div = soup.find("div", class_="lh12")
        if date_div is None:
            return None

        date_text = date_div.get_text()
        date_match = re.search(r"for \w+, (\w+ \d{1,2}[a-z]{2})", date_text)
        if date_match is None:
            return None

        try:
            extracted_date_str = re.sub(r"(st|nd|rd|th)", "", date_match.group(1))
            extracted_date = datetime.strptime(extracted_date_str, "%B %d")
            extracted_mmdd = extracted_date.strftime("%m-%d")
            return extracted_mmdd
        except (ValueError, AttributeError):
            return None

    def _validate_date(self, requested_date: str, fm_date: Optional[str]) -> bool:
        """Validate parsed date matches the requested date."""
        if fm_date is None:
            return False

        try:
            user_mmdd = datetime.strptime(requested_date, "%Y-%m-%d").strftime("%m-%d")
            return fm_date == user_mmdd
        except (ValueError, AttributeError):
            return False

    def _parse_game_row(self, row) -> Optional[Dict]:
        """Parse a single game row from the FanMatch table."""
        cells = row.find_all("td")
        if len(cells) < 5:
            return None

        game_data: Dict[str, Any] = {}

        # Parse game column (teams and rankings)
        game_cell = cells[0]
        game_text = game_cell.get_text(separator=" ", strip=True)

        # Extract team info from the game column
        team_links = game_cell.find_all("a")
        team_info = self._parse_game_teams(game_cell, team_links, game_text)
        game_data["Game"] = self._construct_game_string(team_info)
        game_data.update(team_info)

        # Parse actual game scores if present
        score_info = self._parse_actual_scores(game_cell, game_text)
        game_data.update(score_info)

        # Parse prediction
        prediction_cell = cells[1]
        prediction_text = prediction_cell.get_text(strip=True)
        prediction_data = self._parse_prediction(prediction_text, team_info)
        game_data.update(prediction_data)

        # Parse time
        time_cell = cells[2]
        time_data = self._parse_time(time_cell)
        game_data.update(time_data)

        # Parse location
        location_cell = cells[3]
        location_data = self._parse_location(location_cell)
        game_data.update(location_data)

        # Parse ThrillScore column
        thrill_cell = cells[4]
        thrill_data = self._parse_thrill_score(thrill_cell)
        game_data.update(thrill_data)

        # Parse Comeback column
        if len(cells) > 5:
            comeback_cell = cells[5]
            comeback_data = self._parse_metric_with_rank(comeback_cell)
            game_data["Comeback"] = comeback_data.get("value")
            game_data["ComebackRank"] = comeback_data.get("rank")
        else:
            game_data["Comeback"] = None
            game_data["ComebackRank"] = None

        # Parse Excitement column
        if len(cells) > 6:
            excitement_cell = cells[6]
            excitement_data = self._parse_metric_with_rank(excitement_cell)
            game_data["Excitement"] = excitement_data.get("value")
            game_data["ExcitementRank"] = excitement_data.get("rank")
        else:
            game_data["Excitement"] = None
            game_data["ExcitementRank"] = None

        # Extract MVP if present
        mvp_match = re.search(r"MVP:\s*(.+?)(?:\s+[A-Z]{2,}-T|\s+NCAA|$)", game_text)
        game_data["MVP"] = mvp_match.group(1).strip() if mvp_match else None

        # Extract Tournament info
        tournament_match = re.search(r"([A-Z]{2,}-T|NCAA)$", game_text)
        game_data["Tournament"] = (
            tournament_match.group(1) if tournament_match else None
        )

        conference_span = game_cell.find(
            "span", style=lambda value: value and "color:#f768a1" in value
        )
        game_data["Conference"] = (
            conference_span.get_text(strip=True) if conference_span else None
        )

        return game_data

    def _parse_game_teams(self, game_cell, team_links: List, game_text: str) -> Dict:
        """Parse team information from the game cell."""
        result = {}

        # Get all span elements with seed-gray class for rankings
        rank_spans = game_cell.find_all("span", class_="seed-gray")

        # Extract team names and rankings
        teams = []
        ranks = []

        for link in team_links:
            teams.append(link.get_text(strip=True))

        # If we have fewer teams from links, extract from text
        if len(teams) < 2:
            non_d1_match = re.search(
                r"NR\s+([A-Za-z\s&\'.]+?)\s+(?:vs\.|at)", game_text
            )
            if non_d1_match:
                teams.insert(0, non_d1_match.group(1).strip())

        # Extract rankings
        for span in rank_spans:
            rank_text = span.get_text(strip=True)
            ranks.append(rank_text if rank_text != "NR" else None)

        while len(teams) < 2:
            teams.append(None)
        while len(ranks) < 2:
            ranks.append(None)

        # Store parsed data (keeping original team order)
        result["team1"] = teams[0]
        result["team1_rank"] = ranks[0]
        result["team2"] = teams[1]
        result["team2_rank"] = ranks[1]

        # Determine game location type
        if " vs. " in game_text or " vs." in game_text:
            result["game_type"] = "neutral"
        elif " at " in game_text:
            result["game_type"] = "away"
        else:
            result["game_type"] = None

        # Extract possessions from brackets in game text
        poss_match = re.search(r"\[(\d+)\]", game_text)
        result["actual_possessions"] = (
            float(poss_match.group(1)) if poss_match else None
        )

        return result

    def _construct_game_string(self, team_info: Dict) -> str:
        """Construct the Game string."""
        team1_rank = team_info.get("team1_rank", "NR")
        team1 = team_info.get("team1", "")
        team2_rank = team_info.get("team2_rank", "NR")
        team2 = team_info.get("team2", "")
        game_type = team_info.get("game_type", "")

        # Format ranks
        rank1_str = str(team1_rank) if team1_rank else "NR"
        rank2_str = str(team2_rank) if team2_rank else "NR"

        # Determine separator
        if game_type == "neutral":
            separator = " vs. "
        elif game_type == "away":
            separator = " at "
        else:
            separator = " "

        return f"{rank1_str} {team1}{separator}{rank2_str} {team2}"

    def _parse_prediction(self, prediction_text: str, team_info: Dict) -> Dict:
        """Parse prediction information."""
        result: Dict[str, Any] = {
            "PredictedWinner": None,
            "PredictedScore": None,
            "WinProbability": None,
            "PredictedPossessions": None,
            "PredictedMOV": None,
            "PredictedLoser": None,
        }

        if not prediction_text or prediction_text == "":
            return result

        # Extract predicted winner (team name before the score)
        winner_match = re.search(r"^(.+?)\s+(\d+-\d+)", prediction_text)
        if winner_match:
            result["PredictedWinner"] = winner_match.group(1).strip()
            result["PredictedScore"] = winner_match.group(2)

            scores = result["PredictedScore"].split("-")
            if len(scores) == 2:
                result["PredictedMOV"] = float(int(scores[0]) - int(scores[1]))

        # Extract win probability
        prob_match = re.search(r"\((\d+(?:\.\d+)?%)\)", prediction_text)
        if prob_match:
            result["WinProbability"] = prob_match.group(1)

        # Extract predicted possessions
        poss_match = re.search(r"\[(\d+)\]", prediction_text)
        if poss_match:
            result["PredictedPossessions"] = float(poss_match.group(1))

        # Determine predicted loser
        if result["PredictedWinner"]:
            team1 = team_info.get("team1")
            team2 = team_info.get("team2")
            if team1 == result["PredictedWinner"]:
                result["PredictedLoser"] = team2
            elif team2 == result["PredictedWinner"]:
                result["PredictedLoser"] = team1

        return result

    def _parse_actual_scores(self, game_cell, game_text: str) -> Dict:
        """Parse actual game scores from completed games."""
        result: Dict[str, Any] = {
            "OT": None,
            "Team1Score": None,
            "Team2Score": None,
            "ActualMOV": None,
            "Winner": None,
            "WinnerScore": None,
            "Loser": None,
            "LoserScore": None,
        }

        if "(OT)" in game_text:
            result["OT"] = True

        team_links = game_cell.find_all("a")
        if len(team_links) < 2:
            return result

        scores = []
        for team_link in team_links[:2]:  # Only first 2 team links are team names
            next_text = team_link.next_sibling

            if next_text and isinstance(next_text, str):
                # Extract the score (first 2-3 digit number in this text)
                score_match = re.search(r"\s*(\d{2,3})", next_text)
                if score_match:
                    scores.append(int(score_match.group(1)))

        # Process the scores if we found exactly 2
        if len(scores) == 2:
            result["Team1Score"] = scores[0]
            result["Team2Score"] = scores[1]
            result["ActualMOV"] = float(abs(scores[0] - scores[1]))

            if result["OT"] is None:
                result["OT"] = False

            if scores[0] > scores[1]:
                result["WinnerScore"] = scores[0]
                result["LoserScore"] = scores[1]
            elif scores[1] > scores[0]:
                result["WinnerScore"] = scores[1]
                result["LoserScore"] = scores[0]

        return result

    def _parse_time(self, time_cell) -> Dict:
        """Parse time and network information.

        Note: Some of the rows in the HTML are missing closing `</td>`
        tags. This funciton should account for that but things may still
        bleed through.
        """
        result: Dict[str, Any] = {"Time": None, "Network": None}

        time_link = time_cell.find("a")
        if time_link:
            time_text = time_link.get_text(strip=True)
            if re.match(r"\d+:\d+\s*[ap]m", time_text, re.IGNORECASE):
                result["Time"] = time_text
        else:
            time_text = time_cell.get_text(strip=True)
            time_match = re.match(r"(\d+:\d+\s*[ap]m)", time_text, re.IGNORECASE)
            if time_match:
                result["Time"] = time_match.group(1)

        network_span = time_cell.find("span", class_="seed-gray-block")
        if network_span:
            network_link = network_span.find("a")
            if network_link:
                result["Network"] = network_link.get_text(strip=True)
            else:
                network_text = network_span.get_text(strip=True)
                if network_text and not network_text.strip().isdigit():
                    result["Network"] = network_text

        return result

    def _parse_location(self, location_cell) -> Dict:
        """Parse location information."""
        result: Dict[str, Any] = {"City": None, "State": None, "Arena": None}

        location_parts = []
        for content in location_cell.children:
            if content.name != "a":
                text = content.string if hasattr(content, "string") else str(content)
                if text and text.strip():
                    location_parts.append(text.strip())

        location_text = " ".join(location_parts)

        city_state_match = re.match(r"^([^,]+),\s*([A-Z]{2})", location_text)
        if city_state_match:
            result["City"] = city_state_match.group(1).strip()
            result["State"] = city_state_match.group(2).strip()

        arena_link = location_cell.find("a")
        if arena_link:
            arena_span = arena_link.find("span", class_="win-prob-link")
            if arena_span:
                result["Arena"] = arena_span.get_text(strip=True)

        return result

    def _parse_thrill_score(self, thrill_cell) -> Dict:
        """Parse thrill score and rank."""
        result = {"ThrillScore": None, "ThrillScoreRank": None}

        rank_span = thrill_cell.find("span", class_="seed-gray-block")

        if rank_span:
            rank_text = rank_span.get_text(strip=True)
            result["ThrillScoreRank"] = rank_text

            thrill_score = thrill_cell.find(string=True, recursive=False)
            if thrill_score:
                result["ThrillScore"] = thrill_score.strip()
        else:
            # No rank span found, just get the text
            thrill_text = thrill_cell.get_text(strip=True)
            result["ThrillScore"] = thrill_text if thrill_text else None

        return result

    def _parse_metric_with_rank(self, cell) -> Dict:
        """Parser for comeback and excitement metrics."""
        result: Dict[str, Any] = {"value": None, "rank": None}

        if not cell:
            return result

        rank_span = cell.find("span", class_="win-prob-link")
        if rank_span:
            rank_text = rank_span.get_text(strip=True)
            rank_match = re.search(r"·(\d+)·", rank_text)
            if rank_match:
                result["rank"] = rank_match.group(1)

            value = cell.find(string=True, recursive=False)
            if value:
                stripped_value = value.strip()
                result["value"] = stripped_value if stripped_value else None
            return result

        # Fall back TODO : this could be handled better
        rank_span = cell.find("span", class_="seed-gray-block")
        if rank_span:
            rank_text = rank_span.get_text(strip=True)
            result["rank"] = rank_text

            value = cell.find(string=True, recursive=False)
            if value:
                stripped_value = value.strip()
                result["value"] = stripped_value if stripped_value else None
        else:
            text = cell.get_text(strip=True)
            result["value"] = text if text else None

        return result

    def _post_process_df(self) -> None:
        if self.fm_df is None or self.fm_df.empty:
            return

        if "actual_possessions" in self.fm_df.columns:
            self.fm_df["Possessions"] = self.fm_df["actual_possessions"]
            self.fm_df["Possessions"] = self.fm_df["Possessions"].apply(
                lambda x: str(int(x)) if pd.notna(x) else None
            )

        if "team1_rank" in self.fm_df.columns:
            self.fm_df["Team1Rank"] = self.fm_df["team1_rank"]
        if "team2_rank" in self.fm_df.columns:
            self.fm_df["Team2Rank"] = self.fm_df["team2_rank"]

        if "team1" in self.fm_df.columns:
            self.fm_df["Team1"] = self.fm_df["team1"]
        if "team2" in self.fm_df.columns:
            self.fm_df["Team2"] = self.fm_df["team2"]

        # Parse winner/loser information from completed games
        self._parse_game_results()

        # Drop internal helper columns
        columns_to_drop = [
            "team1",
            "Team1Score",
            "team1_rank",
            "team1_score",
            "team2",
            "Team2Score",
            "team2_rank",
            "team2_score",
            "game_type",
            "actual_possessions",
        ]
        self.fm_df = self.fm_df.drop(
            columns=[col for col in columns_to_drop if col in self.fm_df.columns]
        )

        self.fm_df = self.fm_df.reindex(
            columns=[
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
        )

    def _parse_game_results(self) -> None:
        """Parse actual game results for completed games."""
        if self.fm_df is None:
            raise RuntimeError(
                "Calling _parse_game_results before the dataframe has been set"
            )

        for col in [
            "OT",
            "Winner",
            "WinnerScore",
            "Loser",
            "LoserScore",
            "ActualMOV",
        ]:
            if col not in self.fm_df.columns:
                self.fm_df[col] = None

        for idx in self.fm_df.index:
            team1 = self.fm_df.loc[idx, "Team1"]
            team1_score = self.fm_df.loc[idx, "Team1Score"]
            team2 = self.fm_df.loc[idx, "Team2"]
            team2_score = self.fm_df.loc[idx, "Team2Score"]

            if pd.notna(team1_score) and pd.notna(team2_score):
                if pd.to_numeric(team1_score) > pd.to_numeric(team2_score):
                    self.fm_df.loc[idx, "Winner"] = team1
                    self.fm_df.loc[idx, "Loser"] = team2
                else:
                    self.fm_df.loc[idx, "Winner"] = team2
                    self.fm_df.loc[idx, "Loser"] = team1

    def _parse_summary_stats(self, soup: BeautifulSoup) -> None:
        """Parse summary statistics from the bottom of the page."""

        table = soup.find("table", id="fanmatch-table")
        if not table:
            return

        tbody = table.find("tbody")
        if not tbody:
            return

        rows = tbody.find_all("tr")

        # Summary stats are usually in rows that don't follow the standard game format
        # They have specific text patterns like "Lines of the night", "Points per game", etc.
        for row in rows:
            cells = row.find_all("td")
            if not cells:
                continue

            cell_text = cells[0].get_text(strip=True)

            if "the night" in cell_text.lower():
                self._extract_lines_of_night(rows, rows.index(row))
                break

        self._extract_summary_statistics(soup)

    def _extract_lines_of_night(self, rows: List, start_index: int) -> None:
        """Extract lines of the night."""
        lines = []
        for i in range(start_index + 1, len(rows)):
            row = rows[i]
            cells = row.find_all("td")
            if not cells:
                break

            cell_text = cells[0].get_text(strip=True)

            # Stop when we hit summary statistics
            if any(
                keyword in cell_text.lower()
                for keyword in [
                    "points per game",
                    "predicted total score",
                    "predicted margin",
                ]
            ):
                break

            if cell_text:
                lines.append(cell_text)

        if lines:
            self.lines_o_night = lines

    def _extract_summary_statistics(self, soup: BeautifulSoup) -> None:
        """Extract summary statistics."""
        page_text = soup.get_text()

        # Parse points per game stats
        ppg_match = re.search(r"Points per game:\s*(\d+\.?\d*)", page_text)
        if ppg_match:
            self.ppg = float(ppg_match.group(1))

        # Parse average efficiency
        eff_match = re.search(r"Average efficiency:\s*(\d+\.?\d*)", page_text)
        if eff_match:
            self.avg_eff = float(eff_match.group(1))

        # Parse possessions per 40
        pos_match = re.search(r"Possessions per 40:\s*(\d+\.?\d*)", page_text)
        if pos_match:
            self.pos_40 = float(pos_match.group(1))

        # Parse mean absolute error for predicted total score
        mae_score_match = re.search(
            r"Mean absolute error.*?predicted total score.*?:\s*(\d+\.?\d*)",
            page_text,
            re.IGNORECASE,
        )
        if mae_score_match:
            self.mean_abs_err_pred_total_score = float(mae_score_match.group(1))

        # Parse bias for predicted total score
        bias_match = re.search(r"Bias.*?:\s*([-]?\d+\.?\d*)", page_text)
        if bias_match:
            self.bias_pred_total_score = float(bias_match.group(1))

        # Parse mean absolute error for predicted MOV
        mae_mov_match = re.search(
            r"Mean absolute error.*?predicted.*?margin.*?:\s*(\d+\.?\d*)",
            page_text,
            re.IGNORECASE,
        )
        if mae_mov_match:
            self.mean_abs_err_pred_mov = float(mae_mov_match.group(1))

        # Parse record of favorites
        record_match = re.search(r"Record of favorites:\s*(\d+-\d+)", page_text)
        if record_match:
            self.record_favs = record_match.group(1)

        # Parse expected record
        exp_record_match = re.search(
            r"Expected record:\s*(\d+\.?\d*-\d+\.?\d*)", page_text
        )
        if exp_record_match:
            self.expected_record_favs = exp_record_match.group(1)

        # Parse exact MOV
        exact_mov_match = re.search(r"Exact.*?(\d+)/(\d+)", page_text)
        if exact_mov_match:
            self.exact_mov = f"{exact_mov_match.group(1)}/{exact_mov_match.group(2)}"
