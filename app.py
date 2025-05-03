from backend.database import initialize_database, get_session
from backend.models.user import User
from backend.services.auth_service import AuthService


if __name__ == "__main__":
    initialize_database()
    with get_session() as session:
        auth_service = AuthService(session)

        auth_service.delete_user("admin", "12345L@w")
        auth_service.delete_user("admin", "10936S@n")
        auth_service.register_user("admin", "10936S@n")
        auth_service.login_user("admin", "10936S@n")
        auth_service.login_user("admin", "12345L@w")
        auth_service.change_password("admin", "12345L@w")
        auth_service.login_user("admin", "10936S@n")
        auth_service.login_user("admin", "12345L@w")

    # print("Database tables created")