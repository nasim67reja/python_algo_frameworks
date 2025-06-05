import backtrader as bt
import pandas as pd

data = bt.feeds.GenericCSVData(
    dataname="data/BTCUSDT_2025-06-04_UTC_with_lookback.csv",
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

        self.crossover = bt.indicators.CrossOver(self.short_ema, self.long_ema)

        # Simple counters
        self.total_trades = 0
        self.winning_trades = 0
        self.total_pnl = 0.0

        self.order = None  # To keep track of pending orders

    def next(self):
        if len(self) < self.params.long_period:
            return

        # Skip if we have pending orders
        if self.order:
            return

        # Get current position
        position = self.position.size

        if self.crossover < 0:
            print(f"BEARISH CROSSOVER - Going SHORT")
            # Calculate how many units you can afford
            cash = self.broker.getcash()
            price = self.data.close[0]
            size = cash / price

            print(f"Cash: ${cash:.2f}, Price: ${price:.2f}, Size: {size}")
            self.order = self.sell(size=size)

        elif self.crossover > 0 and position < 0:
            print(f"BULLISH CROSSOVER - Closing SHORT")

            # Close the entire short position
            print(
                f"Current short position: {position} ---- Price: ${self.data.close[0]:.2f}")
            self.order = self.buy(size=abs(position))

            print("____________________________________")

    def notify_order(self, order):
        """Reset self.order when order completes"""
        if order.status in [order.Completed, order.Canceled, order.Rejected]:
            print(f"Order finished: {order.status}")
            self.order = None  # ✅ This allows new orders to be created


cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(EmaCrossover)


cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(commission=0.001)  # 0.1% commission


# print(f"Starting Value: ${cerebro.broker.getvalue():.2f}")
cerebro.run()
# print(f"Final Value: ${cerebro.broker.getvalue():.2f}")


# Plot the results
cerebro.plot(
    style='candlestick',  # Use candlestick chart
    # barup='green',        # Green for bullish candles
    # bardown='red',        # Red for bearish candles
    volume=True,          # Show volume subplot
    plotdist=0.1,         # Distance between plots
    figsize=(15, 8)       # Figure size (width, height)
)
