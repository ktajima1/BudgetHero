from backend.models.category import Category
from typing import List

class CategoryRepository():
    def __init__(self, session):
        self.session = session

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def create_category(self, category_name: str, description: str) -> Category:
        category = Category(
            category_name=category_name,
            description=description
        )
        self.session.add(category)
        print(f"[cat_repo.create_cat]: Created category [{category.id}; {category.category_name}]")
        return category

    def delete_category(self, category: Category):
        self.session.delete(category)
        print(f"[cat_repo.delete_cat]: Deleted category [{category.id}; {category.category_name}]")

    def modify_category(self, category: Category, name: str, description: str):
        if name is not None:
            category.category_name = name
        if description is not None:
            category.description = description
        print(f"[cat_repo.modify_cat]: Updated category [{category.id}; {category.category_name}]")

    def get_category_by_id(self, category_id) -> Category | None:
        # This returns exactly 1 query searched by ID
        query = self.session.query(Category).filter_by(id=category_id).first()
        return query

    def get_category_by_name(self, name: str) -> List[Category] | []:
        # This returns a list of categories with exact match
        # query = self.session.query(Category).filter_by(category_name=name).all()
        # This returns a list of categories whose names contain name as substring
        query = self.session.query(Category).filter_by(Category.category_name.ilike(f"%{name}%")).all()
        print(f"[cat_repo.get_cat]: Retrieved categories with substring [{name}]")
        return query

    def get_all_categories(self) -> List[Category] | []:
        query = self.session.query(Category).all()
        print(f"[cat_repo.get_all_cat]: Retrieved all categories")
        return query