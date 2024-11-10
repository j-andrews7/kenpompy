# Changelog

## v0.4.0

**Release date: 11/09/2024**

* Unit tests and warning fixes for scouting report by @WakeUpWaffles in https://github.com/j-andrews7/kenpompy/pull/76
* Strip asterisks from team name in get_valid_teams for 2020 season (fixes #81) by @esqew in https://github.com/j-andrews7/kenpompy/pull/82
* Add postseason indicator for team schedule (closes #80) by @esqew in https://github.com/j-andrews7/kenpompy/pull/83
* Remove dead imports (fixes #60) by @esqew in https://github.com/j-andrews7/kenpompy/pull/84
* Add pause time between test cases by @esqew in https://github.com/j-andrews7/kenpompy/pull/86
* Add support for scraping dynamic Scouting Report in team.py by @esqew in https://github.com/j-andrews7/kenpompy/pull/71
* Remove unused variable in misc.py by @esqew in https://github.com/j-andrews7/kenpompy/pull/88
* add NST% columns by @nickostendorf in https://github.com/j-andrews7/kenpompy/pull/89
* Refactor for new cloudflare requirements by @seankim658 in https://github.com/j-andrews7/kenpompy/pull/95
* Handle dates with no games in fanmatch data by @seankim658 in https://github.com/j-andrews7/kenpompy/pull/96
* Update docs  by @seankim658 in https://github.com/j-andrews7/kenpompy/pull/97
* Adds `lxml` and fix for new no games fanmatch message by @seankim658 in https://github.com/j-andrews7/kenpompy/pull/99
* Update for predicted possessions and new date matching  by @seankim658 in https://github.com/j-andrews7/kenpompy/pull/101
* V0.4.0 release by @j-andrews7 in https://github.com/j-andrews7/kenpompy/pull/98
* Fix ReadTheDocs documentation build (again) due to missing dependencies.

## v0.3.5

**Release date: 11/22/2023**

* Fix for ambiguous column names in DataFrame returned by get_pomeroy_ratings by @esqew in https://github.com/j-andrews7/kenpompy/pull/34
* Update parsing for team name and seed (fixes for j-andrews7/kenpompy#41) by @nickostendorf in https://github.com/j-andrews7/kenpompy/pull/42
* Added check for expired subscription (closes #37) by @esqew in https://github.com/j-andrews7/kenpompy/pull/45
* Fixed parsing for tournament labels on FanMatch pages (fixes #47) by @esqew in https://github.com/j-andrews7/kenpompy/pull/48
* Enhancement: Conference stats by @WakeUpWaffles in https://github.com/j-andrews7/kenpompy/pull/50
* Fixed shape test for test_get_program_ratings after patch to remove extraneous rows by @esqew in https://github.com/j-andrews7/kenpompy/pull/51
* Fix for typo'd reference in test_team.py by @esqew in https://github.com/j-andrews7/kenpompy/pull/52
* Update to test_get_program_ratings to use dynamic verification of df shape by @esqew in https://github.com/j-andrews7/kenpompy/pull/54
* HTML string literal FutureWarning fixes (closes #55) by @esqew in https://github.com/j-andrews7/kenpompy/pull/56
* CI/CD updates by @esqew in https://github.com/j-andrews7/kenpompy/pull/58
* Remove cancel-in-progress from CI/CD concurrency config by @esqew in https://github.com/j-andrews7/kenpompy/pull/69
* Add name parsing tests for previously problematic team names by @esqew in https://github.com/j-andrews7/kenpompy/pull/73
* Fix for calculation of current season/year (fixes #64) by @esqew in https://github.com/j-andrews7/kenpompy/pull/67
* Fixed team schedules before 2010 by @WakeUpWaffles in https://github.com/j-andrews7/kenpompy/pull/75
* Add new ReadTheDocs config so that docs properly build.

## v0.3.4

**Release date: 12/25/2022**

 - * Fix for Cloudflare SSL profiling by @esqew in https://github.com/j-andrews7/kenpompy/pull/38

## v0.3.3

**Release date: 11/07/2022**

 - Add explicit user-agent to MechanicalSoup instance to bypass Cloudflare (fixes j-andrews7/kenpompy#24) by [@esqew](https://github.com/esqew) in https://github.com/j-andrews7/kenpompy/pull/25
 - Add keyword arguments for str.split (resolves j-andrews7/kenpompy#27) by [@esqew](https://github.com/esqew) in https://github.com/j-andrews7/kenpompy/pull/28
 - Enhancement: Add login failure detection by [@esqew](https://github.com/esqew) in https://github.com/j-andrews7/kenpompy/pull/23
 - Update expected shape of program ratings DataFrame (resolves j-andrews7/kenpompy#29) by [@esqew](https://github.com/esqew) in https://github.com/j-andrews7/kenpompy/pull/30
 - Fix for FanMatch parsing and test warnings (fixes j-andrews7/kenpompy#26) by [@esqew](https://github.com/esqew) in https://github.com/j-andrews7/kenpompy/pull/31
 - Enhancement: Add GitHub Actions CI/CD for pytest by [@esqew](https://github.com/esqew) in https://github.com/j-andrews7/kenpompy/pull/32
 - Set minimum python version to 3.8 to avoid dependency deprecation changes.


**Full Changelog**: https://github.com/j-andrews7/kenpompy/compare/v0.3.2...v0.3.3

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