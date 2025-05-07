from tkinter.constants import RIGHT

from backend.database import get_session
from tkinter import Frame, BOTH, LEFT, X, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from frontend.utils.generate_charts import (
    plot_income_expense_over_time,
    plot_balance_over_time
)


class GraphsView(Frame):
    def __init__(self, parent, user, transaction_service):
        super().__init__(parent)
        self.parent = parent
        self.transaction_service = transaction_service
        self.user = user

        button_frame = Frame(self)
        button_frame.pack(fill=X, pady=(5, 15))  # Small padding at top

        return_btn = Button(
            button_frame,
            text="Return to Dashboard",
            command=self.return_to_dashboard,
            font=('Arial', 10),
            padx=10,
            pady=3
        )
        return_btn.pack(side=LEFT, padx=10)

        self.setup_graphs()

    def return_to_dashboard(self):
        """Handle navigation back to dashboard"""
        from frontend.views.dashboard_view import DashboardView  # Lazy import
        self.destroy()  # Remove current view
        with get_session() as session:
            DashboardView(self.parent, session, self.user).pack()

    def setup_graphs(self):
        # Main container with padding
        main_container = Frame(self, width=700, height=500)  # make container smaller than window
        main_container.pack_propagate(False)  # prevent resizing
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Left graph frame
        graph1_frame = Frame(main_container)
        graph1_frame.pack(side=LEFT)

        # Right graph frame
        graph2_frame = Frame(main_container)
        graph2_frame.pack(side=RIGHT)

        # Plot: Income vs Expense (left graph)
        income_expense_fig = plot_income_expense_over_time(self.transaction_service, self.user)
        if income_expense_fig:
            canvas1 = FigureCanvasTkAgg(income_expense_fig, master=graph1_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(padx=10, pady=5)

        # Plot: Balance over time (right graph)
        balance_fig = plot_balance_over_time(self.transaction_service, self.user, None)
        if balance_fig:
            canvas2 = FigureCanvasTkAgg(balance_fig, master=graph2_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(padx=10, pady=5)