import os
from cryptography.fernet import Fernet

def generate_key():
    """Generates a key and saves it to a file. 
    In a real remote environment, this would be an Env Variable."""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def main():
    print("--- 🛡️ IRVING'S SECURE VAULT ---")
    password = input("Enter Master Password: ")
    
    # Simple hardcoded check for now
    if password == "don_bosco_2026":
        print("✅ Access Granted.")
        generate_key()
        print("Key initialized. Ready for encryption modules.")
    else:
        print("❌ Access Denied.")

if __name__ == "__main__":
    main()