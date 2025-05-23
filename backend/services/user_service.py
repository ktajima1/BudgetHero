from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.utils.enums import IncomeOrExpense, IncrementOrDecrement
from backend.utils.error_utils import handle_errors
import sqlite3
from sqlalchemy.exc import IntegrityError
from typing import Dict
import re

class UserService:
    def __init__(self, session):
        self.repo = UserRepository(session)

    # returns user on success, None on failure
    def register_user(self, username: str, password: str) -> User | Dict[str,str] | None:
        # Check that username fits requirements. Uniqueness is checked when adding user to database via catching DuplicateUsernameError
        username_errors = validate_username(username)
        # Check that password fits requirements
        password_errors = validate_password(password)

        if username_errors:
            handle_errors(username_errors, "auth_serv.register_user")
            return username_errors

        if password_errors:
            handle_errors(password_errors, "auth_serv.register_user")
            return password_errors

        hashed_password = hash_password(password)  # Hash the password to store in database
        print("preparing to create user")
        try:
            new_user = self.repo.create_user(username, hashed_password)
            self.repo.commit()
            print(f"created user: {username}")
            return new_user
        except (IntegrityError, sqlite3.IntegrityError):
            print("user already exists")
            self.repo.rollback()
            return None

    # returns user on success, None on failure
    def login_user(self, username: str, password: str) -> User | None:
        try:
            print(f"logging in as: {username}")
            user = self.repo.find_user(username)
            if user and user.password_hash == hash_password(password):
                print(f"logged in as: {username}")
                return user
            else:
                print(f"login failed for: {username}")
                return None
        except Exception as e:
            print(f"login error: {e}")
            return None

    def get_current_balance(self, user: User) -> float | None:
        try:
            balance = self.repo.get_current_balance(user)
            print(f"current balance: {balance}")
            return balance
        except Exception as e:
            print(f"get balance error: {e}")
            return None

    def update_balance(self, user: User, amount: float, update_type: IncrementOrDecrement) -> float:
        new_balance = current_balance = self.repo.get_current_balance(user)
        try:
            if update_type == IncrementOrDecrement.INCREMENT:
                new_balance = current_balance + amount
            elif update_type == IncrementOrDecrement.DECREMENT:
                new_balance = current_balance - amount
            else:
                raise Exception(f"[user_serv.update_bal]: Error, unknown type {update_type}")
            # print(f"[user_serv.update_balance]: Updating balance by: {amount}")
            self.repo.change_balance(user, new_balance)
            self.repo.commit()
            return new_balance
        except Exception as e:
            print(f"change balance error: {e}")
            return current_balance

    # returns boolean
    def change_password(self, username: str, new_password: str) -> bool | Dict[str,str]:
        try:
            password_errors = validate_password(new_password)
            if password_errors:
                handle_errors(password_errors, "auth_serv.change_password")
                print("CHANGE PASSWORD FAILED:")
                return password_errors

            user = self.repo.find_user(username)
            new_hashed_password = hash_password(new_password)
            self.repo.change_password(user, new_hashed_password)
            self.repo.commit()
            print("CHANGE PASSWORD SUCCESSFUL")
            return True
        except Exception as e:
            print(f"changing password error: {e}")
            return False

    # returns boolean
    def delete_user(self, username: str, password: str) -> bool:
        try:
            user = self.repo.find_user(username)
            if user is None:
                print("DELETION FAILED: user does not exist")
                return False
            else:
                hashed_password = hash_password(password)
                if user.password_hash == hashed_password:
                    self.repo.delete_user(user)
                    self.repo.commit()
                    print("deleted user")
                    return True
                else:
                    print("DELETE FAILED: password does not match")
                    return False
        except Exception as e:
            print(f"deletion error: {e}")
            return False

    def check_if_user_exists(self, username: str) -> bool:
        try:
            user = self.repo.find_user(username)
            if user is not None:
                return True
            else:
                return False
        except Exception as e:
            print(f"get user error: {e}")
            return False

# Look up hashing algorithm for passwords
def hash_password(password: str) -> str:
    return password + "hashed"

# Username requirements:
#   - Must be 4 or more characters long
def validate_username(username: str) -> Dict[str,str]:
    errors = {}
    if len(username) < 4:
        errors["length"] = "Username must be at least 4 characters long"
    return errors if errors else None

# Requirements:
# - 1 capital letter
# - 1 lowercase letter
# - 1 number
# - 1 symbol
# - 8 or more characters
def validate_password(password: str) -> Dict[str,str]:
    errors = {}
    if len(password) < 8:
        errors["length"] = "Password must be at least 8 characters long"
    # Check for at least 1 capital letter
    if not re.search(r'[A-Z]', password):
        errors["capital"] = "Password must contain at least 1 capital letter"
    # Check for at least 1 lowercase letter
    if not re.search(r'[a-z]', password):
        errors["lowercase"] = "Password must contain at least 1 lowercase letter"
    # Check for at least 1 number
    if not re.search(r'[0-9]', password):
        errors["number"] = "Password must contain at least 1 number"
    # Check for at least 1 symbol (adjust the symbol characters as needed)
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors["symbol"] = "Password must contain at least 1 symbol"
    return errors if errors else None

