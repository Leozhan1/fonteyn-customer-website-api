from werkzeug.security import generate_password_hash

password = input("Enter password: ")
hashed = generate_password_hash(password)
print(hashed)
