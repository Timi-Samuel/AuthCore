import smtplib
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from crypto_utils import CryptoService
from custom_exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidVerificationCodeError, PasswordIncorrectError
from model import session, VerificationCodesTable
from utiltools import UtilTools


class Emailer:
    def __init__(self, user_service):
        self.user_service = user_service
        self.crypto_service = CryptoService("secret.key")

    # Retrieve email and app password from environment variables, decrypt them

    def get_sender_credentials(self):
        email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        email = self.crypto_service.decrypt_text(email).strip()
        password = self.crypto_service.decrypt_text(password).strip()
        return email, password

        # Send verification email to user with a randomly generated code
    def send_verification_code_email(self, subject):
        if self.user_service.user_exists():
            raise UserAlreadyExistsError("User already exists")

        sender_email, app_password = self.get_sender_credentials()  # Get sender credentials

        # Compose email content
        verification_number = str(random.randint(
            10000, 99999))  # Generate 5-digit code
        body = f"Use the following verification code to verify your email address: {verification_number}"

        # Create email message object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = self.user_service.email
        message['Subject'] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP server and send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(sender_email, app_password)
            server.send_message(message)
            server.quit()

        # Record verification attempt in database
        timestamp = UtilTools.current_time()
        user_verifcation_attempt = VerificationCodesTable(
            email=self.user_service.email, password=self.user_service.password, code=verification_number, created_at=timestamp)
        session.add(user_verifcation_attempt)
        session.commit()
        return
