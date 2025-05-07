import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

from tkcalendar import DateEntry


class TransactionForm(ttk.Frame):
    def __init__(self, parent, user, transaction_service, category_service, on_success=None):
        super().__init__(parent)
        self.user = user
        self.transaction_service = transaction_service
        self.category_service = category_service
        self.on_success = on_success

        self.type_var = tk.StringVar(value="income")
        self.category_var = tk.StringVar()
        self.date_entry = ttk.Entry(self)
        self.amount_entry = ttk.Entry(self)
        self.description_entry = ttk.Entry(self)

        self.categories = self.category_service.get_all_categories()
        self.category_map = {cat.category_name: cat.id for cat in self.categories}

        # Amount
        ttk.Label(self, text="Amount").pack()
        self.amount_entry.pack()

        # Type
        ttk.Label(self, text="Type").pack()
        ttk.Combobox(self, textvariable=self.type_var, values=["income", "expense"], state="readonly").pack()

        # Category
        ttk.Label(self, text="Category").pack()
        ttk.Combobox(self, textvariable=self.category_var, values=list(self.category_map.keys()), state="readonly").pack()

        # Description
        ttk.Label(self, text="Description").pack()
        self.description_entry.pack()

        # Date
        ttk.Label(self, text="Date (YYYY-MM-DD)").pack()
        # self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        # self.date_entry.pack()
        self.date_entry = DateEntry(
            self,
            date_pattern='yyyy-mm-dd',
            maxdate=date.today(),  # Can't select future dates
            mindate=date(1999, 1, 1)  # Reasonable minimum for currency data
        )
        self.date_entry.pack()

        ttk.Button(self, text="Add Transaction", command=self.add_transaction).pack(pady=10)

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            type_str = self.type_var.get()
            category_name = self.category_var.get()
            category_id = self.category_map.get(category_name)
            description = self.description_entry.get()

            # Parse and validate date
            try:
                date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            result = self.transaction_service.create_transaction(
                self.user, amount, type_str, date, category_id, description
            )

            if isinstance(result, dict):
                error_message = "\n".join([f"{field.capitalize()}: {msg}" for field, msg in result.items()])
                messagebox.showerror("Validation Error", error_message)
            elif result is None:
                messagebox.showerror("Error", "Transaction creation failed.")
            else:
                messagebox.showinfo("Success", "Transaction added successfully.")
                if self.on_success:
                    self.on_success()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
