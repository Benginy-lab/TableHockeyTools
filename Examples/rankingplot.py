from TableHockeyTools.THTools import GetPlayerName
import matplotlib.pyplot as plt
import time
import THTools as TH
from matplotlib.patches import FancyBboxPatch

# Sample data
playername = input("input player name: \n")
playerid = TH.GetPlayerID(playername, return_mode="single")
now = time.localtime()
yearago = f"{now.tm_year - 1}-{now.tm_mon}"
data = TH.GetHistory(playerid, yearago, now, return_mode="dict")

y_values = list(data.values())
x_values = [time.mktime(time.strptime(date_str, "%Y-%m")) for date_str in data.keys()]

# Create a figure and add a rounded background patch

# Scatter plot
plt.plot(x_values, y_values, color='blue', marker='o')

# Labeling the plot
plt.title(f"Plot for {str(TH.GetPlayerName([playerid]))}")
plt.ylabel("Y values")
plt.xlabel("X values (Date)")


# Custom formatting of the y-axis to show dates
plt.gcf().autofmt_xdate()
# Display the plot
plt.show()
