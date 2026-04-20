from cryptography.fernet import Fernet
import base64
import hashlib

def derive_key_from_master_password(master_password: str) -> bytes:
    """Master paroldan 32 byte kalit olish"""
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), b'salt_123', 100000)
    return base64.urlsafe_b64encode(key)

def encrypt_data(data: str, master_password: str) -> str:
    key = derive_key_from_master_password(master_password)
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str, master_password: str) -> str:
    key = derive_key_from_master_password(master_password)
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()