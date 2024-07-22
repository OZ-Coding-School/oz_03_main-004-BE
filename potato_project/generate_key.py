# generate_key.py
from cryptography.fernet import Fernet
import os

# 키 파일 경로 설정
key_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fernet.key')

# 키 파일이 이미 존재하는지 확인
if os.path.exists(key_file_path):
    print(f"Key file already exists at {key_file_path}")
else:
    # 새 키 생성
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
    print(f"Key file generated and saved at {key_file_path}")
