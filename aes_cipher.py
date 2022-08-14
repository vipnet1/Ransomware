from hashlib import md5
from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# basically encrypts data via blocks, and each one depends on another(cyber A cryptography theory by the way)

def encrypt(key, data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)))

def decrypt(key, data):
    raw = b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, raw[:AES.block_size])
    return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)

def generate_key():
    random_data = get_random_bytes(30)
    key = md5(random_data.encode('utf8')).digest()
    return key