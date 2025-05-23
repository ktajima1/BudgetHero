from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository
from backend.utils.error_utils import handle_errors
import sqlite3
from sqlalchemy.exc import IntegrityError
from typing import Dict, List

class CategoryService:
    """
    Service file used to handle business logic for transaction categories
    """
    def __init__(self, session):
        self.repo = CategoryRepository(session)

    def create_category(self, category_name: str, description: str) -> Category | Dict[str,str] | None:
        """
        Creates a new category using the given name and description. Calls validate_category() to check category_name is unique. Category names are stored in lowercase.
        Args:
            category_name (str): The name of the category to create.
            description (str): The description of the category.
        Returns:
            Category: the created category.
            Dict[str,str]: A dictionary containing validation errors concerning category details
            None: Category could not be created
        """
        # Run validation check on category details
        validation_errors = validate_category(category_name, description)
        if validation_errors:
            handle_errors(validation_errors, "cat_serv.create_category")
            return validation_errors
        try:
            print(f"cat_serv.create_category: Running creation of category [{category_name}]")
            # Category names should be case-insensitive
            lc_category_name = category_name.lower()
            new_category = self.repo.create_category(lc_category_name, description)
            self.repo.commit() # Commit the changes
            print(f"[cat_serv.create_cat]: Created category [{new_category.id}; {new_category.category_name}]")
            return new_category
        except (IntegrityError, sqlite3.IntegrityError) as e:
            print(f"[cat_serv.create_category]: Category created failed due to IntegrityError: {e}")
            self.repo.rollback() # Rollback changes to refresh session
            return None
        except Exception as e:
            print(f"[cat_serv.create_category]: Unknown error: {e}")
            return None

    def modify_category(self, category: Category, category_name: str, description: str) -> bool | Dict[str, str]:
        """
        Modified an existing category using the provided details. Checks that the new category is valid before modification.
        Args:
            category (Category): The new category to modify.
            category_name (str): The new category name.
            description (str): The new category description.
        Returns:
            True (bool): Category was modified successfully
            False (bool): Category was not modified successfully
            Dict[str, str]: A dictionary containing validation errors concerning category details
        """
        validation_errors = validate_category(category_name, description)
        if validation_errors:
            handle_errors(validation_errors, "cat_serv.mod_category")
            return validation_errors
        try:
            print(f"cat_serv.mod_cat: Running modification of category [{category.category_name}]")
            self.repo.modify_category(category, category_name, description)
            self.repo.commit()  # Commit the changes
            return True
        except Exception as e:
            print(f"cat_serv.modify_cat: Category could not be modified: {e}")
            return False

    def delete_category(self, category: Category) -> bool:
        """
        Deletes a category
        Args:
            category (Category): The category to delete.
        Returns:
            True (bool): Category was deleted successfully
            False (bool): Category was not deleted successfully
        """
        try:
            print(f"cat_serv.del_cat: Running deletion of category [{category.category_name}]")
            self.repo.delete_category(category)
            self.repo.commit()  # Commit the changes
            return True
        except Exception as e:
            print(f"cat_serv.del_cat: Category could not be deleted: {e}")
            return False

    def get_category_by_id(self, category_id: int) -> Category | None:
        """
        Gets category by id.
        Args:
            category_id (int): The id of the category to get.
        Returns:
            Category: The target category
            None: Category could not be found
        """
        try:
            category = self.repo.get_category_by_id(category_id)
            if category is not None:
                print(f"cat_serv.get_cat_by_id: Category [{category.category_name}] matching [{category_id}] acquired")
                return category
            else:
                print(f"cat_serv.get_cat_by_id: No matching transactions acquired")
                return None
        except Exception as e:
            print(f"cat_serv.get_cat_by_id: something went wrong: {e}")
            return None

    def get_category_by_name(self, category_name: str) -> List[Category]:
        """
        Gets category by name.
        Args:
            category_name (str): The name of the category to get.
        Returns:
            List[Category]: The list of categories that contain the category name as a substring
        """
        try:
            category_list = self.repo.get_category_by_name(category_name)
            if category_list:
                print(f"cat_serv.get_cat_by_name: Categories containing [{category_name}] acquired")
                return category_list
            else:
                print(f"cat_serv.get_cat_by_name: No matching transactions acquired")
                return []
        except Exception as e:
            print(f"cat_serv.get_cat_by_name: something went wrong: {e}")
            return []

    def get_all_categories(self) -> List[Category]:
        """
        Gets all categories.
        Returns:
            List[Category]: The list of all categories.
        """
        try:
            category_list = self.repo.get_all_categories()
            if category_list:
                print(f"cat_serv.get_all_cats: All categories acquired")
                return category_list
            else:
                print(f"cat_serv.get_all_cats: No categories exist")
                return []
        except Exception as e:
            print(f"trans_serv.get_all_cats: something went wrong: {e}")
            return []

    def get_details(self, category: Category) -> str:
        """
        Gets details about a category.
        Args:
            category (Category): The category to get details for.
        Returns:
            str: The details of the category.
        """
        return (f"Category id: {category.id}, "
                f"Name: {category.category_name}, "
                f"Description: {category.description}")

def validate_category(category_name: str, description: str) -> Dict[str, str]:
    """
    Validates details of a category. Category names cannot be empty
    Args:
        category_name (str): The name of the category to validate.
        description (str): The description of the category.
    Returns:
        Dict[str, str]: Any requirement violations concerning category details.
        {}: If the category is valid.
    """
    errors = {}
    # Category name cannot be empty
    if category_name is None or category_name == "":
        errors["category_name"] = "Category name is empty"
    # Add further validation checks here
    return errors
