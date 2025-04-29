from sqlite3 import IntegrityError
from backend.models.user import User
from backend.database import get_session
from backend.services.auth import validate_username, validate_password, hash_password
'''
# Improvements: could use decorations for try and with blocks since a lot of the code is similar for these methods
'''

def create_user(username, password):
    try:
        # Check that username fits requirements. Uniqueness is checked when adding user to database via catching DuplicateUsernameError
        username_errors = validate_username(username)
        # Check that password fits requirements
        password_errors = validate_password(password)

        if username_errors:
            print("username error")
            pass # Code should display message on frontend for what errors exist with the username

        if password_errors:
            for error in password_errors:
                print(f"password error: {error}")
            pass # Code should display message on frontend for what errors exist with the password

        hashed_password = hash_password(password) # Hash the password to store in database
        print("preparing to create user")
        with get_session() as session:
            session.add(User(username=username, password_hash=hashed_password))
            session.commit()
            print("user created")
    except IntegrityError as e: # If username already exists, then database will throw IntegrityError
        print(f"Username already exists, please try another username: {e}")
    except Exception as e: # Fallback
        print(f"Creating user failed: {e}")

def login_user(username, password):
    try:
        with get_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                print("User not found")
            else:
                hashed_password = hash_password(password)
                if user.password_hash == hashed_password:
                    print("Login successful")
                    return user
                else:
                    print("Login failed")
                    return None
    except Exception as e:
        print(f"Could not complete login: {e}")

def delete_user(username, password):
    try:
        with get_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                print("User not found")
            else:
                hashed_password = hash_password(password)
                if hashed_password == user.password_hash:
                    session.delete(user)
                    session.commit()
                    print("user deleted")
                else:
                    print("password did not match, user deletion cancelled")
    except Exception as e:
        print(f"Could not complete user deletion: {e}")

def change_password(username, new_password):
    try:
        with get_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                print("User not found")
            else:
                new_hashed_password = hash_password(new_password)
                user.password_hash = new_hashed_password
                session.commit()
                print("Password changed")
    except Exception as e:
        print(f"Could not change password: {e}")

'''
Test version used in unit testing, modified to accept a session instead of calling get_session
'''
def _create_user(session, username, password):
    try:
        # Check that username fits requirements. Uniqueness is checked when adding user to database via catching DuplicateUsernameError
        username_errors = validate_username(username)
        # Check that password fits requirements
        password_errors = validate_password(password)

        if username_errors:
            print("username error")
            pass # Code should display message on frontend for what errors exist with the username

        if password_errors:
            for error in password_errors:
                print(f"password error: {error}")
            pass # Code should display message on frontend for what errors exist with the password

        hashed_password = hash_password(password) # Hash the password to store in database
        print("preparing to create user")
        session.add(User(username=username, password_hash=hashed_password))
        session.commit()
        print("user created")
    except IntegrityError as e: # If username already exists, then database will throw IntegrityError
        print(f"Username already exists, please try another username: {e}")
    except Exception as e: # Fallback
        print(f"Creating user failed: {e}")

def _login_user(session, username, password):
    try:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            print("User not found")
        else:
            hashed_password = hash_password(password)
            if user.password_hash == hashed_password:
                print("Login successful")
                return user
            else:
                print("Login failed")
                return None
    except Exception as e:
        print(f"Could not complete login: {e}")

def _delete_user(session, username, password):
    try:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            print("User not found")
        else:
            hashed_password = hash_password(password)
            if hashed_password == user.password_hash:
                session.delete(user)
                session.commit()
                print("user deleted")
            else:
                print("password did not match, user deletion cancelled")
    except Exception as e:
        print(f"Could not complete user deletion: {e}")

def _change_password(session, username, new_password):
    try:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            print("User not found")
        else:
            new_hashed_password = hash_password(new_password)
            user.password_hash = new_hashed_password
            session.commit()
            print("Password changed")
    except Exception as e:
        print(f"Could not change password: {e}")