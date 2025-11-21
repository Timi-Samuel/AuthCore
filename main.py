from model import session, User, VerificationCodesTable
from flask import Flask, jsonify, request
from passlib.hash import bcrypt
from crypto_utils import CryptoService
from dotenv import load_dotenv
from emailer import Emailer
from custom_exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidVerificationCodeError, PasswordIncorrectError
from utiltools import UtilTools

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


class UserService:
    # Initialize Server with user email and password
    def __init__(self, email, password, code=None):
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
        hashed_password = bcrypt.hash(self.password)
        user = User(email=self.email, hashed_password=hashed_password,
                    created_at=timestamp)
        session.add(user)
        session.delete(target)  # Remove verification code after use
        session.commit()
        return  # Created successfully

    # Verify a user's login credentials

    def authenticate_user(self):
        target = session.query(User).filter_by(email=self.email).first()
        if not target:
            # Unauthorized if user not found
            raise UserNotFoundError("User not found")

        # Check hashed password
        match = bcrypt.verify(self.password, target.hashed_password)
        if not match:
            # Unauthorized if password incorrect
            raise PasswordIncorrectError("Password is incorrect")
        return

# Flask route to initiate account verification (sends email)


@app.route('/users/verify_account', methods=['POST'])
def verify_account():
    data = request.json
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'message': 'Bad request'}), 400

    user_service = UserService(data['email'], data['password'])

    try:
        Emailer(user_service).send_verification_code_email()
        return jsonify({"message": "Success"}), 200

    except UserAlreadyExistsError:
        return jsonify({"message": "Conflict"}), 409

    except Exception as e:
        return jsonify({"message": f"Server error: {e}"}), 500

# Flask route to add a user to the database after verification


@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    if not data or not all(k in data for k in ('email', 'password', 'code')):
        return jsonify({'message': "Bad request"}), 400

    user_service = UserService(
        data['email'], data['password'], data['code'])
    try:
        user_service.register_user()
        return jsonify({'message': 'Resource created'}), 201

    except UserAlreadyExistsError:
        return jsonify({'message': 'Conflict'}), 409

    except InvalidVerificationCodeError:
        return jsonify({'message': 'Forbidden'}), 403

    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


# Flask route to validate login credentials


@app.route('/users/validate', methods=['POST'])
def authenticate_user():
    data = request.json
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({'message': "Bad request"}), 400

    user_service = UserService(data['email'], data['password'])
    try:
        user_service.authenticate_user()
        return jsonify({'message': 'Success'}), 200

    except UserNotFoundError:
        return jsonify({'message': 'Unauthorized'}), 401

    except PasswordIncorrectError:
        return jsonify({'message': 'Unauthorized'}), 401

    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
