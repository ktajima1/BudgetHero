from backend.errors import InvalidPasswordError
import re

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