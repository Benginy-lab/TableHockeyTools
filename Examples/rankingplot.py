import matplotlib.pyplot as plt
import THTools as TH
import time
from datetime import datetime


id = TH.GetPlayerID("nygard benjamin")
now = time.localtime()
yearago = f"{now.tm_year-1}-{now.tm_mon}"

data = TH.GetHistory(id, yearago, date_end=now, getattr="points", return_mode="dict", verbose=True)
print(data)
x_values = data.values()
y_values = [datetime.strptime(date_str, "%Y-%m") for date_str in data.keys()]
print(y_values)

plt.scatter(x_values, y_values)
plt.gcf().autofmt_xdate()
