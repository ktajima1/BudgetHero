from backend.database import get_engine
from backend.models.user import User
from backend.services.transaction_service import TransactionService
from backend.utils.enums import IncomeOrExpense
from frontend.utils.colors import RED, EMERALD_GREEN # Colors used for app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_income_expense_over_time(transaction_service: TransactionService, user: User) -> plt.Figure | None:
    transactions = transaction_service.get_all_transactions(user)
    if not transactions:
        print(f"No transactions found for user {user.id}")
        return None

    data = [{
        "date": t.date.date(),
        "amount": t.amount,
        "type": t.type.value
    } for t in transactions]

    df = pd.DataFrame(data)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly_grouped = df.groupby(['month', 'type'])['amount'].sum().unstack()

    fig, ax = plt.subplots(figsize=(6, 8))
    monthly_grouped.plot(kind='bar', ax=ax, color=[RED, EMERALD_GREEN])
    ax.set_title(f"Monthly Income vs Expense - User {user.id}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount")
    ax.grid(True, axis='y', linestyle='--')
    ax.legend(title="Transaction Type")
    fig.tight_layout()
    return fig

from pandas.tseries.offsets import DateOffset
from datetime import datetime

def plot_balance_over_time(transaction_service: TransactionService, user: User, n_months: int | None) -> plt.Figure | None:
    transactions = transaction_service.get_all_transactions(user)
    if not transactions:
        print(f"No transactions found for user {user.id}")
        return None

    initial_balance = user.account_balance

    data = []
    for t in transactions:
        sign = 1 if t.type == IncomeOrExpense.INCOME else -1
        data.append({
            "date": pd.to_datetime(t.date),
            "signed_amount": sign * t.amount
        })

    df = pd.DataFrame(data)
    df.sort_values("date", inplace=True)

    # Only filter by date if n_months is specified
    if n_months is not None:
        cutoff_date = datetime.now() - DateOffset(months=n_months)
        df = df[df["date"] >= cutoff_date]
        time_period_title = f"Last {n_months} Months"
    else:
        time_period_title = "All Time"

    if df.empty:
        print(f"No transactions in the specified time period.")
        return None

    df["running_balance"] = initial_balance + df["signed_amount"].cumsum()

    fig, ax = plt.subplots(figsize=(6, 8))
    sns.lineplot(data=df, x="date", y="running_balance", marker='o', ax=ax)
    ax.set_title(f"Account Balance Over {time_period_title}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Balance")
    ax.grid(True)
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig
