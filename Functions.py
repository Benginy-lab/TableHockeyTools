import requests
from bs4 import BeautifulSoup



def GetPlayerPoints(player_id):

    points_url = 'https://stiga.trefik.cz/ithf/ranking/player.aspx?id=' + str(player_id)



    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
    }

    response_points = requests.get(points_url, headers=headers)
    response_points.raise_for_status()

    soup = BeautifulSoup(response_points.content, 'html.parser')

    points_label = soup.find(text="Points")
    if points_label:
        points_value = points_label.find_next("td").string.strip()
        print("Points Value:", points_value)
    else:
        print("ERR: Points value not found.")

def GetPlayerPos(player_id):
    player_pos_url = "http://www.ithf.info/stiga/ithf/ranking/getrank.asmx/GetRank?ID="+str(player_id)


    response_pos = requests.get(player_pos_url)
    print(response_pos.text)

def find_player_id(player_name):
    url = 'https://stiga.trefik.cz/ithf/ranking/playerID.txt'
    
    response = requests.get(url)
    response.raise_for_status()
    
    lines = response.text.splitlines()
    
    for line in lines:
        columns = line.split('\t')
        if len(columns) > 1:
            player_id, last_name, first_name = columns[0], columns[1], columns[2]
            full_name = f"{first_name} {last_name}"
            print(columns)
            if full_name.lower() == player_name.lower():
                return player_id 

    print(f"could not find a {player_name}, check for spelling mistakes. First name first then last name.")
    quit()


    
if __name__ == '__main__':
    player_name = 'Benjamin Nygard'
    if player_name == '':
            player_name = input("Enter player name: ")
    player_id = find_player_id(player_name)
    try:
        print("found player id = "+player_id)
    except NameError:
        print("ERR: Player id not found, check for spelling mistakes in %player_name%")
        quit()
    except:
        print("ERR: ay yo code ass bro")
        quit()
    GetPlayerPos(player_id)
