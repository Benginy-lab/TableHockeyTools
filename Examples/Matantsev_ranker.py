import THTools as TH

players = TH.IDPlayer("Matantsev", return_mode="list", direction="N2ID", verbose=True)
PlayerDict = TH.GetPlayerPoints(players, return_mode="dict")
ranks = TH.LocalRanker(PlayerDict)
for rank in ranks:
    print(rank)
