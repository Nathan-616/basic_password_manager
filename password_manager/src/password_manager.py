# Imports
from cryptography.fernet import Fernet
import base64
import hashlib
import os

def write_key():
    import os.path
    if not os.path.isfile("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

def load_key(master_pwd):
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    hashed_master_pwd = hashlib.sha256(master_pwd.encode()).digest()
    
    # Use XOR (^) to combine bytes of the key and hashed password
    combined_key = bytes(k1 ^ k2 for k1, k2 in zip(key, hashed_master_pwd))
    
    # Ensure the key is 32 bytes long and encoded in URL-safe base64
    key_32_bytes = hashlib.sha256(combined_key).digest()
    key_base64 = base64.urlsafe_b64encode(key_32_bytes)

    return key_base64

def display_menu():
    print("\nSelect an option:")
    print("1. View existing passwords")
    print("2. Add a new password")
    print("3. Quit")

def view(fer):
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())

def add(fer):
    name = input('Account Name: ')
    pwd = input('Password: ')

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")
    print("Password added successfully!")

def main():
    write_key()  # Generate the key file if it doesn't exist
    master_pwd = input("Enter the master password: ")

    # Check if the key file exists before loading the key
    if os.path.isfile("key.key"):
        key = load_key(master_pwd)
        fer = Fernet(key)

        while True:
            display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                view(fer)  # Pass fer to the view function
            elif choice == "2":
                add(fer)   # Pass fer to the add function
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select a valid option.")
    else:
        print("Key file does not exist. Run the program again to create the key file.")

if __name__ == "__main__":
    main()