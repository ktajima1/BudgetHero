import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Frame, Button, BOTH, LEFT, RIGHT, X, Y, W, NO, YES, VERTICAL, END, NORMAL, DISABLED

from backend.database import get_session

class CategoryView(Frame):
    def __init__(self, parent, transaction_service, category_service, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.transaction_service = transaction_service
        self.category_service = category_service

        self.setup_ui()
        self.load_categories()

    def setup_ui(self):
        """
        Set up the UI components
        """
        self.pack(fill=BOTH, expand=True)

        # Button container
        button_frame = Frame(self)
        button_frame.pack(fill=X, pady=(5, 15))

        # Return to Dashboard button
        return_btn = Button(
            button_frame,
            text="Return to Dashboard",
            command=self.return_to_dashboard,
            font=('Arial', 10),
            padx=10,
            pady=3
        )
        return_btn.pack(side=LEFT, padx=10)

        # Add New Category button
        add_btn = Button(
            button_frame,
            text="Add New Category",
            command=self.add_category,
            font=('Arial', 10),
            padx=10,
            pady=3
        )
        add_btn.pack(side=RIGHT, padx=10)

        content_frame = Frame(self)
        content_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Treeview for categories
        self.tree = ttk.Treeview(
            content_frame,
            columns=('id', 'name', 'description'),
            show='headings',
            selectmode='browse'
        )
        self.tree.pack(fill=BOTH, expand=True, pady=(0, 5))

        # Configure columns
        self.tree.heading('id', text='ID', anchor=W)
        self.tree.heading('name', text='Category Name', anchor=W)
        self.tree.heading('description', text='Description', anchor=W)

        self.tree.column('id', width=50, stretch=NO)
        self.tree.column('name', width=150, stretch=YES)
        self.tree.column('description', width=300, stretch=YES)

        # buttons frame
        button_frame = Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        # Edit button
        edit_btn = Button(
            button_frame,
            text="Edit Selected",
            command=self.edit_category,
            state=DISABLED
        )
        edit_btn.pack(side=LEFT, padx=5)
        self.edit_btn = edit_btn

        # Delete button
        delete_btn = Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_category,
            state=DISABLED
        )
        delete_btn.pack(side=LEFT, padx=5)
        self.delete_btn = delete_btn

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def load_categories(self):
        """
        Load categories from database into the treeview
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch categories using category_service
        categories = self.category_service.get_all_categories()

        # Populate treeview
        for category in categories:
            self.tree.insert(
                '',
                END,
                values=(category.id, category.category_name, category.description)
            )

    def on_tree_select(self, event):
        """
        Enable buttons when a category is selected
        """
        selected = self.tree.selection()
        if selected:
            self.edit_btn.config(state=NORMAL)
            self.delete_btn.config(state=NORMAL)
        else:
            self.edit_btn.config(state=DISABLED)
            self.delete_btn.config(state=DISABLED)

    def add_category(self):
        # Get category name
        name = simpledialog.askstring(
            "Add Category",
            "Enter category name:",
            parent=self
        )
        if not name:  # User clicked cancel
            return

        name = name.strip()
        if not name:
            messagebox.showerror("Error", "Category name cannot be empty")
            return

        # Get description
        description = simpledialog.askstring(
            "Add Category",
            f"Enter description for '{name}':\n(Leave empty for no description)",
            parent=self
        )
        description = description.strip() if description else ""
        try:
            success = self.category_service.create_category(category_name=name, description=description)
            if success:
                messagebox.showinfo("Success", f"Category '{name}' added successfully")
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to add category")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def edit_category(self):
        """
        Edit selected category
        """
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            category_id, old_name, old_desc = item['values']

            # Get new category name
            new_name = simpledialog.askstring(
                "Edit Category",
                "Edit category name:",
                initialvalue=old_name,
                parent=self
            )

            if new_name is None:  # User clicked cancel
                return

            new_name = new_name.strip()
            if not new_name:
                messagebox.showerror("Error", "Category name cannot be empty")
                return

            # Get new description
            new_desc = simpledialog.askstring(
                "Edit Category",
                "Edit description:",
                initialvalue=old_desc,
                parent=self
            )
            new_desc = new_desc.strip() if new_desc else ""

            try:
                target_category = self.category_service.get_category_by_id(category_id)
                success = self.category_service.modify_category(
                    category=target_category,
                    category_name=new_name,
                    description=new_desc
                )

                if success:
                    messagebox.showinfo("Success", "Category updated successfully")
                    self.load_categories()  # Refresh the list
                else:
                    messagebox.showerror("Error", "Failed to update category")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_category(self):
        """
        Delete selected category
        """
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            category_id = item['values'][0]

            # Confirm deletion
            if messagebox.askyesno(
                    "Confirm Delete",
                    f"Delete category '{item['values'][1]}'?"
            ):
                target_category = self.category_service.get_category_by_id(category_id)
                success = self.category_service.delete_category(target_category)
                if success:
                    self.load_categories()
                    messagebox.showinfo("Success", "Category deleted")
                else:
                    messagebox.showerror("Error", "Failed to delete category")

    def return_to_dashboard(self):
        """Navigate back to dashboard"""
        from frontend.views.dashboard_view import DashboardView  # Lazy import
        self.destroy()  # Remove current view
        with get_session() as session:
            DashboardView(self.parent, session, self.user).pack()