import pandas as pd
from collections import deque

df = pd.read_csv('transactions.csv')

portfolios = {}
counts = {}
portfolio_net_state = {}
total_gross_profit = 0
total_fees = 0

for _, row in df.iterrows():
    p_id = row['portfolio_id']
    txn_id = row['txn_id']
    val = row['quantity'] * row['unit_price']

    counts[p_id] = counts.get(p_id, 0) + 1
    fee_rate = 0.005
    if counts[p_id] >= 5:
        fee_rate *= 0.6

    current_fee = val * fee_rate

    portfolio_net_state[p_id] = portfolio_net_state.get(p_id, 0) - current_fee
    total_fees += current_fee

    if row['type'] == 1:
        if p_id not in portfolios:
            portfolios[p_id] = deque()
        for _ in range(int(row['quantity'])):
            portfolios[p_id].append((row['unit_price'], txn_id))

    else:
        success_tax_applies = portfolio_net_state.get(p_id, 0) > 50.00

        txn_gross_profit = 0
        for _ in range(int(row['quantity'])):
            buy_price, buy_txn_id = portfolios[p_id].popleft()
            unit_profit = row['unit_price'] - buy_price

            if (txn_id - buy_txn_id) > 6:
                unit_profit *= 0.93

            if success_tax_applies:
                unit_profit *= 0.98

            txn_gross_profit += unit_profit

        total_gross_profit += txn_gross_profit
        portfolio_net_state[p_id] = portfolio_net_state.get(p_id, 0) + txn_gross_profit

szn = total_gross_profit - total_fees
print(f"Adjusted Net Profit (SZN): {round(szn, 2
