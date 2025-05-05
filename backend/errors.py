# Usernames must be unique
class DuplicateUsernameError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

class InvalidPasswordError(Exception):
    def __init__(self, message, field):
        super().__init__(message)
        self.field = field