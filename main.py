from model import session, User, VerificationCodes
from flask import Flask, jsonify, request
from passlib.hash import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import datetime
from crypto_utils import decrypt_text
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


class UserService:
    # Initialize Server with user email and password
    def __init__(self, email, password):
        self.email = email
        self.password = password

    # Get current timestamp
    def current_time(self):
        return datetime.datetime.now()

    # Check if a user already exists in the database
    def user_exists(self):
        target = session.query(User).filter_by(email=self.email).first()
        if target:
            return True
        return False

    # Retrieve email and app password from environment variables, decrypt them
    def get_sender_credentials(self):
        email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        email = decrypt_text(email).strip()
        password = decrypt_text(password).strip()
        return email, password

    # Send verification email to user with a randomly generated code
    def send_verification_code_email(self):
        sender_email, app_password = self.get_sender_credentials()  # Get sender credentials

        # Compose email content
        subject = "Test email"
        verification_number = str(random.randint(
            10000, 99999))  # Generate 5-digit code
        body = f"Use the following verification code to verify your email: {verification_number}"

        # Create email message object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = self.email
        message['Subject'] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            # Connect to Gmail SMTP server and send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(sender_email, app_password)
                server.send_message(message)
                server.quit()

            # Record verification attempt in database
            timestamp = self.current_time()
            user_verifcation_attempt = VerificationCodes(
                email=self.email, password=self.password, code=verification_number, timestamp=timestamp)
            session.add(user_verifcation_attempt)
            session.commit()
            return jsonify({"message": "Success"}), 200
        except Exception as e:
            # Handle email sending errors
            return jsonify({"message": f"Server error: {e}"}), 500

    # Add user to database after verifying code
    def register_user(self, code):
        if self.user_exists():
            return 409  # Conflict if user already exists

        # Find verification code in database
        target = session.query(VerificationCodes).filter_by(
            email=self.email, code=code).first()
        timestamp = self.current_time()
        if target:
            # Hash the user's password before storing
            hashed_password = bcrypt.hash(self.password)
            user = User(email=self.email, password=hashed_password,
                        timestamp=timestamp)
            session.add(user)
            session.delete(target)  # Remove verification code after use
            session.commit()
            return 201  # Created successfully
        else:
            return 403  # Forbidden if code invalid

    # Verify a user's login credentials
    def authenticate_user(self):
        target = session.query(User).filter_by(email=self.email).first()
        if not target:
            return 401  # Unauthorized if user not found

        # Check hashed password
        match = bcrypt.verify(self.password, target.hashed_password)
        if match:
            return 200  # Success
        return 401  # Unauthorized if password incorrect

# Flask route to initiate account verification (sends email)


@app.route('/users/verify_account', methods=['POST'])
def verify_account():
    data = request.json
    if data.get("email") and data.get("password"):
        email = data.get("email")
        password = data.get("password")
        user_service = UserService(email, password)
        if user_service.user_exists():
            return jsonify({"message": "Conflict"}), 409
        user_service.send_verification_code_email()
        return jsonify({"message": "Success"}), 200
    else:
        return jsonify({'message': 'Bad request'}), 400

# Flask route to add a user to the database after verification


@app.route('/users/add', methods=['POST'])
def add_user():
    data = request.json
    if data.get("email") and data.get("password") and data.get("code"):
        email = data.get("email")
        password = data.get("password")
        user_service = UserService(email, password)
        code = data.get('code')
        status_code = user_service.register_user(code)
        if status_code == 201:
            return jsonify({'message': 'Resource created'}), 201
        elif status_code == 409:
            return jsonify({'message': 'Conflict'}), 409
        else:
            return jsonify({'message': 'Forbidden'}), 403
    return jsonify({'message': "Bad request"}), 400

# Flask route to validate login credentials


@app.route('/users/validate', methods=['POST'])
def verify_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email and password:
        user_service = UserService(email, password)
        status_code = user_service.authenticate_user()
        if status_code == 200:
            return jsonify({'message': 'Success'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    else:
        return jsonify({'message': 'Bad request'}), 400


# Run the Flask application
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
