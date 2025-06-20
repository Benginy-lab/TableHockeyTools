import THTools as TH

    
if __name__ == "__main__":
    player_names = ['Matantsev Evgeniy', 'Kalnins Rainers']

    
    TH.THlog("Getting player ids", "info")
    print(TH.GetPlayerID(player_names, return_mode="dict"))

    TH.THlog("Getting player rankings", "info")
    print(TH.GetPlayerRank(player_names=player_names, return_mode="dict", verbose=True))
    
    TH.THlog("Getting player points", "info")
    print(TH.GetPlayerPoints(player_names=player_names, return_mode="dict"))

    
        
    




