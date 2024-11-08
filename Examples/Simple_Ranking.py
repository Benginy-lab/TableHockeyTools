import THTools as TH


    
if __name__ == "__main__":
    player_names = ['Evigeny Matansev', 'Rainers Kalnins']
    player_ids = []
    for player_name in player_names:
        player_ids.append(TH.GetPlayerID(player_name))
    
    try:
        print("found player ids = "+str(player_ids))
    except NameError:
        print("ERR: Player id not found, check for spelling mistakes in %player_names%")
        quit()
    except:
        print("ERR: something unexpected happened when trying to find player ids")
        quit()
    
        
    




