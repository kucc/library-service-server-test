import os
import base64

def generate_salt(length=16):
    # 무작위 바이트 시퀀스 생성
    salt = os.urandom(length)
    return salt

def encode_salt(salt):
    # 솔트를 base64로 인코딩
    encoded_salt = base64.b64encode(salt).decode('utf-8')
    return encoded_salt

# 솔트 생성 및 인코딩 예시
for _ in range(5):
    print("======")
    salt = generate_salt()
    print(salt)
    encoded_salt = encode_salt(salt)[8:]
    print(encoded_salt)
