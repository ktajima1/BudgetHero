import tkinter as tk
from tkinter import ttk, messagebox
from backend.services.user_service import UserService
# from frontend.views.login_view import LoginView

class RegisterView(ttk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.session = session
        self.user_service = UserService(session)
        self.parent = parent

        self.username_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")

        ttk.Label(self, text="Register").pack(pady=10)
        ttk.Label(self, text="Username").pack()
        self.username_entry.pack()

        ttk.Label(self, text="Password").pack()
        self.password_entry.pack()

        ttk.Button(self, text="Register", command=self.register).pack(pady=10)
        ttk.Button(self, text="Back to Login", command=self.back_to_login).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_service.register_user(username, password)
        if user:
            messagebox.showinfo("Success", "User registered.")
            self.back_to_login()
        else:
            messagebox.showerror("Failed", "Registration failed.")

    def back_to_login(self):
        from frontend.views.login_view import LoginView
        self.pack_forget()
        LoginView(self.parent, self.session).pack(fill="both", expand=True)
