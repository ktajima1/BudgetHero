from backend.models.user import User
class AuthRepository():
    def __init__(self, session):
        self.session = session

    def create_user(self, username, hashed_password):
        user = User(username=username, password_hash=hashed_password)
        self.session.add(user)
        self.session.commit()
        return user

    def find_user(self, username):

        return self.session.query(User).filter_by(username=username).first()

    def delete_user(self, user):
        self.session.delete(user)
        self.session.commit()

    def change_password(self, user, new_hashed_password):
        user.password_hash = new_hashed_password
        self.session.commit()
