from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet

from base64 import b64decode, b64encode

global encryptor
global decryptor

encryptor = None
decryptor = None

global encrypted_private_key # with fernet
global encrypted_fernet_key # with server public key
global public_key

ENCRYPTION_CHUNKS = 100

# setup encryptor, save public key, encrypted private key(using server public key)
def setup():
    global encrypted_private_key
    global encrypted_fernet_key
    global public_key
    global encryptor

    with open('public.pem','r') as file:
        server_public_key = RSA.import_key(file.read())
        server_encryptor = PKCS1_OAEP.new(server_public_key)

    key = RSA.generate(1024)
    print('Generated RSA keys')

    encryptor = PKCS1_OAEP.new(key)

    public_key = key.public_key().exportKey('OpenSSH')

    private_key = key.export_key('PEM')

    fernet_key = Fernet.generate_key()
    fernet = Fernet(fernet_key)
    
    encrypted_private_key = fernet.encrypt(private_key)
    encrypted_fernet_key = server_encryptor.encrypt(fernet_key)

    print('Encrypted private key with server public key')

def get_encrypted_fernet_key():
    return encrypted_fernet_key

def encrypt(data):
    encripted = encryptor.encrypt(data)
    return b64encode(encripted)

def decrypt(data):
    # decrypted = decryptor.decrypt(ciphertext)
    pass