import THTools as TH

players = ["nygard benjamin", "nygard daniel"]
Tournaments = TH.GetPlayerTournaments(player_names=players, verbose=True)
for i in range(len(Tournaments[0])):
    print(f"---------------- Tournament stats for player: {Tournaments[1][i].upper()}-----------")
    print(f"""
    Amount of Tournaments: {len(Tournaments[2][i])}

""")
    for tournament in Tournaments[2][i]:
        if len(tournament[0]) > 20:
            print(f"{tournament[0][:20]}:\t\t| position:{tournament[1]}\t\t | points:{tournament[2]}({tournament[3]}) \n{tournament[0][20:]}")
        
        else:
            print(f"{tournament[0]}:\t\t| position:{tournament[1]}\t\t| points:{tournament[2]}({tournament[3]})")
