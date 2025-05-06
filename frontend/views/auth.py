import tkinter as tk
from tkinter import messagebox

from frontend.components.AuthForm import AuthForm
from backend.services.user_service import UserService
from backend.database import get_session

class AuthWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x250")

        session = get_session()  # SQLAlchemy session
        self.user_service = UserService(session)

        self.auth_form = AuthForm(self, self.login_user, self.register_user)
        self.auth_form.pack(padx=20, pady=20)

    def login_user(self, username, password):
        with get_session() as session:
            user_service = UserService(session)
            user = user_service.login_user(username, password)
            if user:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                # Transition to next view here
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

    def register_user(self, username, password):
        with get_session() as session:
            user_service = UserService(session)
            user = user_service.register_user(username, password)
            if user:
                messagebox.showinfo("Registration Successful", "Account created. You can now log in.")
            else:
                messagebox.showerror("Registration Failed", "Check your input or try a different username.")


