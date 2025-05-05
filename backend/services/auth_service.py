import sqlite3
from sqlalchemy.exc import IntegrityError
from backend.repositories.auth_repository import AuthRepository
from backend.errors import InvalidPasswordError

import re

from backend.utils.error_utils import handle_errors


class AuthService:
    def __init__(self, session):
        self.repo = AuthRepository(session)

    # returns user on success, None on failure
    def register_user(self, username, password):
        # Check that username fits requirements. Uniqueness is checked when adding user to database via catching DuplicateUsernameError
        username_errors = validate_username(username)
        # Check that password fits requirements
        password_errors = validate_password(password)

        if username_errors:
            handle_errors(username_errors, "auth_serv.register_user")
            return None  # Code should display message on frontend for what errors exist with the username

        if password_errors:
            handle_errors(password_errors, "auth_serv.register_user")
            return None  # Code should display message on frontend for what errors exist with the password

        hashed_password = hash_password(password)  # Hash the password to store in database
        print("preparing to create user")
        try:
            new_user = self.repo.create_user(username, hashed_password)
            print(f"created user: {username}")
            return new_user
        except (IntegrityError, sqlite3.IntegrityError):
            print("user already exists")
            return None

    # returns user on success, None on failure
    def login_user(self, username, password):
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

    # returns boolean
    def change_password(self, username, new_password):
        try:
            password_errors = validate_password(new_password)
            if password_errors:
                handle_errors(password_errors, "auth_serv.change_password")
                print("CHANGE PASSWORD FAILED:")
                return False

            user = self.repo.find_user(username)
            new_hashed_password = hash_password(new_password)
            self.repo.change_password(user, new_hashed_password)
            print("CHANGE PASSWORD SUCCESSFUL")
            return True
        except Exception as e:
            print(f"changing password error: {e}")
            return False

    # returns boolean
    def delete_user(self, username, password):
        try:
            user = self.repo.find_user(username)
            if user is None:
                print("DELETION FAILED: user does not exist")
                return False
            else:
                hashed_password = hash_password(password)
                if user.password_hash == hashed_password:
                    self.repo.delete_user(user)
                    print("deleted user")
                    return True
                else:
                    print("DELETE FAILED: password does not match")
                    return False
        except Exception as e:
            print(f"deletion error: {e}")
            return False

# Look up hashing algorithm for passwords
def hash_password(password):
    return password + "hashed"

# Username requirements:
#   - Must be 4 or more characters long
def validate_username(username):
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
def validate_password(password):
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

