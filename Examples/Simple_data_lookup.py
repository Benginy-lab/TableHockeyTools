import THTools as TH

    
if __name__ == "__main__":
    player_names = ['Matantsev Evgeniy', 'Kalnins Rainers']

    
    print(TH.GetPlayerID(player_names, return_mode="dict"))

    print(TH.GetPlayerRank(player_names=player_names, return_mode="dict", verbose=True))
    
    print(TH.GetPlayerPoints(player_names=player_names, return_mode="dict"))

    
        
    




