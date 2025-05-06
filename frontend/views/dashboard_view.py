import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
from dateutil.relativedelta import relativedelta

from backend.services.transaction_service import TransactionService
from backend.services.category_service import CategoryService
from backend.utils.enums import IncomeOrExpense
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from frontend.components.TransactionForm import TransactionForm
from frontend.views.transaction_view import TransactionView


class DashboardView(ttk.Frame):
    def __init__(self, parent, session, user):
        super().__init__(parent)
        self.user = user
        self.transaction_service = TransactionService(session)
        self.category_service = CategoryService(session)

        ttk.Label(self, text=f"Welcome, {user.username}!").pack(pady=5)

        form_view = TransactionForm(
            self,
            user,
            self.transaction_service,
            self.category_service,
            on_success=self.refresh_charts
        )
        form_view.pack(pady=10)

        self.transaction_view = TransactionView(self, user, self.transaction_service)
        self.transaction_view.pack(pady=10)
        self.plot_canvas = None
        # self.plot_summary()
        self.transaction_view.plot_balance_over_time(2)

    def refresh_charts(self):
        self.transaction_view.plot_summary()
        self.transaction_view.plot_balance_over_time(2)

    def plot_summary(self):
        transactions = self.transaction_service.get_all_transactions(self.user)
        income = sum(t.amount for t in transactions if t.type == IncomeOrExpense.INCOME)
        expense = sum(t.amount for t in transactions if t.type == IncomeOrExpense.EXPENSE)

        fig, ax = plt.subplots()
        ax.pie([income, expense], labels=["Income", "Expense"], autopct="%1.1f%%", colors=["green", "red"])
        ax.set_title("Income vs Expense")

        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()

        self.plot_canvas = FigureCanvasTkAgg(fig, master=self)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(pady=10)

    def plot_balance_over_time(self, user, last_n_months: int = None):
        initial_balance = user.account_balance

        # Get all transactions using transaction service
        transactions = self.transaction_service.get_all_transactions(self.user)
        if not transactions:
            print(f"No transactions found for user {self.user.id}")
            return

        # Prepare transaction data
        data = []
        for t in sorted(transactions, key=lambda x: x.date):
            signed_amount = t.amount if t.type == IncomeOrExpense.INCOME else -t.amount
            data.append((t.date, signed_amount))

        # Create DataFrame and compute running balance
        df = pd.DataFrame(data, columns=["date", "amount_signed"])
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        # Filter to last N months if specified
        if last_n_months:
            cutoff_date = datetime.now() - relativedelta(months=last_n_months)
            df = df[df['date'] >= cutoff_date]

        df['running_balance'] = initial_balance + df['amount_signed'].cumsum()

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['date'], df['running_balance'], marker='o', color='blue')
        ax.set_title("Account Balance Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Balance")
        ax.grid(True)

        # Set monthly ticks on x-axis
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        fig.autofmt_xdate(rotation=45)

        # Replace previous canvas if needed
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()

        self.plot_canvas = FigureCanvasTkAgg(fig, master=self)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(pady=10)

