import THTools as TH


    
if __name__ == "__main__":
    player_names = ['Matantsev Evgeniy', 'Kalnins Rainers']
    player_ids = []
    for player_name in player_names:
        player_ids.append(TH.GetPlayerID(player_name))
    
    try:
        for player_id, player_name in zip(player_ids, player_names):
            print(f"Player {player_name} has {TH.GetPlayerPoints(player_id)} points")
            print(f"Player {player_name} is ranked {TH.GetPlayerRank(player_id)}")
    except NameError:
        print("ERR: Player id not found, check for spelling mistakes in %player_names%")
        quit()
    except:
        print("ERR: something unexpected happened when trying to find player ids")
        quit()
    
    
        
    




