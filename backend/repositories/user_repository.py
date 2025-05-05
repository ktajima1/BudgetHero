from backend.models.user import User

class AuthRepository():
    def __init__(self, session):
        self.session = session

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def create_user(self, username: str, hashed_password: str) -> User:
        user = User(username=username, password_hash=hashed_password)
        self.session.add(user)
        return user

    def find_user(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).first()

    def delete_user(self, user: User):
        self.session.delete(user)

    def change_password(self, user: User, new_hashed_password: str):
        user.password_hash = new_hashed_password
