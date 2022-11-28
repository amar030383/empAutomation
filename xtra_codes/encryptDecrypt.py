import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SECRET_KEY = b"message"  # Password Encode Secret Key Before Password Encrypt
SALT = b"sAlT"*8

def get_fenec():
    kdf = PBKDF2HMAC( algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(SECRET_KEY))
    return Fernet(key)

def encrypt_password(password):
    f = get_fenec()
    token = f.encrypt(bytes(password, encoding='utf-8'))
    return token.decode()

def decrypt_password(tek):
    f = get_fenec()
    return f.decrypt(bytes(tek, encoding='utf-8')).decode()

password = "x7zBCHki"
tek = encrypt_password(password)
print (tek)

dteck = decrypt_password(tek)
print (dteck)