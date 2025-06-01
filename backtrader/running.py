# import matplotlib.pyplot as plt


# # Sample data
# x = [1, 2, 3, 4, 5]
# y = [10, 20, 25, 30, 40]

# # Create a plot
# plt.plot(x, y)

# # Add title and labels
# plt.title("Simple Line Chart")
# plt.xlabel("X Axis")
# plt.ylabel("Y Axis")

# # Show the plot
# plt.show()


import backtrader as bt
# import pandas as pd

btc_csv_parsed=bt.feeds.GenericCSVData(
    dataname="feeddata/BTCUSDT_1d.csv",
    dtformat=('%Y-%m-%d'),
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1
)


cerebro = bt.Cerebro()
cerebro.adddata(btc_csv_parsed)

cerebro.run()

# %matplotlib widget

cerebro.plot(style='bar')