import requests
import re
from passlib.hash import bcrypt

# Base URL for the backend API
base_url = 'http://127.0.0.1:5001/users'


class UserClient:
    # Initialize UserClient with email, password, and backend URL
    def __init__(self, user_email, user_password, url):
        self.url = url
        self.email = user_email
        self.password = user_password

    # Validate password strength using regex
    def is_password_strong(self, password):
        pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
        return bool(re.match(pattern, password))

    # Send POST request to add a new user to the backend
    def register_user(self, code):
        url = self.url + '/add'
        response = requests.post(
            url, json={'email': self.email, 'password': self.password, 'code': code})
        if response.status_code == 201:
            return "Account created successfully"
        # Return backend error message if creation failed
        return response.json()["message"]

    # Send POST request to verify existing user login
    def login_user(self):
        url = self.url + '/validate'
        response = requests.post(
            url, json={'email': self.email, 'password': self.password})
        if response.status_code == 200:
            return "Account validated successfully"
        # Return backend error message if verification failed
        return response.json()["message"]

    # Send POST request to initiate verification process (email code)
    def send_verification_code(self):
        url = self.url + '/verify_account'
        response = requests.post(
            url, json={'email': self.email, 'password': self.password})
        if response.status_code == 200:
            code = response.json()['message']
            return code
        # Return backend message if verification initiation fails
        else:
            return response.json()['message']

    # Main logic to add user to database after verification
    def register_with_verification(self):
        if self.is_password_strong(self.password):
            verification_sent = self.send_verification_code()
            if verification_sent == 'User already exists':
                return 'User already exists'
            # Prompt user to enter the verification code received via email
            verification_code_input = input(
                "Enter verification code (sent to email you entered): ")
            if verification_sent:
                added = self.register_user(verification_code_input)
                if added == "Account created successfully":
                    return 'Verification Successful'
                else:
                    return f'Failed: {added}'
            else:
                return 'Account verification failed'
        else:
            # Password does not meet criteria
            return "Invalid password."

# Helper function to get email and password input from user


def prompt_credentials():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    return email, password

# ----------Interface----------#


def run_cli():
    # Dictionary of available options for the CLI menu
    menu_options = {
        "1": "Sign up",
        "2": "Login",
        "3": "Exit"
    }

    while True:
        print("Welcome to the application home. Choose an option:")
        # Display menu options
        for key, value in menu_options.items():
            print(f"{key}. {value}")

        choice = input("Enter choice here: ").strip()

        if choice == "1":
            # Sign up flow
            email, password = prompt_credentials()
            user_client = UserClient(email, password, base_url)
            print(user_client.register_with_verification(), "\n")
        elif choice == "2":
            # Login flow
            email, password = prompt_credentials()
            user_client = UserClient(email, password, base_url)
            print(user_client.login_user(), "\n")
        elif choice == "3":
            # Exit the program
            print("Bye!\n")
            break
        else:
            # Handle invalid input
            print("Invalid option. Please enter 1, 2, or 3.\n")


# Entry point for the script
if __name__ == "__main__":
    run_cli()
