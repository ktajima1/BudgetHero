import tkinter as tk
from tkinter import ttk, messagebox
from backend.services.user_service import UserService
from frontend.views.change_password_view import ChangePasswordView
from frontend.views.register_view import RegisterView
from frontend.views.dashboard_view import DashboardView

class LoginView(tk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent, bg="#f0fdf4")  # Light green background
        self.session = session
        self.user_service = UserService(session)
        self.parent = parent

        # Title
        tk.Label(self, text="BudgetHero", font=("Helvetica", 24, "bold"), fg="#166534", bg="#f0fdf4").pack(pady=(40, 10))
        tk.Label(self, text="Login", font=("Helvetica", 16), bg="#f0fdf4").pack(pady=(0, 20))

        # Username
        form_frame = tk.Frame(self, bg="#f0fdf4")
        form_frame.pack()

        tk.Label(form_frame, text="Username", font=("Helvetica", 12), bg="#f0fdf4").pack(anchor="w")
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(form_frame, text="Password", font=("Helvetica", 12), bg="#f0fdf4").pack(anchor="w")
        self.password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 12), width=30)
        self.password_entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self, bg="#f0fdf4")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#4ade80", fg="white",
                  width=15, command=self.login).pack(pady=5)

        tk.Button(button_frame, text="Register", font=("Helvetica", 12), bg="white", fg="#16a34a",
                  width=15, relief="groove", command=self.go_to_register).pack()

        tk.Button(button_frame, text="Forgot Password", font=("Helvetica", 12), bg="white", fg="#16a34a",
                  width=15, relief="groove", command=self.go_to_reset_password).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_service.login_user(username, password)
        if user:
            self.destroy()
            DashboardView(self.parent, self.session, user).pack(fill="both", expand=True)
            self.parent.geometry("900x900")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def go_to_register(self):
        self.pack_forget()
        RegisterView(self.parent, self.session).pack(fill="both", expand=True)

    def go_to_reset_password(self):
        self.pack_forget()
        ChangePasswordView(self.parent, self.session).pack(fill="both", expand=True)

