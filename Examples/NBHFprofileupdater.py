import THfunctions.tablehockey as TH
    
if __name__ == '__main__':
    player_name = 'Benjamin Nygard'
    if player_name == '':
            player_name = input("Enter player name: ")
    player_id = TH.find_player_id(player_name)
    try:
        print("found player id = "+player_id)
    except NameError:
        print("ERR: Player id not found, check for spelling mistakes in %player_name%")
        quit()
    except:
        print("ERR: something unexpected happened when trying to find player id")
        quit()
    TH.GetPlayerPos(player_id)
