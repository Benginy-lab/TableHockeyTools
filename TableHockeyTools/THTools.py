
import re
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from functools import lru_cache

# Utility function to ensure input is a list
def ensure_list(x):
    return x if isinstance(x, list) else [x]

#simple logging function
def THlog(message, mode="info"):
    class TextColors:
        OKBLUE = '\033[94m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

    if mode == "info":
        print(f"{TextColors.OKBLUE}INFO: {message}{TextColors.ENDC}")
    elif mode == "warning":
        print(f"{TextColors.WARNING}WARN: {message} \n add supress_warnings=True if you want to ignore{TextColors.ENDC} ")
    elif mode == "error":
        print(f"{TextColors.FAIL}ERROR:{message}{TextColors.ENDC}")


# cashing the player id data to avoid excessive requests
@lru_cache(maxsize=10)
def GetPlayerList(verbose = False):
    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'
    THlog(f"fetching {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()



## gets the ranking points for a player
def GetPlayerPoints(player_ids=None, player_names=None, return_mode="list", verbose=False, supress_warnings=False):
    if return_mode not in ["list", "dict", "single"]:
        THlog("return_mode must be either 'single', 'list' or 'dict'", "error")
        return
    if return_mode == "list":
        points_values = []
    elif return_mode == "dict":
        points_values = {}
    else:
        points_values = None

    if player_ids==None and player_names==None:
        THlog("Please provide either a player ID or a player name.", "error")
        return
    
    
    
    
    player_names = ensure_list(player_names)
    player_ids = ensure_list(player_ids)

    #get names from ids and ids from names
    tmpplayer_ids = IDPlayer(player_names, return_mode="list", direction="N2ID", supress_warnings=True)
    tmpplayer_names = IDPlayer(player_ids, return_mode="list", direction="ID2N", supress_warnings=True) #gets player names from player ids

    player_names += tmpplayer_names
    player_ids += tmpplayer_ids

    #clean up Nonetypes
    if player_names[0] == None:
        player_names.pop(0)
    
    if player_ids[0] == None:
        player_ids.pop(0)
    
    
    if verbose:
        THlog(f"Found player names {player_names}", "info")
        THlog(f"Found player ids {player_ids}", "info")

    for id, name in zip(player_ids, player_names):
        points_url = f'https://stiga.trefik.cz/ithf/ranking/player.aspx?id={id}'
        if verbose:
            THlog(f"fetching url {points_url} for {name}")

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
    player_ids = ensure_list(player_ids)
    player_names = ensure_list(player_names)

    if len(player_ids) == 0 and len(player_names) == 0:
        THlog("Please provide either a player ID or a player name.", "error")
    
    tmpplayer_ids = IDPlayer(player_names, return_mode="list", direction="N2ID", supress_warnings=True) #gets player ids from player names

    if verbose:
        THlog(f"Found player ids {tmpplayer_ids}", "info")
    
    player_names += IDPlayer(player_ids, return_mode="list", direction="ID2N", supress_warnings=True) #gets player names from player ids


    player_ids = tmpplayer_ids+player_ids
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

# New IDPlayer function that handles both name-to-ID and ID-to-name lookups
def IDPlayer(query_values, return_mode="single", direction="N2ID", verbose=False, supress_warnings=False):
    if return_mode not in ["dict", "list", "single"]:
        THlog("return_mode must be either 'dict', 'list' or 'single'", "error")
        return

    if direction not in ["N2ID", "ID2N"]:
        THlog("direction must be either 'N2ID'(name to ID) or 'ID2N'(ID to name)", "error")
        return
    # check for empty input
    query_values = ensure_list(query_values)
    if query_values[0] is None:
        if not supress_warnings:
            THlog("No query values provided", "warning")
        if return_mode == "single":
            return
        else:
            return []

    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    result = [] if return_mode == "list" else {} if return_mode == "dict" else None

    for query in query_values:
        found = False
        for line in lines:
            columns = line.split('\t')
            if len(columns) > 1:
                player_id, full_name = columns[0], columns[1]
                if direction == "N2ID" and full_name.lower().__contains__(query.lower()):
                    found = True
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}", "info")
                    if return_mode == "list":
                        result.append(player_id)
                    elif return_mode == "dict":
                        result[full_name] = player_id
                    else:
                        return int(player_id)
                elif direction == "ID2N" and int(player_id) == int(query):
                    found = True
                    if verbose:
                        THlog(f"Found player {full_name} with ID {player_id}", "info")
                    if return_mode == "list":
                        result.append(full_name)
                    elif return_mode == "dict":
                        result[full_name] = player_id
                    else:
                        return full_name
        if not found and not supress_warnings:
            THlog(f"Could not find a match for {query}, check for spelling mistakes.", "warning")

    if (isinstance(result, list) or isinstance(result, dict)) and not result:
        THlog("No matches found.", "error")
        return

    return result

# wrappers for compatibility
def GetPlayerID(player_names, return_mode="single", verbose=False, supress_warnings=False):
    THlog("GetPlayerID is deprecated, it is recommended you use IDPlayer", )
    return IDPlayer(player_names, return_mode=return_mode, direction="N2ID", verbose=verbose, supress_warnings=supress_warnings)

def GetPlayerName(player_ids, return_mode="single", verbose=False, supress_warnings=False):
    THlog("GetPlayerName is deprecated, it is recommended you use IDPlayer")
    return IDPlayer(player_ids, return_mode=return_mode, direction="ID2N", verbose=verbose, supress_warnings=supress_warnings)

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
        THlog(f"playerpoints : {PlayerPoints}\nIs sorted to:  {sortedPlayerPoints}", "info")

    for Playerpoints, pos in zip(sortedPlayerPoints.items(), range(len(PlayerPoints))):
        name = Playerpoints[0]
        points = Playerpoints[1]
        pointslst.append(int(points))
        result.append([int(pos)+1, name, points])

    if sorted(pointslst)[::-1] != pointslst:
        THlog("Sorting points failed, Aborting...", "error")
        return
    return result

# filters the player ids based on different criteria
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


                        try:
                            if int(ranking_start) <= int(Playerranking) <= int(ranking_end):
                                if verbose:
                                    THlog(f"Found player {full_name} with ID {player_id}")

                                if return_mode == "list":
                                    player_ids.append(player_id)
                                elif return_mode == "dict":
                                    player_ids[full_name] = player_id
                        except ValueError:
                            if not supress_warnings:
                                THlog(f"Could not find ranking for {id}, skipping...", "warning")
                            continue
                        except TypeError:
                            THlog("ranking_start and ranking_end must be integers", "error")
                            return


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

def GetHistory(playerid, date, date_end=None, getattr="points", return_mode="single", verbose=False, supress_warnings=False):
    points = []
    ranks = []
    dates = []
    invalid = []

    try:
        int(playerid)
    except TypeError:
        THlog("Invalid playerid, please enter a number", "error")
        return

    if return_mode not in ["single", "list", "dict"]:
        THlog("return mode must be either 'dict','single' or 'list'", "error")
        return

    if getattr not in ["points","rank","both"]:
        THlog("return mode must be either 'points','rank' or 'both'", "error")
        return

    elif return_mode == "single" and getattr =="both":
        THlog("Can not return single when getattr is both", "error")
        return

    if not isinstance(date, time.struct_time):
        try:
            date = time.strptime(date, "%Y-%m")
        except TypeError:
            THlog("Error in formatting dates, remember to input as a string 'YYYY-MM'", "error")
            return
    if date_end != None and not isinstance(date_end, time.struct_time):
            try:
                date_end = time.strptime(date_end, "%Y-%m")
            except TypeError:
                THlog("Error in formatting dates, remember to input as a string 'YYYY-MM'", "error")
                return


    if date_end is None:
        dates.append(date)
    else:
        current_date = date
        if not current_date <= date_end:
            THlog("date_end must be higher than date", "error")
            return
        while current_date <= date_end:
            dates.append(current_date)
            # Get next month
            year = current_date.tm_year + (current_date.tm_mon) // 12
            month = (current_date.tm_mon % 12) + 1
            current_date = time.strptime(f"{year}-{month:02d}", "%Y-%m")
    if verbose:
        verboseprint=[]
        for date in dates:
            verboseprint.append(time.strftime("%Y-%m", date))

        THlog(f"dates to check: {verboseprint}")

    url = f"https://stiga.trefik.cz/ithf/ranking/rankpl.aspx?pl={playerid}"
    if verbose:
        THlog(f"Requesting {url}", "info")

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    for i in range(len(dates)):
        tmpdate = dates[i]
        
        year_label = soup.find("td", class_="PlayerB", string=str(tmpdate.tm_year))
        if not year_label:
            THlog(f"Year {tmpdate.tm_year} not found in the data", "log")
            invalid.append(i)
            continue
                

        year_row = year_label.find_parent("tr")
        month_table = year_row.find_next("table")
        month_index = tmpdate.tm_mon - 1  # Month is 1-based in struct_time, so adjust by -1

        month_cells = month_table.find_all("td", class_=["Player", "Player1", "Player2", "Player3", "Player4", "Player5"])
        if month_index >= len(month_cells):
            THlog(f"Invalid month index or unexpected table format for month {month_index} in {tmpdate.tm_year}", "error")
            continue


        month_cell = month_cells[month_index]

        ranking_value = month_cell.text.split('.')[0].strip()  # Get the numeric part
        link_tag = month_cell.find("a")  # Find the link in this cell
        points_value = link_tag.text.strip() if link_tag else None

        try:
            if ranking_value.isdigit():
                if return_mode == "single":
                    return ranking_value
                ranks.append(ranking_value)
                if verbose:
                    THlog(f"Found rank {ranking_value} for {time.strftime('%B %Y', tmpdate)}")
        except:
            if not supress_warnings:
                THlog(f"No valid ranking data found for {time.strftime('%B %Y', tmpdate)} skipping...", "warning")
            invalid.append(i)

        try:
            if points_value.isdigit():
                if return_mode == "single":
                    return points_value
                points.append(points_value)
                if verbose:
                    THlog(f"Found points {points_value} for {time.strftime('%B %Y', tmpdate)}")
        except:
            if not supress_warnings:
                THlog(f"No valid points data found for {time.strftime('%B %Y', tmpdate)} skipping...", "warning")
            invalid.append(i)
            
        
    
    for idx in reversed(invalid):
        dates.pop(idx)

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
    result={}
    for date, rank, point in zip(dates, ranks, points):
        date = time.strftime("%Y-%m", date)

        if getattr == "points":
            result[date]= point
        elif getattr == "rank":
            result[date]=rank
        else:
            result[date]=[point, rank]
    return result

def GetPlayerTournaments(player_ids=None, player_names=None, verbose=False, supress_warnings=False):
    player_ids = ensure_list(player_ids)
    player_names = ensure_list(player_names)

    if len(player_ids) == 0 and len(player_names) == 0:
        THlog("Please provide either a player ID or a player name.", "error")
        return
    
    # we only want the first player we find with that name, to make the lists equal length
    tmpplayer_ids =[]
    for name in player_names:
        if name == None:
            player_names.pop(0)
            continue
        tmpid = IDPlayer(name, return_mode="single", verbose=verbose)
        tmpplayer_ids.append(tmpid)

        
    tmpplayer_names = IDPlayer(player_ids, return_mode="list", verbose=verbose, direction="ID2N", supress_warnings=True)
    
    # clean up nonetypes after ensurelist
    if player_ids[0] == None:
        player_ids.pop(0)

    if verbose:
        THlog(f"Found player ids {tmpplayer_ids} from list {player_names}", "info")
        THlog(f"Found player names {tmpplayer_names} from list {player_ids}")


    player_names += tmpplayer_names
    player_ids += tmpplayer_ids

    if player_names[0] is None:
        player_names.pop(0)
    if player_ids[len(player_ids)-1] is None:
        player_ids.pop(len(player_ids)-1)

    if len(player_ids) != len(player_names):
        THlog("Player names and IDs are not the same length, my code is bad. Please report this to me on github", "error")
        return
    tournament_info = []

    for player_id in player_ids:
        url = f"https://stiga.trefik.cz/ithf/ranking/player.aspx?id={player_id}"
        if verbose:
            THlog(f"Requesting url {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        

        # Find the main tournament table
        main_table = soup.find("span", {"id": "LabTournaments"})
        if not main_table:
            THlog("Tournament data section not found.", "error")
            return

        # Parse each row from the tournament table
        rows = main_table.find_all("tr")
        if verbose:
            THlog(f"tournaments found {len(rows)}")


        player_tournament_info = []
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 7:
                continue

            # Tournament name
            name = cells[1].get_text(strip=True)
            

            # Placement (first number before '.')
            place_text = cells[5].get_text(strip=True)
            place_match = re.match(r"(\d+)", place_text)
            placement = int(place_match.group(1)) if place_match else None
            

            # Points: extract both current and original if available
            point_text = cells[6].get_text(strip=True)
            point_match = re.match(r"(\d+)(?:\s*\((\d+)\))?", point_text)
            if point_match:
                current = int(point_match.group(1))
                original = int(point_match.group(2)) if point_match.group(2) else current
            else:
                current = original = 0



        
            player_tournament_info.append([name, placement, original, current])
        tournament_info.append(player_tournament_info)
    return player_ids, player_names, tournament_info

def CalculateTournament(playerIDs=[], Value=[], level=0, verbose=False, supress_warnings=False):
    PlayersBeatenMethod = []
    NumberOfPlayersBeatenMethod = []
    ScalarMethod = []
    LinearMethod = []
    Result = [0 for _ in range(max(len(playerIDs), len(Value)))]
    WinnerPointsList=[1000, 600,500,100,70,40,20]
    coefList = [0.96,0.96, 0.92, 0.89, 0.83, 0.6, 0.4]

    if playerIDs ==[] and Value ==[]:
        THlog("Please provide a list of playerIDs or a list of best tournaments", "error")
        return
    # 3.1 Which players beaten-method

    #find each player's best tournament if not provided
    if Value ==[]:
        
        
        Info = GetPlayerTournaments(player_ids=playerIDs)

        for PlayerTournament in Info[2]:
            playername = PlayerTournament[1]
            if verbose:
                THlog(f"Found tournaments for player {IDPlayer(playername, direction='ID2N')}", "info")
            best = 0           
            bestOrig = 0
            for i in range(len(PlayerTournament)):
                currPoints = PlayerTournament[i][3]
                origpoints = PlayerTournament[i][2]
                if currPoints > best:
                    best = currPoints
                if origpoints > bestOrig:
                    bestOrig = origpoints
            if best != bestOrig:
                Value.append(bestOrig*0.8)
            else:
                Value.append(best)

        Value.sort(reverse=True)
    for i in range(len(Value)):
        remaining = len(Value) - i
        average_of_4 = 0
        if remaining >= 4:
            average_of_4 = sum(Value[i:i+4]) / 4
        else:
            average_of_4 = sum(Value[i:]) / remaining
        
        average_of_4*=coefList[level]
        PlayersBeatenMethod.append(average_of_4)
        

    # 3.2 Number of Players Beaten Method
    
        PlayersBeaten = (len(Value)-1)-i
        function = 1+(((min(70, len(Value))-1)*PlayersBeaten)/(len(Value)-1))
        NumberOfPlayersBeatenMethod.append(function)

    # 3.3 Scalar method
        ScalarMethod.append(WinnerPointsList[level]/(2**i))

    # 3.4 Linear method
        #function = 1+((WinnerPointsList[level]-1)*(len(Value)-1-i)/len(Value)-1)
        LinearMethod.append(1+(((WinnerPointsList[level]-1)*(len(Value)-i-1))/(len(Value)-1)))

    ScalarMethod[len(ScalarMethod)-1]=1
    print(f"NumberOfPlayersBeatenMethod: {NumberOfPlayersBeatenMethod}")
    print(f"PlayersBeatenMethod: {PlayersBeatenMethod}")
    print(f"ScalarMethod: {ScalarMethod}")
    print(f"LinearMethod: {LinearMethod}")

    # summarization
    #take the maximum value from each postion

    for i in range(len(NumberOfPlayersBeatenMethod)):
        i -=1
        if Result[i] < NumberOfPlayersBeatenMethod[i]:
            Result[i] = NumberOfPlayersBeatenMethod[i]
        if Result[i] < PlayersBeatenMethod[i]:
            Result[i] = PlayersBeatenMethod[i]
        if Result[i] < ScalarMethod[i]:
            Result[i] = ScalarMethod[i]
        if Result[i] < LinearMethod[i]:
            Result[i] = LinearMethod[i]
    # winner gets an extra 10 points
    Result[0]+=10
    return Result