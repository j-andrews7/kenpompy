# Changelog

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