import vectorbt as vbt
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Set timezone for Bangladesh
bd_tz = pytz.timezone('Asia/Dhaka')

# Define time window (8-10 PM Bangladesh time)
start_hour = 20
end_hour = 22

# Get date range for last 1 month
end_date = datetime.now(bd_tz)
start_date = end_date - timedelta(days=30)

# Download 5-min BTC-USD data for the last month
price = vbt.YFData.download(
    'ETH-USD',
    interval='5m',
    start=start_date.strftime('%Y-%m-%d'),
    end=end_date.strftime('%Y-%m-%d')
).get('Close')

# Convert index to Bangladesh time
price.index = price.index.tz_convert('Asia/Dhaka')

# Filter for 8-10 PM each day
price = price[(price.index.hour >= start_hour) & (price.index.hour < end_hour)]

# Calculate EMAs
ema_fast = vbt.MA.run(price, window=5, short_name='EMA5', ewm=True).ma
ema_slow = vbt.MA.run(price, window=10, short_name='EMA10', ewm=True).ma

# Generate signals
entries = (ema_fast > ema_slow) & (ema_fast.shift(1) <= ema_slow.shift(1))
exits = (ema_fast < ema_slow) & (ema_fast.shift(1) >= ema_slow.shift(1))

# Simulate trades with 1% risk-to-reward ratio
# For simplicity, assume fixed position size and no compounding
risk_pct = 0.01
reward_pct = 0.01

# Calculate stop loss and take profit levels
stop_loss = price * (1 - risk_pct)
take_profit = price * (1 + reward_pct)

# Run backtest
pf = vbt.Portfolio.from_signals(
    price,
    entries,
    exits,
    sl_stop=stop_loss,
    tp_stop=take_profit,
    init_cash=1000,
    fees=0.0005,
    freq='5T'
)

# Output total profit and loss
# print('Total Profit and Loss for 1 Month:')
# print(pf.total_profit)
# print('Total Return (%):')
# print(pf.total_return * 100)

# Output total profit and loss
print('Total Profit and Loss for 1 Month:')
print(pf.total_profit())
print('Total Return (%):')
print(pf.total_return() * 100)
