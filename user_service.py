from passlib.hash import bcrypt_sha256
from crypto_utils import CryptoService
from model import session, User, VerificationCodesTable, VerificationLogs, DBOperations
from utiltools import UtilTools
from custom_exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidVerificationCodeError, PasswordIncorrectError


class UserService:
    # Initialize Server with user email and password
    def __init__(self, email, password=None, code=None):
        self.email = email
        self.password = password
        self.code = code
        self.crypto_service = CryptoService('secret.key')

    # Check if a user already exists in the database
    def user_exists(self):
        target = session.query(User).filter_by(email=self.email).first()
        if target:
            return True
        return False

    # Add user to database after verifying code

    def register_user(self):
        if self.user_exists():
            # Conflict if user already exists
            raise UserAlreadyExistsError("User already exists.")

        # Find verification code in database
        target = session.query(VerificationCodesTable).filter_by(
            email=self.email, code=self.code).first()
        timestamp = UtilTools.current_time()
        if not target:
            raise InvalidVerificationCodeError("Invalid verification code.")
        # Hash the user's password before storing
        hashed_password = bcrypt_sha256.hash(self.password)
        user = User(email=self.email, hashed_password=hashed_password,
                    created_at=timestamp)
        session.add(user)
        session.delete(target)  # Remove verification code after use
        session.commit()
        return  # Created successfully

    def update_password(self):
        user = session.query(User).filter_by(email=self.email).first()
        if not user:
            raise UserNotFoundError("User not found")
        target = session.query(VerificationCodesTable).filter_by(
            email=self.email, code=self.code).first()
        if not target:
            raise InvalidVerificationCodeError("Invalid verification code.")
        user.hashed_password = bcrypt_sha256.hash(self.password)
        print(user.hashed_password)
        session.delete(target)  # Remove verification code after use
        session.commit()
        return

    # Verify a user's login credentials

    def authenticate_user(self):
        target = session.query(User).filter_by(email=self.email).first()
        if not target:
            # Unauthorized if user not found
            raise UserNotFoundError("User not found")

        # Check hashed password
        match = bcrypt_sha256.verify(self.password, target.hashed_password)
        if not match:
            # Unauthorized if password incorrect
            raise PasswordIncorrectError("Password is incorrect")
        return

    # Remove the code from db once account has been verified
    def remove_verification_code(self):
        db = DBOperations(self.email, self.password)
        db.remove_verification_code()
        return
