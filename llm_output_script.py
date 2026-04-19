import pandas as pd

# Wczytanie danych
df = pd.read_csv("transactions.csv")

# Sortowanie po czasie
df = df.sort_values("txn_id")

total_profit = 0.0
total_fees = 0.0

# Przetwarzanie per portfolio
for portfolio_id, group in df.groupby("portfolio_id"):
    group = group.sort_values("txn_id")

    fifo = []  # lista [quantity, price, txn_id]
    txn_count = 0
    net_profit_portfolio = 0.0  # ZNP

    for _, row in group.iterrows():
        txn_count += 1

        qty = row["quantity"]
        price = row["unit_price"]
        txn_id = row["txn_id"]
        txn_type = row["type"]

        # --- Podatek PT ---
        fee = 0.005 * qty * price

        # Rabat od 5 transakcji
        if txn_count >= 5:
            fee *= 0.6

        total_fees += fee
        net_profit_portfolio -= fee  # najpierw odejmujemy

        # --- KUPNO ---
        if txn_type == 1:
            fifo.append([qty, price, txn_id])

        # --- SPRZEDAŻ ---
        else:
            remaining = qty
            profit = 0.0

            while remaining > 0:
                buy_qty, buy_price, buy_txn = fifo[0]

                take = min(remaining, buy_qty)

                # zysk jednostkowy
                unit_profit = price - buy_price

                # degradacja czasowa
                if txn_id - buy_txn > 6:
                    unit_profit *= 0.93

                profit += unit_profit * take

                # aktualizacja FIFO
                if take == buy_qty:
                    fifo.pop(0)
                else:
                    fifo[0][0] -= take

                remaining -= take

            # --- Dynamiczny podatek -2% ---
            if net_profit_portfolio > 50:
                profit *= 0.98

            total_profit += profit
            net_profit_portfolio += profit

# --- Wynik końcowy ---
szn = total_profit - total_fees
print(round(szn, 2))
