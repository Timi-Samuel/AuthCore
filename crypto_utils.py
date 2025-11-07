# crypto_utils.py
import os
from cryptography.fernet import Fernet

def load_or_generate_key():
    key_path = "secret.key"
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    return key

key = load_or_generate_key()
fernet = Fernet(key)

def encrypt_text(plaintext: str) -> str:
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_text(ciphertext: str) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()


