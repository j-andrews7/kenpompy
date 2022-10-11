"""
This module contains the FanMatch class for scraping the FanMatch pages into more usable objects.
"""

import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup

class FanMatch:
    """Object to hold FanMatch page scraping results.
    
    This class scrapes the kenpom FanMatch page when a new instance is created. 

    Args:
        browser (mechanicalsoup StatefulBrowser): Authenticated browser with full access to kenpom.com generated
            by the `login` function.
        date (str): Date to scrape, in format "YYYY-MM-DD", such as "2020-01-29".

    Attributes:
        url (str): Full url for the page to be scraped.
        date (str): Date to be scraped.
        lines_o_night (list): List containing lines of the night if games have taken place.
        ppg (float): Average points per game for the day.
        avg_eff (float): Average efficiency for the day.
        pos_40 (float): Possessions per 40 minutes for the day.
        mean_abs_err_pred_total_score (float): The mean absolute error of predicted total score for the day.
        bias_pred_total_score (float): The bias of predicted total score for the day.
        mean_abs_err_pred_mov (float): The mean absolute error of the predicted margin of victory for the day.
        record_favs (str): Record of favorites for the day.
        expected_record_favs (str): Expected record of favorites for the day.
        exact_mov (str): Number of games where margin of victory was accurately predicted out of total played.
        fm_df (pandas dataframe): Pandas dataframe containing parsed FanMatch table.
    """

    def __init__(self, browser, date = None):
        self.url = 'https://kenpom.com/fanmatch.php'
        self.date = date
        self.lines_o_night = None
        self.ppg = None
        self.avg_eff = None
        self.pos_40 = None
        self.mean_abs_err_pred_total_score = None
        self.bias_pred_total_score = None
        self.mean_abs_err_pred_mov = None
        self.record_favs = None
        self.expected_record_favs = None
        self.exact_mov = None
        
        if self.date is not None:
            self.url = self.url + "?d=" + self.date

        browser.open(self.url)
        fm = browser.get_current_page()
        table = fm.find_all("table")[0]
        fm_df = pd.read_html(str(table))
        fm_df = fm_df[0]
        fm_df = fm_df.rename(columns={"Thrill Score": "ThrillScore", "Come back": "Comeback", "Excite ment": "Excitement"})
        fm_df.ThrillScore = fm_df.ThrillScore.astype("str")
        fm_df["ThrillScoreRank"] = fm_df.ThrillScore.str[4:].str.strip()
        fm_df.ThrillScore = fm_df.ThrillScore.str[0:4]
        
        # Take care of parsing if some/all games have been completed.
        if not all(pd.isnull(fm_df["Excitement"])):
            fm_df["Excitement"] = fm_df.Excitement.str.split("·").str[0]
            fm_df["ExcitementRank"] = fm_df.Excitement.str.split("·").str[1]
            
            # Handle extra rows without game info.
            e_start = fm_df.index[fm_df["Game"].str.contains("the night")].tolist()[0]
            extra = fm_df.iloc[e_start:len(fm_df),]
            fm_df.drop(extra.index, inplace = True)
            self.lines_o_night = extra.iloc[1:len(extra)-4, 0].tolist()
            
            sts = extra.iloc[-1, 0]
            pred_score = extra.iloc[-2, 0]
            pred_mov = extra.iloc[-3, 0]

            sts_s = sts.split(": ")[2:]
            sts_s = [x.split("•")[0].strip() for x in sts_s]
            self.ppg = float(sts_s[0])
            self.avg_eff = float(sts_s[1])
            self.pos_40  = float(sts_s[2])

            pred_s = pred_score.split(": ")[1:]
            pred_s = [x.split("•")[0].strip() for x in pred_s]
            self.mean_abs_err_pred_total_score = float(pred_s[0])
            self.bias_pred_total_score = float(pred_s[1])

            pred_m = pred_mov.split(": ")[1:]
            mean_abs_err_pred_mov = pred_m[0]
            self.mean_abs_err_pred_mov = float(mean_abs_err_pred_mov.split("  •")[0])
            record_favs = pred_m[1]
            self.record_favs = record_favs.split(" (")[0]
            expected_record_favs = pred_m[2]
            self.expected_record_favs = expected_record_favs.split(")")[0]
            exact_mov = pred_m[2]
            exact_mov = exact_mov.split(" in ")[1]
            exact_mov = exact_mov.split()
            self.exact_mov = exact_mov[0] + "/" + exact_mov[2]
    
        # Will only be present if some games have been completed.
        if not all(pd.isnull(fm_df.Comeback)):
            fm_df["Comeback"] = fm_df.Comeback.str.split("·").str[0]
            fm_df["ComebackRank"] = fm_df.Comeback.str.split("·").str[1]

        mvp = fm_df.Game.str.split(" MVP: ").str[1]
        fm_df["Game"], fm_df["MVP"] = fm_df.Game.str.split(" MVP: ").str[0], mvp

        pos = fm_df.Game.str.split(r" \[").str[1]
        fm_df["Game"], fm_df["Possessions"] = fm_df.Game.str.split(r" \[").str[0], pos.astype("str")
        fm_df.Possessions = fm_df.Possessions.str.strip(r"\]")
        predict_info = fm_df.Prediction.str.split()
        pred_winner = fm_df.Prediction.astype("str").str.split().str[0:-2].tolist()
        pred_winner = [" ".join(i) if not any(pd.isnull(i)) else float("nan") for i in pred_winner]
        fm_df["PredictedWinner"] = pred_winner
        fm_df["PredictedScore"] = fm_df.Prediction.str.split().str[-2]
        fm_df["WinProbability"] = fm_df.Prediction.str.split().str[-1]
        fm_df.WinProbability = fm_df.WinProbability.str.strip("()")

        fm_df["PredictedMOV"] = [(int(x[0]) - int(x[1])) if len(x) > 1 else float("nan") for x 
                                 in fm_df.PredictedScore.astype("str").str.split("-")]

        fm_df.drop(["Prediction", "Time (ET)"], axis = 1, inplace = True)
        
        # Parse predicted loser.
        teams = fm_df.Game.str.split(", ").tolist()
        teams_np = fm_df.Game.str.split(" at ").tolist()
        
        i = 0
        pred_loser = []
        for x in teams:
            if not len(x) == 2:
                x = teams_np[i]
                
                # Account for neutral games.
                if len(x) < 2:
                    x = x[0].split(" vs. ")
                x[0] = " ".join(x[0].split()[1:])
                x[1] = " ".join(x[1].split()[1:])
                
            else:
                x[1] = x[1].split(" (")[0]

                x[0] = " ".join(x[0].split()[1:-1])
                x[1] = " ".join(x[1].split()[1:-1])
            
            if x[0] != pred_winner[i]:
                pred_loser.append(x[0])
            else:
                pred_loser.append(x[1])
                
            i = i + 1
            
        fm_df["PredictedLoser"] = pred_loser
        
        winner = fm_df.Game.str.split(", ").str[0].tolist()
        loser = fm_df.Game.str.split(", ").str[1].tolist()
        
        if not all(pd.isnull(loser)):
            loser = [str(x).split("(")[0] for x in loser]
            ot = fm_df.Game.str.split("(").str[1].astype("str").str.strip(")").tolist()
            fm_df["OT"] = ot
            
            fm_df["Loser"] = [" ".join(x.split()[1:-1]) if len(x.split(" at ")) < 2 else float("nan") for x in loser]
            fm_df["LoserRank"] = [x.split()[0] for x in loser]
            fm_df["LoserScore"] = [x.split()[-1] if len(x.split(" at ")) < 2 else float("nan") for x in loser]
            
        else:
            fm_df["OT"] = float("nan")
            fm_df["Loser"] = float("nan")
            fm_df["LoserRank"] = float("nan")
            fm_df["LoserScore"] = float("nan")
        
        fm_df["Winner"] = [" ".join(x.split()[1:-1]) if (len(x.split(" at ")) < 2 and 
            len(x.split(" vs. ")) < 2) else float("nan") for x in winner]
        fm_df["WinnerRank"] = [x.split()[0] if (len(x.split(" at ")) < 2 and 
            len(x.split(" vs. ")) < 2) else float("nan") for x in winner]
        fm_df["WinnerScore"] = [x.split()[-1] if (len(x.split(" at ")) < 2 and 
            len(x.split(" vs. ")) < 2) else float("nan") for x in winner]
        
        if not all(pd.isnull(loser)):
            fm_df["ActualMOV"] = [(int(x[0]) - int(x[1])) if not pd.isnull(x[0]) else float("nan") for x 
                                  in list(zip(fm_df.WinnerScore.tolist(), fm_df.LoserScore.tolist()))]
        else:
            fm_df["ActualMOV"] = float("nan")
        
        self.fm_df = fm_df
