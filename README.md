# AuthCore
A simple authentication system built with Python and Flask, featuring user registration, email verification, and password encryption. This project demonstrates secure handling of credentials using encrypted storage, modular code structure, and clean code practices.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Code Formatting](#code-formatting)
- [Acknowledgements](#acknowledgements)
- [Disclaimer](#disclaimer)

---

## Features
- User registration with email and password
- Email verification system
- Password encryption using symmetric encryption (Fernet)
- Modular code for easy maintenance
- SQLite database for local development

---

## Project Structure
AuthCore/
├── crypto_utils.py        # Utility functions for encryption and decryption
├── encrypt_password.py    # Script for encrypting passwords
├── frontend.py            # CLI-based frontend for interacting with the app
├── main.py                # Main Flask application
├── model.py               # Database models and ORM setup
├── practice_emails.py     # Test email addresses for development
├── secret.key             # Encryption key (not pushed to GitHub)
├── requirements.txt       # Python dependencies
├── .gitignore             # Files ignored by Git
└── README.md              # Project documentation

---

## Getting Started
### Prerequisites
- Python 3.12 or higher
- pip installed
- Flask
- SQLAlchemy
- cryptography

---

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Timi-Samuel/AuthCore.git
```

2. Navigate into the project folder:
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

---

## Usage
1. Start the Flask app:
```bash
python main.py
```

2. Interact with the app via the CLI (frontend.py) or by sending HTTP requests to the Flask endpoints.

---

### Interactive Example
#### Step 1: Register a New User (CLI)
```less
> python frontend.py
Enter your email: youremail@example.com
Enter your password: YourPassword123
Enter verification code (sent to email you entered): exampleverificationcode
Verification Successful.
```

---

## User Registration and Verification Flow
* Register a new user via CLI or /users/register endpoint
* A verification email is sent (requires valid email credentials)
* Complete verification to activate the account

---

## Code Formatting
* Code was formatted using the *`autopep8` extension in VS Code*
* Variable renaming and readability improvements were assisted with ChatGPT

---

## Disclaimer
Some sensitive data such as `.env` variables and `secret.key` are *excluded from GitHub* for security purposes (see .gitignore)
Do *not* store real credentials in the repository. Always use environment variables or secure vaults for production
