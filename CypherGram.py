from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import hashlib

# Constants
SALT_SIZE = 16
KEY_SIZE = 32
IV_SIZE = 16
ITERATIONS = 100_000

def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)

def pad(text):
    padding = AES.block_size - len(text.encode()) % AES.block_size
    return text + chr(padding) * padding

def unpad(text):
    return text[:-ord(text[-1])]

def encrypt(plaintext, password):
    if len(password) < 10:
        raise ValueError("❌ Password must be at least 10 characters")

    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password.encode(), salt)
    iv = get_random_bytes(IV_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plaintext)
    encrypted = cipher.encrypt(padded_text.encode())

    result = base64.b64encode(salt + iv + encrypted).decode()
    return result

def decrypt(encrypted_b64, password):
    raw = base64.b64decode(encrypted_b64)
    salt = raw[:SALT_SIZE]
    iv = raw[SALT_SIZE:SALT_SIZE + IV_SIZE]
    encrypted = raw[SALT_SIZE + IV_SIZE:]

    key = derive_key(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    return unpad(decrypted.decode())

# Example usage:
if __name__ == "__main__":
    mode = input("Encrypt or Decrypt? (e/d): ").lower()
    password = input("🔑 Enter password (min 10 chars): ")
    
    if mode == 'e':
        text = input("📝 Enter text to encrypt: ")
        encrypted = encrypt(text, password)
        print(f"\n🔐 Encrypted:\n{encrypted}")
    elif mode == 'd':
        encrypted = input("🔐 Enter encrypted text: ")
        try:
            decrypted = decrypt(encrypted, password)
            print(f"\n🧾 Decrypted:\n{decrypted}")
        except Exception as e:
            print("❌ Decryption failed. Wrong key or corrupted data.")
    else:
        print("❗ Choose either 'e' or 'd'")
