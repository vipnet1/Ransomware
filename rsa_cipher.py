from msilib.schema import Error
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet

from base64 import b64decode, b64encode
import os


global encryptor
global decryptor

encryptor = None
decryptor = None

global encrypted_private_key # with fernet
global encrypted_fernet_key # with server public key
global public_key #client_public_key


# setup encryptor, save public key, encrypted private key(using server public key)
def setup():
    global encrypted_private_key
    global encrypted_fernet_key
    global public_key
    global encryptor

    with open('./keys/public.pem','r') as file:
        server_public_key = RSA.import_key(file.read())
        server_encryptor = PKCS1_OAEP.new(server_public_key)

    encrypted_client_private_key_path = './keys/encrypted_private_key'
    encrypted_fernet_key_path = './keys/encrypted_fernet_key'
    client_public_key_path = './keys/client_public_key.pem'

    try:
        if(os.stat(encrypted_fernet_key_path).st_size !=0 and os.stat(encrypted_client_private_key_path).st_size!=0 and os.stat(client_public_key_path).st_size!=0):
            encrypted_fernet_key = read_key(encrypted_fernet_key_path)
            encrypted_private_key = read_key(encrypted_client_private_key_path)
            
            with open(client_public_key_path,'r') as f:
                public_key = f.read().encode('utf-8')
                public_key_obj = RSA.import_key(f.read())
                encryptor = PKCS1_OAEP.new(public_key_obj)

            return True
    except Exception as e:
        print(e)

    key = RSA.generate(1024)
    print('Generated RSA keys')

    encryptor = PKCS1_OAEP.new(key)

    public_key = key.public_key().exportKey('OpenSSH')

    private_key = key.export_key('PEM')

    fernet_key = Fernet.generate_key()
    fernet = Fernet(fernet_key)
    
    encrypted_private_key = fernet.encrypt(private_key)
    encrypted_fernet_key = server_encryptor.encrypt(fernet_key)
    #print(f'pk: {encrypted_private_key}, fernet: {encrypted_fernet_key}')
    print('Encrypted private key with server public key')
    save_keys()
    return False

def get_encrypted_fernet_key():
    return encrypted_fernet_key

def init_decryptor(fernet_key):
    global decryptor

    fernet = Fernet(fernet_key)

    private_key = fernet.decrypt(encrypted_private_key)
    private_key = RSA.import_key(private_key)

    decryptor = PKCS1_OAEP.new(private_key)

def encrypt(data):
    encripted = encryptor.encrypt(data)
    return b64encode(encripted)

def decrypt(data):
    global decryptor
    
    bin_data = b64decode(data)
    decrypted = decryptor.decrypt(bin_data)
    return decrypted


def read_key(file_path):
    try:
        with open(file_path,'r') as f:
            data = f.read().encode('utf-8')
            return b64decode(data)
    except Exception as e:
        pass


def write_key(file_path, content):
    try:
        data = b64encode(content).decode('utf-8')
        #print(f'data = {data}')
        with open(file_path, 'w') as f:
            f.write(data)
        
        return True
    except:
        return False

def save_keys():
    global public_key
    encrypted_client_private_key_path = './keys/encrypted_private_key'
    encrypted_fernet_key_path = './keys/encrypted_fernet_key'
    client_public_key_path = './keys/client_public_key.pem'
    write_key(encrypted_client_private_key_path, encrypted_private_key)
    write_key(encrypted_fernet_key_path, encrypted_fernet_key)
    try:
        with open(client_public_key_path,'w') as f:
            f.write(public_key.decode('utf-8'))
    except Exception as e:
        print(f'writing client_public_key failed: {e}')
