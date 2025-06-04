import backtrader as bt
import pandas as pd

data = bt.feeds.GenericCSVData(
    dataname="data/BTCUSDT_2025-06-02_UTC_with_lookback.csv",
    dtformat='%Y-%m-%d %H:%M:%S',
    timeframe=bt.TimeFrame.Minutes,
    compression=15,
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1  # No open interest in your CSV
)


class EmaCrossover(bt.Strategy):
    params = (
        ('short_period', 9),
        ('long_period', 21),
    )

    def __init__(self):
        self.short_ema = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.short_period)
        self.long_ema = bt.indicators.ExponentialMovingAverage(
            self.data.close, period=self.params.long_period)

        # Use Backtrader's built-in CrossOver indicator
        self.crossover = bt.indicators.CrossOver(self.short_ema, self.long_ema)

        # Initialize counters
        self.bullish_crossovers = 0
        self.bearish_crossovers = 0
        self.total_crossovers = 0

    def next(self):

        if self.crossover > 0:  # Bullish crossover
            self.bullish_crossovers += 1
            self.total_crossovers += 1
            print(
                f"🟢 BULLISH CROSSOVER #{self.bullish_crossovers} on {self.data.datetime.date(0)} --- {self.short_ema[0]} vs {self.long_ema[0]}")

        elif self.crossover < 0:  # Bearish crossover
            self.bearish_crossovers += 1
            self.total_crossovers += 1
            print(
                f"🔴 BEARISH CROSSOVER #{self.bearish_crossovers} on {self.data.datetime.date(0)}  --- {self.short_ema[0]} vs {self.long_ema[0]} ")


cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(EmaCrossover)

cerebro.run()


# Plot the results
cerebro.plot(
    style='candlestick',  # Use candlestick chart
    barup='green',        # Green for bullish candles
    bardown='red',        # Red for bearish candles
    volume=True,          # Show volume subplot
    plotdist=0.1,         # Distance between plots
    figsize=(15, 8)       # Figure size (width, height)
)
