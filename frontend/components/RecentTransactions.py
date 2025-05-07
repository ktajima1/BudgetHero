import tkinter as tk
from tkinter import ttk
from datetime import datetime

class RecentTransactions(ttk.Frame):
    def __init__(self, parent, user, transaction_service, limit=5):
        super().__init__(parent)
        self.user = user
        self.transaction_service = transaction_service
        self.limit = limit

        ttk.Label(self, text="Recent Transactions", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        for widget in self.container.winfo_children():
            widget.destroy()


        transactions = self.transaction_service.get_recent_transactions(self.user, self.limit)

        if not transactions:
            ttk.Label(self.container, text="No recent transactions.").pack(anchor="w")
            return

        for t in transactions:
            date_str = t.date.strftime("%Y-%m-%d")
            type_str = t.type.name.capitalize()
            sign = "+" if type_str == "Income" else "-"
            color = "green" if type_str == "Income" else "red"
            entry = f"{date_str} | {type_str} | {sign}${abs(t.amount):.2f} | {t.description}"

            label = ttk.Label(self.container, text=entry, foreground=color)
            label.pack(anchor="w", pady=2)
