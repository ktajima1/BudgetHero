import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import pandas as pd
from dateutil.relativedelta import relativedelta
from backend.utils.enums import IncomeOrExpense

class TransactionView(ttk.Frame):
    def __init__(self, parent, user, transaction_service):
        super().__init__(parent)
        self.user = user
        self.transaction_service = transaction_service
        self.plot_canvas = None

        self.plot_balance_over_time(last_n_months=2)

    def plot_balance_over_time(self, last_n_months=None):
        initial_balance = self.user.account_balance
        transactions = self.transaction_service.get_all_transactions(self.user)
        if not transactions:
            return

        data = []
        for t in sorted(transactions, key=lambda x: x.date):
            signed_amount = t.amount if t.type == IncomeOrExpense.INCOME else -t.amount
            data.append((t.date, signed_amount))

        df = pd.DataFrame(data, columns=["date", "amount_signed"])
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        if last_n_months:
            cutoff_date = datetime.now() - relativedelta(months=last_n_months)
            df = df[df['date'] >= cutoff_date]

        df['running_balance'] = initial_balance + df['amount_signed'].cumsum()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['date'], df['running_balance'], marker='o', color='blue')
        ax.set_title("Account Balance Last Two Months")
        ax.set_xlabel("Date")
        ax.set_ylabel("Balance")
        ax.grid(True)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        fig.autofmt_xdate(rotation=45)

        self._update_plot(fig)

    def _update_plot(self, fig):
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()
        self.plot_canvas = FigureCanvasTkAgg(fig, master=self)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(pady=10)
