import requests
import re

# Base URL for the backend API
base_url = 'http://127.0.0.1:5001/users'


class AuthService:
    def __init__(self, email, password, url):
        self.email = email
        self.password = password
        self.url = url

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

    def register_with_verification(self, verification_code):
        if self.is_password_strong(self.password):
            added = self.register_user(verification_code)
            if added == "Account created successfully":
                return 'Verification Successful'
            else:
                return f'Failed: {added}'
        else:
            # Password does not meet criteria
            return "Invalid password."


class Client:

    def handle_register(self):
        email, password = prompt_credentials()
        auth_service = AuthService(email, password, base_url)
        # auth_service.send_verification_code()
        verification_sent = auth_service.send_verification_code()
        if verification_sent == 'Conflict':
            return 'User already exists'
        elif verification_sent != 'Success':
            return f"Failed to send verification code: {verification_sent}"
        code = input("Enter verification code sent to your email: ")
        return auth_service.register_with_verification(code)

    def handle_login(self):
        email, password = prompt_credentials()
        auth_service = AuthService(email, password, base_url)
        return auth_service.login_user()

    def show_menu(self):

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
                print(self.handle_register(), "\n")
            elif choice == "2":
                # Login flow
                print(self.handle_login(), "\n")
            elif choice == "3":
                # Exit the program
                print("Bye!\n")
                break
            else:
                # Handle invalid input
                print("Invalid option. Please enter 1, 2, or 3.\n")

# Helper function to get email and password input from user


def prompt_credentials():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    return email, password

# ----------Interface----------#


def run_cli():
    client = Client()
    client.show_menu()


# Entry point for the script
if __name__ == "__main__":
    run_cli()
