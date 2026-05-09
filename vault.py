import os
from cryptography.fernet import Fernet

# --- CONFIGURATION ---
KEY_FILE = "secret.key"
DATA_FILE = "vault.json"

def load_key():
    """Loads the encryption key from the local file."""
    return open(KEY_FILE, "rb").read()

def encrypt_data(data):
    """Scrambles the data so it's unreadable without the key."""
    key = load_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    """Unscrambles the data back to plain text."""
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

def initialize_vault():
    """Ensures a key exists before starting."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print("🔑 New encryption key generated.")

def main():
    initialize_vault()
    
    print("--- 🛡️ SECURE VAULT ENGINE ---")
    choice = input("1. Encrypt a message\n2. Decrypt a message\n> ")

    if choice == "1":
        msg = input("Enter secret message to hide: ")
        secret = encrypt_data(msg)
        print(f"🔒 Encrypted String: {secret.decode()}")
    elif choice == "2":
        token = input("Paste the encrypted string: ")
        try:
            original = decrypt_data(token.encode())
            print(f"🔓 Original Message: {original}")
        except Exception:
            print("❌ Error: Invalid key or corrupted data.")

if __name__ == "__main__":
    main()