from backend.database import get_engine
from frontend.utils.colors import RED, EMERALD_GREEN # Colors used for app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_income_expense_over_time(user_id: int):
    engine = get_engine()

    # Load transactions
    query = f"""
        SELECT date, amount, type
        FROM transactions
        WHERE user_id = {user_id}
        ORDER BY date
    """
    df = pd.read_sql_query(query, con=engine)
    if df.empty:
        print(f"No transactions found for user {user_id}")
        return

    # Ensure date is datetime (remove time part)
    df['date'] = pd.to_datetime(df['date']).dt.date

    monthly = df.copy()
    monthly['month'] = pd.to_datetime(monthly['date']).dt.to_period('M')
    monthly_grouped = monthly.groupby(['month', 'type'])['amount'].sum().unstack()

    monthly_grouped.plot(kind='bar', figsize=(12, 6), color=[RED, EMERALD_GREEN])
    plt.title(f"Monthly Income vs Expense - User {user_id}")
    plt.xlabel("Month")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', linestyle='--')
    plt.legend(title="Transaction Type")
    plt.tight_layout()
    plt.show()

def plot_balance_over_time(user_id: int):
    engine = get_engine()

    # Load initial user balance
    user_query = f"SELECT account_balance FROM users WHERE id = {user_id}"
    user_df = pd.read_sql_query(user_query, con=engine)
    if user_df.empty:
        print(f"No user found with ID {user_id}")
        return

    initial_balance = user_df.loc[0, 'account_balance']

    # Load transactions
    txn_query = f"""
        SELECT date, amount, type
        FROM transactions
        WHERE user_id = {user_id}
        ORDER BY date
    """
    df = pd.read_sql_query(txn_query, con=engine)
    if df.empty:
        print(f"No transactions found for user {user_id}")
        return

    # Prepare data
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df['amount_signed'] = df.apply(
        lambda row: row['amount'] if row['type'].lower() == 'income' else -row['amount'], axis=1
    )

    # Calculate running balance
    df['running_balance'] = initial_balance + df['amount_signed'].cumsum()

    # Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='date', y='running_balance', marker='o')
    plt.title(f"Account Balance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

user_id = 3
plot_balance_over_time(user_id)
# plot_income_expense_over_time(user_id)