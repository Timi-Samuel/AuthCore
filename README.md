# AuthCore
A simple authentication system built with Python and Flask, featuring user registration, email verification, password encryption, and password reset. This project demonstrates secure handling of credentials using encrypted storage, modular code structure, and clean code practices.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [User Flow](#user-flow)
- [Code Formatting](#code-formatting)
- [Acknowledgements](#acknowledgements)
- [Disclaimer](#disclaimer)

---

## Features
- User registration with email and password
- Email verification system using verification codes
- Password reset functionality via verification code
- Password encryption using symmetric encryption (Fernet) and secure hashing (bcrypt or bcrypt_sha256)
- Modular and maintainable code structure
- SQLite database for local development
- CLI frontend for quick testing and interaction

---

## Project Structure
AuthCore/

├── crypto_utils.py           # Utility functions for encryption and decryption  
├── encrypt_password.py       # Script for encrypting passwords  
├── interface.py              # Tkinter GUI frontend for interacting with the app  
├── main.py                   # Main Flask application  
├── model.py                  # Database models, ORM setup, and DB operations  
├── emailer.py                # Handles sending verification and reset emails  
├── user_service.py           # Core user logic (registration, authentication, password reset)  
├── utiltools.py              # Miscellaneous utility functions  
├── practice_emails.py        # Test email addresses for development  
├── secret.key                # Encryption key (not pushed to GitHub)  
├── requirements.txt          # Python dependencies  
├── .gitignore                # Files ignored by Git  
└── README.md                 # Project documentation  

---

## Getting Started
### Prerequisites
- Python 3.12 or higher  
- pip installed  
- Flask  
- SQLAlchemy  
- passlib  
- cryptography
- tkinter  

---

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Timi-Samuel/AuthCore.git
```

2. Navigate into the project folder
```bash
cd AuthCore
```

3. Create a virtual environment and activate it:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a .env file in the root directory with your sensitive credentials (email, app passwords, etc.).

### Usage
1. Start the Flask app:
```bash
python main.py
```


2. Launch the Tkinter GUI
```bash
python interface.py
```
* A window will appear with input fields for `email`, `password`, and buttons for `Register`, `Login`, and `Forgot Password`.
* Follow prompts in the GUI for verification and password reset.

### User Registration and Verification Flow
1. Register a new user through the GUI:
* Enter your email and password
* A verification code is sent to your email
* Enter the verification code in the GUI to complete registration

2. Log in with registered credentials.

3. Reset password if forgotten:
* Click *Forgot Password*
* Receive a verification code via email
* Enter the code and new password in the GUI to reset

### Code Formatting
* Code formatted with the autopep8 extension in VS Code
* Variable renaming and readability improvements assisted by ChatGPT

### Acknowledgements
* Flask and SQLAlchemy for backend and database
* Passlib for secure password hashing
* Tkinter for GUI development

### Disclaimer
* Sensitive data such as `.env` variables and `secret.key` are excluded from GitHub for security purposes.
* Do *not* store real credentials in the repository; always use environment variables or secure vaults for production.
