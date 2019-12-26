# kenpompy - Basketball for Nerds
[![Documentation Status](https://readthedocs.org/projects/kenpompy/badge/?version=latest)](https://kenpompy.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.com/j-andrews7/kenpompy.svg?branch=master)](https://travis-ci.com/j-andrews7/kenpompy) [![codecov](https://codecov.io/gh/j-andrews7/kenpompy/branch/master/graph/badge.svg)](https://codecov.io/gh/j-andrews7/kenpompy)


This python package serves as a convenient web scraper for [kenpom.com](kenpom.com), which provides tons of great NCAA basketball statistics and metrics. It **requires a subscription to Ken Pomeroy's site for use**, otherwise only the home page will be accessible. It's a small fee for a year of access, and totally worth it in my opinion.

## Objective
Ultimately, this package is to allow both hobbyist and reknown sports analysts alike to get data from kenpom in a format more suitable for visualization, transformation, and additional analysis. It's meant to be simple, easy to use, and to yield information in a way that is immediately usable.

## Responsible Use
As with many web scrapers, the responsibility to use this package in a reasonable manner falls upon the user. Don't be a jerk and constantly scrape the site a thousand times a minute or you run the risk of potentially getting barred from it, which you'd likely deserve. I am in no way responsible for how you use (or abuse) this package. Be sensible.

## But I Use R
Yeah, yeah, but have you heard of [reticulate](https://rstudio.github.io/reticulate/)? It's an R interface to python that also supports passing objects (like dataframes!) between them. 

---

## Installation
This package will be put on pypi once in a stable state, but it can currently be easily installed with:

```
git clone https://github.com/j-andrews7/kenpompy.git
pip install .
```

## What It Can (and Can't) Do
This a work in progress - it can currently scrape all of the summary and miscellaneous tables, pretty much all of those under the Stats and Miscellany headings. `Team` and `Player` classes are planned, but they're more complicated and will take some time.

## Usage
`kenpompy` is simple to use. Generally, tables on each page are scraped into `pandas` dataframes with simple parameters to select different seasons or tables. As many tables have headers that don't parse well, some are manually altered to a small degree to make the resulting dataframe easier to interpret and manipulate. 

First, you must login:
```
from kenpompy.utils import login

# Returns an authenticated browser that can then be used to scrape pages that require authorization.
browser = login(your_email, your_password)
```

Then you can request specific pages that will be parsed into convenient dataframes:
```
import kenpompy.summary as kp

# Returns a pandas dataframe containing the efficiency and tempo stats for the current season (https://kenpom.com/summary.php).
eff_stats = kp.get_efficiency(browser)
```

---

## Contributing
You can contribute by creating [issues](https://github.com/j-andrews7/kenpompy/issues) to highlight bugs and make suggestions for additional features. [Pull requests](https://github.com/j-andrews7/kenpompy/pulls) are also very welcome.

## License
`kenpompy` is released on the GNU GPL v3.0 license. You are free to use, modify, or redistribute it in almost any way, provided you state changes to the code, disclose the source, and use the same license. It is released with zero warranty for any purpose and I retain no liability for its use. [Read the full license](https://github.com/j-andrews7/kenpompy/blob/master/LICENSE) for additional details.