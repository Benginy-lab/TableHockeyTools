
# TableHockeyTools Manpage(1)

## NAME
**THTools** - Python package for retrieving and displaying table hockey player data.

## SYNOPSIS
```python
from THTools import THlog, GetPlayerPoints, GetPlayerRank, GetPlayerID, GetPlayerName, IDfilter, LocalRanker,
```

## DESCRIPTION
**THTools** provides functions to work with table hockey player data. This includes functions for retrieving player ranking points, ranks, IDs, and names. Logging is provided with customizable verbosity and warning suppression.

## FUNCTIONS

### DEFAULT PARAMETERS
- `return_mode` (str): Output format, one of "list", "dict", or "single". _(default: "list")_
- `verbose` (bool): If `True`, logs additional information. _(default: False)_
- `supress_warnings` (bool): If `True`, suppresses warning logs. _(default: False)_


### THlog(message, mode="info")
Logs messages with different color-coded modes.

- **Parameters:**
  - `message` (str): Message to log.
  - `mode` (str): Logging mode, one of "info", "warning", or "error".

### GetPlayerPoints(player_ids=None, player_names=None, return_mode="list", verbose=False, supress_warnings=False)
Fetches ranking points for specified players.

- **Parameters:**
  - `player_ids` (str or list): Player ID(s).
  - `player_names` (str or list): Player name(s).

- **Returns:** List, dict, or single value of points.

### GetPlayerRank(player_ids=None, player_names=None, return_mode="list", verbose=False, supress_warnings=False)
Fetches open ranking postition for specified players.

- **Parameters:** Same as **GetPlayerPoints**.

- **Returns:** List, dict, or single value of rank.

### GetPlayerID(player_names, return_mode="single", verbose=False, supress_warnings=False)
Fetches player ID(s) for given player name(s).
Last name is required first, followed by first name. Given names are case-insensitive.

- **Parameters:**
  - `player_names` (str or list): Player name(s).
  - `return_mode` (str): Output format, one of "list", "dict", or "single".

- **Returns:** List, dict, or single value of player ID(s).

### GetPlayerName(player_ids, return_mode="single", verbose=False, supress_warnings=False)
Fetches player name(s) for given player ID(s).

- **Parameters:** Same as **GetPlayerID**.

- **Returns:** List, dict, or single value of player names.

### LocalRanker(PlayerPoints, verbose=False, supress_warnings=False)
ranks the given players with given points.
- **Input:** Dictionary _{"PlayerName":points}_

- **Parameters:**
  - `Playerpoints` (directory): a Dictionary of Playernames and points
  - _Default parameters except return_mode_

- **Returns:** list of lists formatted as [[postition,Name,Points], ]

### IDFilter(country="any", Team="any", ranking_start=1, ranking_end=None, return_mode="list", filter_mode="and", verbose=False, supress_warnings=True)
Returns every id containing these parameters.
- **Parameters:**
  - `country` (str):filters everybody from other countries
  - `team` (str):filters everybody from other teams.
  - `ranking_start` and `ranking_end` (int):returns only players who are between theese two postitions
  - `filter_mode` (str):contains two modes: `"and"` and `"or"`.  `"and"` mode returns only players who are within both/all of the conditions, while `"or"` mode returns if player fits at least one of the categories.
  - _Default parameters_
- **Returns:**
  the ids in either list format or a dict formatted as `"full_name":player id`

### GetHistory(playerid, date, date_end=None, getattr="points", return_mode="single", verbose=False, supress_warnings=False)
Returns points and/or rank of a player at a set date, the date format is "YYYY-MM". To get results from a range of dates, set the date variable to the start date and the date_end to the end date.
- **Parameters:**
  - `playerid` (int or str):the ITHF player id of the player being checked
  - `date` (str): the date to check, or the start date if `date_end` is set. Formatted `"YYYY-MM"` example `"2024-11"`
  - `date_end` (str): set to `None` unless you want to set a range, in that case, this is the last month counted. for example if `"2020-03"` then march 2020 would be the last mont checked.
  - `getattr` (str): could be set to `points`, `rank` or `both`
  - _Default parameters_

- **Returns**
  - if `return_mode` is set to `"single"`, it will return a single string with the value of either the rank or amount of points.
  - if `return_mode` is `"list"`, it will return a list of points, ranks or a list of a list of both. example [[points, rank], ]
  - if `return_mode` is `"dict"`, it will return a dict formatted `"YYYY-MM":points or rank` if `getattr` is set to `"both"`, this function will return a dict formatted `"YYYY-MM":[points, rank]`

## EXAMPLES

1. **Log an informational message:**
   ```python
   THlog("Retrieving player points", "info")
   ```

2. **Get ranking points for a single player by ID:**
   ```python
   points = GetPlayerPoints(player_ids="12345", return_mode="single")
   ```

3. **Get the player ID for a name:**
   ```python
   player_id = GetPlayerID("Doe John", return_mode="single")
   ```

## DEPENDENCIES
- `requests`
- `bs4` (BeautifulSoup)
- `xml.etree.ElementTree`
