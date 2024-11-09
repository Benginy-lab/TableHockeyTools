
# TableHockeyTools Manpage(1)

## NAME
**THTools** - Python package for retrieving and displaying table hockey player data.

## SYNOPSIS
```python
from THTools import THlog, GetPlayerPoints, GetPlayerRank, GetPlayerID, GetPlayerName
```

## DESCRIPTION
**THTools** provides functions to work with table hockey player data. This includes functions for retrieving player ranking points, ranks, IDs, and names. Logging is provided with customizable verbosity and warning suppression.

## FUNCTIONS

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
  - `return_mode` (str): Output format, one of "list", "dict", or "single". _(default: "list")_
  - `verbose` (bool): If `True`, logs additional information. _(default: False)_
  - `supress_warnings` (bool): If `True`, suppresses warning logs. _(default: False)_

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