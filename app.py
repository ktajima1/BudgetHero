from backend.database import initialize_database

import tkinter as tk
from backend.database import get_session
from frontend.views.login_view import LoginView

def main():
    initialize_database() # Create databases

    root = tk.Tk()
    root.title("Budget Hero")
    root.geometry("600x500")

    with get_session() as session:
        app = LoginView(root, session)
        app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()
