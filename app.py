from backend.database import initialize_database, get_session
from backend.services.user_service import AuthService
from backend.services.transaction_service import TransactionService
from backend.services.category_service import CategoryService
from datetime import datetime
from backend.utils.enums import IncomeOrExpense

if __name__ == "__main__":
    initialize_database()
    with get_session() as session:
        auth_service = AuthService(session)
        transaction_service = TransactionService(session)
        category_service = CategoryService(session)

        # status1 = auth_service.delete_user("admin", "12345L@w")
        # status2 = auth_service.delete_user("admin", "10936S@n")
        # user1 = auth_service.register_user("admin", "10936S@n")
        # user2 = auth_service.login_user("admin", "10936S@n")
        # user3 = auth_service.login_user("admin", "12345L@w")
        # status3 = auth_service.change_password("admin", "12345L@w")
        user5 = auth_service.login_user("admin", "10936S@n")
        # user5 = auth_service.login_user("mod", "12345L@w")

        # cat0 = category_service.create_category("meow", "cat")
        # cat1 = category_service.create_category("woof", "dog")
        # cat2 = category_service.create_category("quack", "duck")
        # cat3 = category_service.create_category("ribbit", "frog")
        # print("Completed creation of all cats\n")
        # cats = category_service.get_all_categories()
        # for cat in cats:
        #     print(category_service.get_details(cat))
        #     category_service.delete_category(cat)
        # print("Deleted all cats")

        # Syntax: datetime(year, month, day, hour=0, minute=0, second=0)
        dt = datetime(2024, 12, 25, 14, 30, 0)  # Dec 25, 2024 at 2:30 PM
        # user, amount, type, date, category_id, description

        transaction_service.create_transaction(user5, 100, "inCOME", dt, 1, "meow")
        transaction_service.create_transaction(user5, 200, "income", dt, 2, "woof")
        transaction_service.create_transaction(user5, 125.5, "expense", dt, 5, "tomato")

        tlist = transaction_service.get_all_transactions(user5)
        for transaction in tlist:
            print(f"\t {transaction_service.get_details(transaction)}")
        print("t2list:")
        filters = {
            "id" : None,
            "type_enum": IncomeOrExpense.INCOME,
            "category": None,
            "min_amount": None,
            "max_amount": None,
            "description" : []
        }
        t2list = transaction_service.get_transactions(user5, filters)
        for transaction in t2list:
            print(f"\t {transaction_service.get_details(transaction)}")

        del_list = transaction_service.get_all_transactions(user5)
        print("Starting deletion of all transactions:")
        for transaction in del_list:
            transaction_service.delete_transaction(transaction)
            print(f"\tDeleted transaction: {transaction_service.get_details(transaction)}")
        print("Finished and deleted all transactions")
        t3list = transaction_service.get_all_transactions(user5)
        for transaction in t3list:
            print(f"\t {transaction_service.get_details(transaction)}")
