from flask import Flask, jsonify, request
from dotenv import load_dotenv
from emailer import Emailer
from custom_exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidVerificationCodeError, PasswordIncorrectError
from user_service import UserService

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


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
def register_user():
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

# Flask route to request password change


@app.route('/users/forgot_password/', methods=['POST'])
def forgot_password():
    data = request.json
    if not data or not data['email']:
        return jsonify({'message': "Bad request"}), 400

    try:
        user_service = UserService(data['email'])
        Emailer(user_service).send_verification_code_email(
            "Password reset request", True)
        return jsonify({"message": "Success"}), 200

    except UserNotFoundError:
        return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"message": f"Server error: {e}"}), 500


@app.route('/users/change_password/', methods=["POST"])
def change_password():
    data = request.json
    if not data or not all(k in data for k in ('email', 'password', 'code')):
        return jsonify({'message': "Bad request"}), 400

    user_service = UserService(data['email'], data['password'], data['code'])

    try:
        user_service.update_password()
        return jsonify({'message': 'Password updated successfully'}), 200
    except UserNotFoundError:
        return jsonify({"message": "User not found"}), 404

    except InvalidVerificationCodeError:
        return jsonify({'message': 'Forbidden'}), 403

    except Exception as e:
        return jsonify({'message': f"Server error: {e}"}), 500


# Run the Flask application
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
