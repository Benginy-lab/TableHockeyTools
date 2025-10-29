import matplotlib.pyplot as plt
import time
import THTools as TH
from datetime import datetime


class player:
    def __init__(self, playername):
        self.playername= playername
        self.playerid = None

        self.data = None
        self.max_y = None

        self.x_values = []
        self.y_values = []

    def getdata(self, start, stop):
        self.playerid = TH.IDPlayer(self.playername, return_mode="single", direction="N2ID", verbose=True)

        self.data = TH.GetHistory(self.playerid, start, date_end=stop, getattr="points", return_mode="dict", supress_warnings=False)
        if self.data != None:
            self.x_values = [datetime.strptime(date_str, "%Y-%m") for date_str in self.data.keys()]
            self.y_values = [int(value) for value in self.data.values()]
            self.max_y = max(self.y_values)
            plt.plot(self.x_values, self.y_values, color='blue')

now = time.localtime()
yearago = f"{now.tm_year - 10}-{now.tm_mon}"

player1 = player(input("enter player 1: "))
player2 = player(input("\nenter player 2: "))


player1.getdata(yearago, now)
player2.getdata(yearago, now)


plt.ylim(0, max(player1.max_y, player2.max_y)*1.1)

names = TH.IDPlayer([player1.playerid, player2.playerid], return_mode="list", direction="ID2N")
plt.title(f"Plot for {names[0]} and {names[1]}")
plt.ylabel("Y values")
plt.xlabel("X values (Date)")


plt.gcf().autofmt_xdate()

plt.show()
