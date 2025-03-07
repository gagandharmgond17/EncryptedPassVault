from cryptography.fernet import Fernet
import random
import string
import os
def load_or_generate_key():
    key_file = "secret.key"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
    else:
        with open(key_file, 'rb') as file:
            key = file.read()
    return Fernet(key)
def generate_password(length=12):
    if length < 6:
        raise ValueError("Password length must be at least 6 characters.")
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.SystemRandom().choice(characters) for _ in range(length))
def save_password_encrypted(password, fernet):
    encrypted_password = fernet.encrypt(password.encode())
    files = [name for name in os.listdir('.') if name.startswith("password_") and name.endswith(".bin")]
    filename = f'password_{len(files) + 1}.bin'
    with open(filename, 'wb') as file:
        file.write(encrypted_password)
    return filename
def decrypt_password(filename, fernet):
    try:
        if not os.path.exists(filename):
            return "❌ Error: File not found."
        with open(filename, 'rb') as file:
            encrypted_password = file.read()
        return fernet.decrypt(encrypted_password).decode()
    except Exception as e:
        return f"❌ Error decrypting file: {str(e)}"
def auto_delete_old_files(limit=5):
    files = sorted(
        [f for f in os.listdir('.') if f.startswith("password_") and f.endswith(".bin")],
        key=os.path.getctime
    )
    while len(files) > limit:
        os.remove(files.pop(0))
def main():
    fernet = load_or_generate_key()
    while True:
        print("\nOptions:\n1. Generate & Save Password\n2. Retrieve Password\n3. Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            try:
                length = int(input("Enter password length (min 6): ").strip())
                password = generate_password(length)
                filename = save_password_encrypted(password, fernet)
                auto_delete_old_files()
                print(f"✅ Password saved in encrypted file: {filename}")
            except ValueError as ve:
                print(f"❌ Error: {ve}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
        elif choice == '2':
            filename = input("Enter password file name (e.g., password_1.bin): ").strip()
            decrypted_password = decrypt_password(filename, fernet)
            print(f"🔓 Decrypted Password: {decrypted_password}")
        elif choice == '3':
            print("Exiting... Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice, try again.")
if __name__ == "__main__":
    main()
