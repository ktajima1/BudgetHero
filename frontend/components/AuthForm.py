import tkinter as tk
from tkinter import messagebox

class AuthForm(tk.Frame):
    def __init__(self, parent, on_login, on_register):
        super().__init__(parent)
        self.on_login = on_login
        self.on_register = on_register

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.handle_login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self, text="Register", command=self.handle_register)
        self.register_button.pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username and password:
            self.on_login(username, password)
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username and password:
            self.on_register(username, password)
        else:
            messagebox.showwarning("Missing Fields", "Please enter both username and password.")
