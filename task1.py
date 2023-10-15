import pandas as pd
import numpy as np

# Load the trade log from a CSV file
df = pd.read_csv("tradelog.csv")  

# Define initial portfolio value and risk-free interest rate
initial_portfolio_value = 6500
risk_free_rate = 0.05

# Calculate the parameters
total_trades = len(df)
profitable_trades = len(df[df['Exit Price'] > df['Entry Price']])
loss_making_trades = total_trades - profitable_trades
win_rate = profitable_trades / total_trades
average_profit_per_trade = (df['Exit Price'] - df['Entry Price'])[df['Exit Price'] > df['Entry Price']].mean()
average_loss_per_trade = (df['Entry Price'] - df['Exit Price'])[df['Entry Price'] > df['Exit Price']].mean()
risk_reward_ratio = abs(average_profit_per_trade / average_loss_per_trade)
loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * average_loss_per_trade)

# Calculate portfolio returns
portfolio_returns = (df['Exit Price'] - df['Entry Price']) / df['Entry Price']
average_ror_per_trade = portfolio_returns.mean()

# Calculate Sharpe Ratio
sharpe_ratio = (average_ror_per_trade - risk_free_rate) / portfolio_returns.std()

# Calculate Max Drawdown
cumulative_returns = (portfolio_returns + 1).cumprod()
peak = cumulative_returns.expanding().max()
drawdown = (cumulative_returns - peak) / peak
max_drawdown = drawdown.min()

# Calculate Max Drawdown Percentage
max_drawdown_percentage = max_drawdown * 100

# Calculate CAGR
ending_value = cumulative_returns.iloc[-1]
beginning_value = initial_portfolio_value
number_of_periods = len(cumulative_returns)
cagr = (ending_value / beginning_value) ** (1 / number_of_periods) - 1

# Calculate Calmar Ratio
calmar_ratio = cagr / abs(max_drawdown)

# Print the results
print("Total Trades:", total_trades)
print("Profitable Trades:", profitable_trades)
print("Loss-Making Trades:", loss_making_trades)
print("Win Rate:", win_rate)
print("Average Profit per Trade:", average_profit_per_trade)
print("Average Loss per Trade:", average_loss_per_trade)
print("Risk Reward Ratio:", risk_reward_ratio)
print("Expectancy:", expectancy)
print("Average ROR per Trade:", average_ror_per_trade)
print("Sharpe Ratio:", sharpe_ratio)
print("Max Drawdown:", max_drawdown)
print("Max Drawdown Percentage:", max_drawdown_percentage)
print("CAGR:", cagr)
print("Calmar Ratio:", calmar_ratio)


new_results = pd.DataFrame({
    "Parameter": ["Total Trades", "Profitable Trades", "Loss-Making Trades", "Win Rate",
                  "Average Profit per Trade", "Average Loss per Trade", "Risk Reward Ratio",
                  "Expectancy", "Average ROR per Trade", "Sharpe Ratio", "Max Drawdown",
                  "Max Drawdown Percentage", "CAGR", "Calmar Ratio"],
    "Value": [total_trades, profitable_trades, loss_making_trades, win_rate,
              average_profit_per_trade, average_loss_per_trade, risk_reward_ratio,
              expectancy, average_ror_per_trade, sharpe_ratio, max_drawdown,
              max_drawdown_percentage, cagr, calmar_ratio]
})

# Load the existing results.csv file
existing_results = pd.read_csv("C:\\Users\\hp\\Downloads\\results.csv")

# Append the new results to the existing file
all_results = pd.concat([existing_results, new_results], ignore_index=True)


# Save the updated results to results.csv
all_results.to_csv("C:\\Users\\hp\\Downloads\\results.csv", index=False)