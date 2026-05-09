import os
import json
from cryptography.fernet import Fernet

# Configuration - File names for the key and the database
KEY_FILE = "secret.key"
DATA_FILE = "vault.json"

def initialize_vault():
    """Generates an encryption key if it doesn't already exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print("🔑 System: New encryption key generated.")

def load_key():
    """Reads the key from the secret.key file."""
    return open(KEY_FILE, "rb").read()

def save_vault(data):
    """Encrypts the entire password dictionary and saves it to vault.json."""
    key = load_key()
    f = Fernet(key)
    # Convert the dictionary to a string, then encrypt it
    encrypted_data = f.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as f_out:
        f_out.write(encrypted_data)

def load_vault():
    """Decrypts and loads the password database."""
    if not os.path.exists(DATA_FILE):
        return {} # Return empty dictionary if no data exists yet
    
    key = load_key()
    f = Fernet(key)
    with open(DATA_FILE, "rb") as f_in:
        encrypted_data = f_in.read()
    
    try:
        # Decrypt the file content and turn it back into a Python dictionary
        decrypted_data = f.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)
    except Exception:
        print("⚠️ Warning: Could not decrypt vault. Data may be corrupted or key is missing.")
        return {}

def main():
    initialize_vault()
    vault = load_vault()

    while True: # Keep the program running until the user chooses to exit
        print("\n--- 🛡️ IRVING'S SECURE VAULT v1.0 ---")
        print("1. Add/Update Password")
        print("2. Retrieve Password")
        print("3. List Services")
        print("4. Exit")
        
        choice = input("> ")

        if choice == "1":
            service = input("Enter Service Name (e.g., GitHub): ").lower()
            pwd = input(f"Enter Password for {service}: ")
            vault[service] = pwd
            save_vault(vault)
            print(f"✅ Credentials for {service} saved securely.")

        elif choice == "2":
            service = input("Enter Service Name: ").lower()
            if service in vault:
                print(f"🔓 Password for {service}: {vault[service]}")
            else:
                print("❌ Service not found.")

        elif choice == "3":
            print("\n--- Managed Services ---")
            if not vault:
                print("(No services stored)")
            for s in vault.keys():
                print(f"- {s}")
                
        elif choice == "4":
            print("Stay secure. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()