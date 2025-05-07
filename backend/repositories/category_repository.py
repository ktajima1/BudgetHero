from backend.models.category import Category
from typing import List

class CategoryRepository():
    """
    This is the repository for the categories, used to insert, delete, modify, and retrieve data from the Category model.
    """
    def __init__(self, session):
        self.session = session

    def rollback(self):
        """
        Rollback the current session.
        """
        self.session.rollback()

    def commit(self):
        """
        Commit changes to the database.
        """
        self.session.commit()

    def create_category(self, category_name: str, description: str) -> Category:
        """
        Creates a new category with the given name and description.
        Args:
            category_name (String): The name of the new category.
            description (String): The description of the new category.

        Returns:
            Category : The new category.
        """
        category = Category(
            category_name=category_name,
            description=description
        )
        self.session.add(category)
        print(f"[cat_repo.create_cat]: Created category [{category.category_name}]")
        return category

    def delete_category(self, category: Category):
        """
        Delete a category from the database.

        Args:
            category (Category): The category instance to delete.

        Returns:
            None
        """
        self.session.delete(category)
        print(f"[cat_repo.delete_cat]: Deleted category [{category.id}; {category.category_name}]")

    def modify_category(self, category: Category, name: str, description: str):
        """
        Modify a category from the database.

        Args:
            category (Category): The category instance to modify.
            name (String): The new name of the category.
            description (String): The new description of the category.

        Returns:
            None
        """
        if name is not None:
            category.category_name = name
        if description is not None:
            category.description = description
        print(f"[cat_repo.modify_cat]: Updated category [{category.id}; {category.category_name}]")

    def get_category_by_id(self, category_id) -> Category | None:
        """
        Get a category from the database using ID

        Args:
            category_id (int): The ID of the category.

        Returns:
            Category : The category.
            None: The category was not found.
        """
        # This returns exactly 1 query searched by ID
        query = self.session.query(Category).filter_by(id=category_id).first()
        return query

    def get_category_by_name(self, name: str) -> List[Category] | []:
        """
        Get a category from the database using category name

        Args:
            name (String): The name of the category.

        Returns:
            List[Category] : List of matching categories with name as substring
            [] : Empty list if there are no matching categories.
        """
        # This returns a list of categories with exact match
        # query = self.session.query(Category).filter_by(category_name=name).all()
        # This returns a list of categories whose names contain name as substring
        query = self.session.query(Category).filter_by(Category.category_name.ilike(f"%{name}%")).all()
        print(f"[cat_repo.get_cat]: Retrieved categories with substring [{name}]")
        return query

    def get_all_categories(self) -> List[Category] | []:
        """
        Get all categories from the database.

        Returns:
            List[Category] : List of all categories
        """
        query = self.session.query(Category).all()
        print(f"[cat_repo.get_all_cat]: Retrieved all categories")
        return query