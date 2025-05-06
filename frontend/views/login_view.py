import tkinter as tk
from tkinter import ttk, messagebox
from backend.services.user_service import UserService
from frontend.views.register_view import RegisterView
from frontend.views.dashboard_view import DashboardView

class LoginView(ttk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.session = session
        self.user_service = UserService(session)
        self.parent = parent

        self.username_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")

        ttk.Label(self, text="Login").pack(pady=10)
        ttk.Label(self, text="Username").pack()
        self.username_entry.pack()

        ttk.Label(self, text="Password").pack()
        self.password_entry.pack()

        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=self.go_to_register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_service.login_user(username, password)
        if user:
            self.pack_forget()
            DashboardView(self.parent, self.session, user).pack(fill="both", expand=True)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def go_to_register(self):
        self.pack_forget()
        RegisterView(self.parent, self.session).pack(fill="both", expand=True)
