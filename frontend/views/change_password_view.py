import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

from backend.services.user_service import UserService
from frontend.views.register_view import RegisterView
from frontend.views.dashboard_view import DashboardView

class ChangePasswordView(tk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent, bg="#f0fdf4")  # Light green background
        self.session = session
        self.user_service = UserService(session)
        self.parent = parent

        # Title
        tk.Label(self, text="BudgetHero", font=("Helvetica", 24, "bold"), fg="#166534", bg="#f0fdf4").pack(
            pady=(40, 10))
        tk.Label(self, text="Reset Password", font=("Helvetica", 16), bg="#f0fdf4").pack(pady=(0, 20))

        # Username
        form_frame = tk.Frame(self, bg="#f0fdf4")
        form_frame.pack()

        tk.Label(form_frame, text="Username", font=("Helvetica", 12), bg="#f0fdf4").pack(anchor="w")
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(form_frame, text="New Password", font=("Helvetica", 12), bg="#f0fdf4").pack(anchor="w")
        self.password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 12), width=30)
        self.password_entry.pack(pady=5)

        tk.Label(form_frame, text="Confirm Password", font=("Helvetica", 12), bg="#f0fdf4").pack(anchor="w")
        self.confirm_password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 12), width=30)
        self.confirm_password_entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self, bg="#f0fdf4")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Change Password", font=("Helvetica", 12, "bold"), bg="#4ade80", fg="white",
                  width=15, command=self.change_password).pack(pady=5)

        tk.Button(button_frame, text="Back to Login", font=("Helvetica", 12), bg="white", fg="#16a34a",
                  width=15, relief="groove", command=self.back_to_login).pack()

    def change_password(self):
        username = self.username_entry.get()
        new_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if self.user_service.check_if_user_exists(username) is False:
            messagebox.showerror("Failed", "Username does not exist")
        else:
            if new_password != confirm_password:
                messagebox.showerror("Failed", "Passwords do not match")
            else:
                success = self.user_service.change_password(username, new_password)
                if isinstance(success, Dict):
                    messagebox.showerror("Failed", "Change password failed. Password requirements not met")
                else:
                    messagebox.showinfo("Success", "Password changed.")
                    self.back_to_login()

    def back_to_login(self):
        from frontend.views.login_view import LoginView
        self.pack_forget()
        LoginView(self.parent, self.session).pack(fill="both", expand=True)
