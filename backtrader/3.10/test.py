import backtrader as bt
# import pandas as pd

btc_csv_parsed=bt.feeds.GenericCSVData(
    dataname="BTCUSDT_1d.csv",
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

cerebro.plot(style='bar', barup='green', bardown='red', volume=False, subplot=False, plotlinelabels=True, plotymargin=0.1, plotymargin2=0.1, plotyhlines=True, plotyhlinescolor='blue', plotyhlineswidth=1.5, plotyhlinesstyle='--', plotyhlinesalpha=0.5)
