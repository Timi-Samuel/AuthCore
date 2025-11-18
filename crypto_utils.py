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


class CryptoService:
    def __init__(self, key_path):
        self.key_path = key_path
        self.__fernet: bytes
        self.key = self.load_or_generate_key()
        self.__fernet = Fernet(self.key)

    def load_or_generate_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read()
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as f:
            f.write(key)
            return key

    def encrypt_text(self, plaintext):
        return self.__fernet.encrypt(plaintext.encode()).decode()

    def decrypt_text(self, ciphertext):
        return self.__fernet.decrypt(ciphertext.encode()).decode()
