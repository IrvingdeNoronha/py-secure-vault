import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

DATA_FILE = "vault.json"

def derive_key(password: str):
    """Derives a cryptographic key from a master password."""
    if not password:
        return None
    salt = b'irving_goa_salt' 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

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
    try:
        with open(DATA_FILE, "rb") as f_in:
            encrypted_data = f_in.read()
        decrypted_data = f.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)
    except Exception:
        return None

def main():
    print("--- 🛡️ IRVING'S SECURE VAULT v2.1 ---")
    
    # --- SETUP OR UNLOCK FLOW ---
    if not os.path.exists(DATA_FILE):
        print("First time setup: No vault found.")
        master_pwd = input("Set your Master Password: ")
        confirm_pwd = input("Confirm Master Password: ")
        
        if master_pwd != confirm_pwd:
            print("❌ Passwords do not match. Restarting...")
            return
        
        # Initialize an empty vault with the new password
        save_vault({}, master_pwd)
        print("✅ Vault created successfully!")
    else:
        master_pwd = input("Enter Master Password to unlock: ")

    # --- LOAD DATA ---
    vault = load_vault(master_pwd)
    
    if vault is None:
        print("❌ Incorrect password. Access Denied.")
        return

    print("🔓 Vault Unlocked.")

    # --- MAIN MENU ---
    while True:
        print("\n1. Add Password | 2. Retrieve | 3. List | 4. Exit")
        choice = input("> ")

        if choice == "1":
            service = input("Service: ").lower().strip()
            pwd = input(f"Password for {service}: ")
            vault[service] = pwd
            save_vault(vault, master_pwd)
            print("✅ Saved.")
        elif choice == "2":
            service = input("Service: ").lower().strip()
            print(f"🔓 {vault.get(service, 'Not found.')}")
        elif choice == "3":
            print(f"Managed Services: {', '.join(vault.keys()) if vault else 'None'}")
        elif choice == "4":
            print("Stay secure. Goodbye!")
            break

if __name__ == "__main__":
    main()