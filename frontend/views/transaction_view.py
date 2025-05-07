import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import pandas as pd
from dateutil.relativedelta import relativedelta
from backend.utils.enums import IncomeOrExpense
from frontend.utils.generate_charts import plot_balance_over_time


class TransactionView(ttk.Frame):
    def __init__(self, parent, user, transaction_service):
        super().__init__(parent)
        self.user = user
        self.transaction_service = transaction_service
        self.plot_canvas = None

        self.plot_balance_over_time(last_n_months=2)

    def plot_balance_over_time(self, last_n_months=None):
        balance_fig = plot_balance_over_time(self.transaction_service, self.user, 2)

        self._update_plot(balance_fig)

    def _update_plot(self, fig):
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()
        self.plot_canvas = FigureCanvasTkAgg(fig, master=self)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(pady=10)
