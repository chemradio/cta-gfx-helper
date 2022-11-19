import secrets

for _ in range(20):
    print(secrets.token_hex(8))