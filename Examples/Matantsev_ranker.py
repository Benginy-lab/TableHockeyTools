import THTools as TH

players = TH.GetPlayerID(["Matantsev"], return_mode="list")
PlayerDict = TH.GetPlayerPoints(players, return_mode="dict")
ranks = TH.LocalRanker(PlayerDict)
for rank in ranks:
    print(rank)
