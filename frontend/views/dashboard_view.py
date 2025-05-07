from backend.database import get_session
from backend.services.conversion_service import ConversionService
from backend.services.user_service import UserService
from backend.services.transaction_service import TransactionService
from backend.services.category_service import CategoryService

from frontend.components.RecentTransactions import RecentTransactions
from frontend.components.TransactionForm import TransactionForm
from frontend.views.transaction_view import TransactionView

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class DashboardView(tk.Frame):
    def __init__(self, parent, session, user):
        super().__init__(parent, bg="#f0fdf4")  # Light green background
        self.user = user
        self.transaction_service = TransactionService(session)
        self.category_service = CategoryService(session)
        self.conversion_service = ConversionService(session)

        # Header
        tk.Label(self, text="Dashboard", font=("Helvetica", 18, "bold"), bg="#f0fdf4").pack(pady=(20, 0))
        tk.Label(self, text=f"Welcome, {user.username.capitalize()}!", font=("Helvetica", 12), bg="#f0fdf4").pack(pady=(0, 10))

        # Navigation Buttons
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=10)

        ttk.Button(nav_frame, text="Manage Categories", command=self.go_to_categories).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="View Graphs", command=self.go_to_graphs).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Currency Converter", command=self.go_to_currency_converter).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Delete Account", command=self.delete_account).pack(side="left", padx=5)
        ttk.Button(self, text="Log Out", command=self.logout).pack(pady=(0, 10))

        # Horizontal layout container for form and recent transactions
        content_frame = ttk.Frame(self)
        content_frame.pack(pady=10)

        # Transaction Form
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", padx=20)

        ttk.Label(left_frame, text="Add a new transaction", font=("Helvetica", 12, "bold")).pack(pady=(0, 5))

        self.transaction_form = TransactionForm(
            left_frame,
            user,
            self.transaction_service,
            self.category_service,
            on_success=self.refresh_dashboard
        )
        self.transaction_form.pack()

        # Recent Transactions
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="left", padx=20)

        self.recent_transactions = RecentTransactions(
            right_frame,
            user,
            self.transaction_service
        )
        self.recent_transactions.pack()

        # Balance Overtime chart
        self.transaction_view = TransactionView(self, user, self.transaction_service)
        self.transaction_view.pack(pady=20)

        self.refresh_dashboard()

    # refresh charts on dashboard
    def refresh_dashboard(self):
        self.transaction_view.plot_balance_over_time(2)
        self.recent_transactions.refresh()

    # navigation
    def go_to_categories(self):
        from frontend.views.category_view import CategoryView
        self.pack_forget()
        CategoryView(self.master, self.transaction_service, self.category_service, self.user).pack(fill="both", expand=True)

    def go_to_graphs(self):
        from frontend.views.graphs_view import GraphsView
        self.pack_forget()
        GraphsView(self.master, self.user, self.transaction_service).pack(fill="both", expand=True)

    def go_to_currency_converter(self):
        from frontend.views.currency_converter_view import CurrencyConverterView
        self.pack_forget()
        CurrencyConverterView(self.master, self.transaction_service, self.conversion_service, self.user).pack(fill="both", expand=True)

    def delete_account(self):
        confirm = messagebox.askyesno(
            "Delete Account",
            "Are you sure you want to delete your account? This cannot be undone."
        )

        if not confirm:
            return

        password = simpledialog.askstring(
            "Confirm Password",
            "Please enter your password to confirm:",
            show="*"
        )

        if not password:
            messagebox.showwarning("Cancelled", "Account deletion cancelled.")
            return

        with get_session() as session:
            user_service = UserService(session)
            user = user_service.login_user(self.user.username, password)

            if user:
                user_service.delete_user(user.username, password)
                messagebox.showinfo("Account Deleted", "Your account has been deleted.")
                from frontend.views.login_view import LoginView
                self.pack_forget()
                LoginView(self.master, session).pack(fill="both", expand=True)
            else:
                messagebox.showerror("Authentication Failed", "Incorrect password. Account was not deleted.")

    def logout(self):
        from frontend.views.login_view import LoginView
        with get_session() as session:
            self.pack_forget()
            LoginView(self.master, session).pack(fill="both", expand=True)



