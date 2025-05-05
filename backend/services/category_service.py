import sqlite3
from sqlalchemy.exc import IntegrityError

from typing import Dict, List

from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository
from backend.utils.error_utils import handle_errors

class CategoryService:
    def __init__(self, session):
        self.repo = CategoryRepository(session)

    def create_category(self, category_name: str, description: str) -> Category | None:
        validation_errors = validate_category(category_name, description)
        if validation_errors:
            handle_errors(validation_errors, "cat_serv.create_category")
            return None
        try:
            print(f"cat_serv.create_category: Running creation of category [{category_name}]")
            # Category names should be case-insensitive
            lc_category_name = category_name.lower()
            new_category = self.repo.create_category(lc_category_name, description)
            self.repo.commit() # Commit the changes
            return new_category
        except (IntegrityError, sqlite3.IntegrityError) as e:
            print(f"[cat_serv.create_category]: Category created failed due to IntegrityError: {e}")
            self.repo.rollback() # Rollback changes to refresh session
            return None
        except Exception as e:
            print(f"[cat_serv.create_category]: Unknown error: {e}")
            return None

    def modify_category(self, category: Category, category_name: str, description: str) -> bool:
        try:
            print(f"cat_serv.mod_cat: Running modification of category [{category.category_name}]")
            self.repo.modify_category(category, category_name, description)
            self.repo.commit()  # Commit the changes
            return True
        except Exception as e:
            print(f"cat_serv.modify_cat: Category could not be modified: {e}")
            return False

    def delete_category(self, category: Category) -> bool:
        try:
            print(f"cat_serv.del_cat: Running deletion of category [{category.category_name}]")
            self.repo.delete_category(category)
            self.repo.commit()  # Commit the changes
            return True
        except Exception as e:
            print(f"cat_serv.del_cat: Category could not be deleted: {e}")
            return False

    def get_category_by_id(self, category_id: int) -> Category | None:
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
        return (f"Category id: {category.id}, "
                f"Name: {category.category_name}, "
                f"Description: {category.description}")

def validate_category(category_name: str, description: str) -> Dict[str, str]:
    errors = {}
    # Category name cannot be empty
    if category_name is None or category_name == "":
        errors["category_name"] = "Category name is empty"
    # Add further validation checks here
    return errors
