import tkinter as tk
from tkinter import ttk, messagebox, StringVar, Entry, Label, Button, Frame, LEFT, BOTH, X
from datetime import datetime, date
from tkcalendar import DateEntry  # Requires tkcalendar package (pip install tkcalendar)

from backend.database import get_session
from backend.utils.supported_currencies import SUPPORTED_CURRENCIES


class CurrencyConverterView(Frame):
    def __init__(self, parent, transaction_service, conversion_service, user):
        super().__init__(parent)
        self.parent = parent # For dashboard navigation purposes
        self.user = user # For dashboard navigation purposes

        self.conversion_service = conversion_service
        self.supported_currencies = sorted(SUPPORTED_CURRENCIES)
        self.setup_ui()

    def setup_ui(self):
        """Set up the currency converter interface"""
        self.pack(fill=BOTH, expand=True, padx=20, pady=20)

        return_frame = Frame(self)
        return_frame.grid(row=0, column=0, columnspan=1, pady=10)

        # Button to return to dashboard
        return_btn = Button(
            return_frame,
            text="Return to Dashboard",
            command=self.return_to_dashboard,
            width=20
        )
        return_btn.pack(side=LEFT, padx=10)

        # Display a calendar to select date
        Label(self, text="Conversion Date:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = DateEntry(
            self,
            date_pattern='yyyy-mm-dd',
            maxdate=date.today(),  # Can't select future dates
            mindate=date(1999, 1, 1)  # Reasonable minimum for currency data
        )
        self.date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Amount Entry
        Label(self, text="Amount:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = Entry(self, width=15)
        self.amount_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.amount_entry.insert(0, "1.00")

        # Base Currency Dropdown
        Label(self, text="From Currency:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.base_currency = StringVar()
        base_dropdown = ttk.Combobox(
            self,
            textvariable=self.base_currency,
            values=self.supported_currencies,
            state="readonly",
            width=12
        )
        base_dropdown.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        base_dropdown.current(0)

        # Target Currency Dropdown
        Label(self, text="To Currency:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.target_currency = StringVar()
        target_dropdown = ttk.Combobox(
            self,
            textvariable=self.target_currency,
            values=self.supported_currencies,
            state="readonly",
            width=12
        )
        target_dropdown.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        target_dropdown.current(1 if len(self.supported_currencies) > 1 else 0)

        # Convert and swap nuttons
        button_frame = Frame(self)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        convert_btn = Button(
            button_frame,
            text="Convert",
            command=self.convert_currency,
            width=10
        )
        convert_btn.pack(side=LEFT, padx=5)

        swap_btn = Button(
            button_frame,
            text="Swap Currencies",
            command=self.swap_currencies,
            width=15
        )
        swap_btn.pack(side=LEFT, padx=5)

        # Display results
        self.result_var = StringVar(value="Select currencies and date to convert")
        result_label = Label(
            self,
            textvariable=self.result_var,
            font=('Arial', 10, 'bold'),
            wraplength=300
        )
        result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def return_to_dashboard(self):
        """Navigate back to dashboard"""
        from frontend.views.dashboard_view import DashboardView  # Lazy import
        self.destroy()  # Remove current view
        with get_session() as session:
            DashboardView(self.parent, session, self.user).pack()

    def swap_currencies(self):
        """Swap base and target currencies"""
        current_base = self.base_currency.get()
        current_target = self.target_currency.get()

        if current_base and current_target:
            self.base_currency.set(current_target)
            self.target_currency.set(current_base)
            if "=" in self.result_var.get():
                self.convert_currency()

    def convert_currency(self):
        """Convert currency using historical date data from API"""
        try:
            # Get input values
            amount = float(self.amount_entry.get())
            base_curr = self.base_currency.get()
            target_curr = self.target_currency.get()
            selected_date = self.date_entry.get_date()

            # Validate inputs
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return

            if not base_curr or not target_curr:
                messagebox.showerror("Error", "Please select both currencies")
                return

            if base_curr == target_curr:
                self.result_var.set(f"{amount:.2f} {base_curr} = {amount:.2f} {target_curr} (same currency)")
                return

            # Get conversion rate for selected date
            rate_obj = self.conversion_service.get_rate(
                base_currency=base_curr,
                target_currency=target_curr,
                date=selected_date
            )

            if rate_obj is None:
                messagebox.showerror("Error",
                                     f"Could not get conversion rate for {selected_date.strftime('%Y-%m-%d')}\n"
                                     "The rate might not be available for this date.")
                return

            # Calculate and display result
            converted_amount = amount * rate_obj.rate
            self.result_var.set(
                f"On {selected_date.strftime('%Y-%m-%d')}:\n"
                f"{amount:.2f} {base_curr} = {converted_amount:.2f} {target_curr}\n"
                f"Exchange Rate: 1 {base_curr} = {rate_obj.rate:.6f} {target_curr}"
            )

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")