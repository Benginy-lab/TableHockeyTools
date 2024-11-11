
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time



#simple logging function
def THlog(message, mode="info"):
    class TextColors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if mode == "info":
        print(f"{TextColors.OKBLUE}INFO: {message}{TextColors.ENDC}")
    elif mode == "warning":
        print(f"{TextColors.WARNING}WARN: {message} \n add supress_warnings=True if you want to ignore{TextColors.ENDC} ")
    elif mode == "error":
        print(f"{TextColors.FAIL}ERROR:{message}{TextColors.ENDC}")

## gets the ranking points for a player
def GetPlayerPoints(player_ids=[], player_names=[], return_mode="list", date=None, verbose=False, supress_warnings=False):
    if return_mode not in ["list", "dict", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        points_values = []
    elif return_mode == "dict":
        points_values = {}
    else:
        points_values = None

    player_ids = list(player_ids)
    player_names = list(player_names)

    if not ((len(player_ids) == 0) or (len(player_names) == 0)):
        THlog("Please provide either a player ID or a player name, not both.", "error")
        return
    elif len(player_ids) == 0 and len(player_names) == 0:
        THlog("Please provide either a player ID or a player name.", "error")

    if player_ids == []:
        player_ids = GetPlayerID(player_names, return_mode="list") #gets player ids from player names

        if verbose:
            THlog(f"Found player ids {player_ids}", "info")
    if player_names == []:
        player_names = GetPlayerName(player_ids, return_mode="list") #gets player names from player ids
        if verbose:
            THlog(f"Found player names {player_names}", "info")

    for id, name in zip(player_ids, player_names):
        points_url = 'https://stiga.trefik.cz/ithf/ranking/player.aspx?id=' + id

        response_points = requests.get(points_url)
        response_points.raise_for_status()

        soup = BeautifulSoup(response_points.content, 'html.parser')

        points_label = soup.find(string="Points")

        if points_label:
            points_value = points_label.find_next("td").string.strip() #gets the value of the points from the html
            try:
                int(points_value)
            except ValueError:
                if not supress_warnings:
                    THlog(f"{name} Has no points, skipping... ID = {id}", "warning")
                continue

            if return_mode == "list":
                points_values.append(points_value)
            elif return_mode == "dict":
                points_values[name] = points_value
            else:
                return points_value
        elif not supress_warnings:
            THlog(f"Could not find points for player {name}.", "warning")
        if len(points_values) == 0 and len(player_names) > 1:
            THlog(f"could not find any points values for {player_names}", "error")
    return points_values


## gets the open ranking for a player, output is a list or key-value pair depending on return_mode
def GetPlayerRank(player_ids=None, player_names=None, return_mode="list", verbose=False, supress_warnings=False):
    if return_mode not in ["list", "dict", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        ranks = []
    elif return_mode == "dict":
        ranks = {}

    player_ids = [player_ids] if type(player_ids) is not list else player_ids
    player_names = [player_names] if type(player_names) is not list else player_names

    if not ((player_ids[0] is None )^(player_names[0] is None)):
        THlog("Please provide either a player ID or a player name.", "error")
        return

    if player_ids[0] is None:
        player_ids = GetPlayerID(player_names, return_mode="list") #gets player ids from player names

        if verbose:
            THlog(f"Found player ids {player_ids}", "info")

    for id, name in zip(player_ids, player_names):
        player_pos_url = "https://www.ithf.info/stiga/ithf/ranking/getrank.asmx/GetRank?ID="+str(id)
        if verbose:
            THlog(f"Requesting url {player_pos_url}", "info")

        response = requests.get(player_pos_url) #request url
        response.raise_for_status()
        rank = ET.fromstring(response.content).text
        if rank == "-": #if no rank is found the response from the server is "-"
            if not supress_warnings:
                THlog(f"no rank for {name}", "warning")
            continue
        else:
            if return_mode == "list":
                ranks.append(rank)
            elif return_mode == "dict":
                ranks[name] = rank
            else:
                return rank
    return ranks


## gets the player id from the player's name, last name first then first name.
def GetPlayerID(player_names, return_mode="single", verbose=False, supress_warnings=False):
    if return_mode not in ["dict", "list", "single"]:
        THlog("return_mode must be either 'dict', 'list' or 'single'", "error")
        return
    if return_mode == "list":
        player_ids = []
    elif return_mode == "dict":
        player_ids = {}
    else:
        player_ids = 0

    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'

    response = requests.get(url)
    response.raise_for_status()

    lines = response.text.splitlines()
    if player_names is None:
        THlog("Please provide either a player name or a list of player names.", "error")
        return
    if player_names.__class__.__name__ == "str":
        player_names = [player_names]
    for player_name in player_names:
        for line in lines:
            columns = line.split('\t')
            if len(columns) > 1:
                player_id, full_name = columns[0], columns[1]
                if full_name.lower().__contains__(player_name.lower()):
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}", "info")

                    if return_mode == "list":
                        player_ids.append(player_id)
                    elif return_mode == "dict":
                        player_ids[full_name] = player_id
                    else:
                        return int(player_id)

        if len(player_ids) == 0 and len(player_names) > 1 and not supress_warnings:
            THlog(f"could not find a {player_name}, check for spelling mistakes.", "warning")
    if len(player_ids) == 0:
        THlog("No player IDs found.", "error")
        return
    return player_ids


##opposite of GetPlayerID, gets the player name from the player's id
def GetPlayerName(player_ids, return_mode="single", verbose=False, supress_warnings=False):
    if return_mode not in ["dict", "list", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        player_names = []
    elif return_mode == "dict":
        player_names = {}
    else:
        player_names = 0

    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'

    response = requests.get(url)
    response.raise_for_status()

    lines = response.text.splitlines()
    if player_ids is None:
        THlog("Please provide either a player name or a list of player names.", "error")
        return
    if player_ids.__class__.__name__ == "str":
        player_ids = [player_ids]

    for id in player_ids:
        for line in lines:
            columns = line.split('\t')
            if len(columns) > 1:
                player_id, full_name = columns[0], columns[1]
                if player_id == id:
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}")

                    if return_mode == "list":
                        player_names.append(full_name)
                    elif return_mode == "dict":
                        player_names[full_name] = player_id
                    else:
                        return full_name

        if len(player_names) == 0 and len(player_ids) > 1 and not supress_warnings:
            THlog(f"could not find id {id}, check for spelling mistakes.", "warning")
    if len(player_names) == 0:
        THlog("No player names found.", "error")
        return
    return player_names


# Ranks the players based on their points and returns a list of ranks in a list format. input must be a dictionary of player names and points
def LocalRanker(PlayerPoints, verbose=False, supress_warnings=False):
    try:
        dict(PlayerPoints)
    except TypeError:
        THlog("PlayerPoints must be a dictionary of player names and points.", "error")
        return
    except:
        THlog("something unexpected happened when trying to sort the player points, EXITING...", "error")
        return
    result = []
    pointslst = []
    sortedPlayerPoints = dict(sorted(PlayerPoints.items(), key=lambda x: int(x[1]), reverse=True))
    if verbose:
        print(f"playerpoints : {PlayerPoints}\nIs sorted to:  {sortedPlayerPoints}")

    for Playerpoints, pos in zip(sortedPlayerPoints.items(), range(len(PlayerPoints))):
        name = Playerpoints[0]
        points = Playerpoints[1]
        pointslst.append(int(points))
        result.append([int(pos)+1, name, points])

    if sorted(pointslst)[::-1] != pointslst:
        THlog("Sorting points failed, Aborting...", "error")
        return
    return result

# filters the players id based on different criteria
def IDFilter(country="any", Team="any", ranking_start=1, ranking_end=None, return_mode="list", filter_mode="and", verbose=False, supress_warnings=True):
    if return_mode not in ["dict", "list"]:
        THlog("return_mode must be either 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        player_ids = []
    else:
        player_ids = {}

    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'

    response = requests.get(url)
    response.raise_for_status()

    lines = response.text.splitlines()
    for line in lines:
        columns = line.split('\t')
        if len(columns) > 1:
            player_id, full_name, Playerteam, Playercountry, Playerranking = columns[0], columns[1], columns[2], columns[3], columns[4][:-1]
## additive filter ---------------------------------------------------------------------
            if filter_mode == "and":
                if country.lower() == Playercountry.lower() or country.lower() == "any":

                    if Team.lower() == Playerteam.lower() or Team.lower() == "any":
                        if ranking_end is None :
                            if verbose:
                                THlog(f"Found player {full_name} with ID {player_id}")

                            if return_mode == "list":
                                player_ids.append(player_id)
                            elif return_mode == "dict":
                                player_ids[full_name] = player_id
                            continue


                        try: int(ranking_start) <= int(Playerranking) <= int(ranking_end)
                        except ValueError:
                            if not supress_warnings:
                                THlog(f"Could not find ranking for {id}, skipping...", "warning")
                            continue
                        except TypeError:
                            THlog("ranking_start and ranking_end must be integers", "error")
                            return

                        if int(ranking_start) <= int(Playerranking) <= int(ranking_end):
                            if verbose:
                                THlog(f"Found player {full_name} with ID {player_id}")

                            if return_mode == "list":
                                player_ids.append(player_id)
                            elif return_mode == "dict":
                                player_ids[full_name] = player_id
## or filter ---------------------------------------------------------------------
            elif filter_mode == "or":
                if country.lower() == Playercountry.lower():
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}")

                    if return_mode == "list":
                        player_ids.append(player_id)
                    elif return_mode == "dict":
                        player_ids[full_name] = player_id
                if Team.lower() == Playerteam.lower():
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}")

                    if return_mode == "list":
                        player_ids.append(player_id)
                    elif return_mode == "dict":
                        player_ids[full_name] = player_id
                if ranking_end is not None:
                    try:
                        int(Playerranking)
                    except ValueError:
                        if not supress_warnings:
                            THlog(f"Could not find ranking for {full_name}, skipping...", "warning")
                            continue

                    if int(ranking_start) <= int(Playerranking) <= int(ranking_end):
                        if verbose:
                            THlog(f"Found player {full_name} with ID {player_id}")

                        if return_mode == "list":
                            player_ids.append(player_id)
                        elif return_mode == "dict":
                            player_ids[full_name] = player_id
            else:
                THlog("filter_mode must be either 'and' or 'or'", "error")
                return
    return player_ids

def GetHistory(playerid, date_start, date_end=None, getattr="points", return_mode="single", verbose=False, supress_warnings=False):
    points = []
    ranks = []
    dates = []

    try:
        int(playerid)
    except TypeError:
        THlog("Invalid playerid, please enter a number", "error")
        return

    if return_mode not in ["single", "list", "dict"]:
        THlog("return mode must be either 'dict','single' or 'list'", "error")
        return

    try:
        if date_end is None:
            dates.append(time.strptime(date_start, "%Y-%m"))
        else:
            start_date = time.strptime(date_start, "%Y-%m")
            end_date = time.strptime(date_end, "%Y-%m")
            current_date = start_date
            while current_date <= end_date:
                dates.append(current_date)
                # Get next month
                year = current_date.tm_year + (current_date.tm_mon) // 12
                month = (current_date.tm_mon % 12) + 1
                current_date = time.strptime(f"{year}-{month:02d}", "%Y-%m")
    except TypeError:
        THlog("Error in formatting dates, remember to input as a string 'YYYY-MM'", "error")
        return





    url = f"https://stiga.trefik.cz/ithf/ranking/rankpl.aspx?pl={playerid}"
    if verbose:
        THlog(f"Requesting {url}", "info")

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    for date in dates:
        year_label = soup.find("td", class_="PlayerB", string=str(date.tm_year))
        if not year_label:
            THlog(f"Year {date.tm_year} not found in the data", "error")
            return

        year_row = year_label.find_parent("tr")
        month_table = year_row.find_next("table")
        month_index = date.tm_mon - 1  # Month is 1-based in struct_time, so adjust by -1

        month_cells = month_table.find_all("td", class_=["Player", "Player1"])
        if month_index >= len(month_cells):
            THlog("Invalid month index or unexpected table format", "error")
            return

        month_cell = month_cells[month_index]

        ranking_value = month_cell.text.split('.')[0].strip()  # Get the numeric part
        points_value = month_cell.find("a").text.strip()  # Find the link in this cell


        if getattr == "rank" or "both":
            if ranking_value.isdigit():
                if return_mode == "single":
                    return ranking_value
                ranks.append(ranking_value)
            else:
                if not supress_warnings:
                    THlog(f"No valid ranking data found for {time.strftime('%B %Y', date)}", "warning")
                continue
        if getattr == "points" or "both":
            if points_value.isdigit():
                if points_value.isdigit():
                    if return_mode == "single":
                        return points_value
                    points.append(points_value)
                else:
                    if not supress_warnings:
                        THlog(f"No valid points data found for {time.strftime('%B %Y', date)}", "warning")
                    continue
    if return_mode == "list":
        if getattr == "points":
            return points
        elif getattr == "rank":
            return ranks
        else:
            returnlst = []
            for rank,points in zip(ranks, points):
                returnlst.append([points, rank])
            return returnlst

    dict={}
    for date in dates:
        date = time.strftime("%Y-%m", date)
        for rank,points in zip(ranks, points):
            if getattr == "points":
                dict[date]=points
            elif getattr == "rank":
                dict[date]=rank
            else:
                dict[date]=[points, rank]
    return dict
