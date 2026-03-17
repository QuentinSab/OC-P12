from utils.password import hash_password, verify_password

hashed = hash_password("test123")

print(hashed)
print(verify_password("test123", hashed), "doit être vrai.")
print(verify_password("wrong", hashed), "doit être faux.")
