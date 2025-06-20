import THTools as TH

Info = TH.GetPlayerTournaments(player_names=["Nygard benjamin", "nygard sofie"])
for i in range(len(Info[0])):
    print(f"Tournament listings for player {TH.IDPlayer(Info[0][i], direction="ID2N")} ({Info[0][i]})")
    for tournament in Info[2][i]:
        print(f"\t{tournament[0]}: placed {tournament[1]}{"th" if tournament[1] > 1 else "st."}, {tournament[3]}({tournament[2]}) points")

