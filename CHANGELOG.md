# Changelog

## v0.3.2

**Release date: 08/03/2022**

 - Fix a parsing error in `team.get_schedule()` when ampersand in team name - [#14](https://github.com/j-andrews7/kenpompy/issues/14).
 - Fix a bunch of pandas deprecation warnings - [#18](https://github.com/j-andrews7/kenpompy/issues/18).
 - Fix a test failing due to a change in how experience is quantified- [#21](https://github.com/j-andrews7/kenpompy/issues/21).

Big thanks to [@esqew](https://github.com/esqew) for the fixes.

## v0.3.1

**Release date: 01/23/2022**

 - Fix a bug in `get_teamstats` when no season was provided and defense was requested - [#12](https://github.com/j-andrews7/kenpompy/issues/12).

## v0.3.0

**Release date: 11/14/2021**

 - Begin a `team` module that allow for schedule scraping for each team (thanks to [@andrewsseamanco](https://github.com/andrewseamanco))
 - Fix a few bugs in `summary` and `misc` scraping modules, see [#9](https://github.com/j-andrews7/kenpompy/issues/9) & see [#7](https://github.com/j-andrews7/kenpompy/issues/7).
 - Fix issue with `get_program_ratings` due to additional column being added.

## v0.2.0

**Release date: 02/16/2020**

 - Added the `FanMatch` class for scraping the FanMatch page.
   - Also calculate predicted Margin of Victory and slightly alters format of output table for more convenient use.
 - Fix several edge-case bugs in `summary` and `misc` scraping modules, mostly having to do with teams with no rank.


## v0.1.0 - Initial Release

**Release date: 12/26/2019**

 - Provide functions for scraping nearly all `Summary` and `Miscellaneous` pages.