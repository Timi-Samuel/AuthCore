class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidVerificationCodeError(Exception):
    pass


class PasswordIncorrectError(Exception):
    pass
