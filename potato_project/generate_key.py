# generate_key.py
import secrets

def generate_key():
    return secrets.token_urlsafe(50)

if __name__ == "__main__":
    key = generate_key()
    with open('key_file.txt', 'w') as f:
        f.write(key)
    print(f"Key generated and saved to key_file.txt: {key}")
