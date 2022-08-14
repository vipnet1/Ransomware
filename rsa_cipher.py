from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

global encryptor
global decryptor

encryptor = None
decryptor = None

global encrypted_private_key
global public_key

# setup encryptor, save public key, encrypted private key(using server public key)
def setup():
    global encrypted_private_key
    global public_key
    global encryptor

    with open('public.pem','r') as file:
        server_public_key = RSA.import_key(file.read())
        server_encryptor = PKCS1_OAEP.new(server_public_key)

    key = RSA.generate(1024)
    print('Generated RSA keys')

    encryptor = PKCS1_OAEP.new(key)

    public_key = key.public_key().exportKey('OpenSSH').decode("utf-8")

    private_key = key.export_key('PEM')
    encrypted_private_key = server_encryptor.encrypt(private_key)

    print('Encrypted private key with server public key')

    

def encrypt(data):
    # ciphertext = encryptor.encrypt(b'yo')
    pass

def decrypt(data):
    # decrypted = decryptor.decrypt(ciphertext)
    pass