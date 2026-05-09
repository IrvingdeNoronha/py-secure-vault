import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

DATA_FILE = "vault.json"

def derive_key(password: str):
    """Derives a cryptographic key from a master password."""
    # We use a hardcoded salt here for the demo, 
    # but in a pro app, this would be saved in a separate file.
    salt = b'irving_goa_salt' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def save_vault(data, password):
    key = derive_key(password)
    f = Fernet(key)
    encrypted_data = f.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as f_out:
        f_out.write(encrypted_data)

def load_vault(password):
    if not os.path.exists(DATA_FILE):
        return {}
    
    key = derive_key(password)
    f = Fernet(key)
    with open(DATA_FILE, "rb") as f_in:
        encrypted_data = f_in.read()
    
    try:
        decrypted_data = f.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)
    except Exception:
        # If the password is wrong, decryption will fail here
        return None

def main():
    print("--- 🛡️ IRVING'S SECURE VAULT v2.0 ---")
    master_pwd = input("Enter Master Password to unlock vault: ")
    
    vault = load_vault(master_pwd)
    
    if vault is None:
        print("❌ Incorrect Master Password or Corrupted Vault. Access Denied.")
        return

    while True:
        print("\n1. Add Password | 2. Retrieve | 3. List | 4. Exit")
        choice = input("> ")

        if choice == "1":
            service = input("Service: ").lower()
            pwd = input(f"Password for {service}: ")
            vault[service] = pwd
            save_vault(vault, master_pwd)
            print("✅ Saved.")
        elif choice == "2":
            service = input("Service: ").lower()
            print(f"🔓 {vault.get(service, 'Not found.')}")
        elif choice == "3":
            print(f"Managed: {', '.join(vault.keys())}")
        elif choice == "4":
            break

if __name__ == "__main__":
    main()