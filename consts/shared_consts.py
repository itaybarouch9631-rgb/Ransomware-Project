import ssl
from Crypto.Cipher import AES


MINIMUM_SSL_VERSION = ssl.TLSVersion.TLSv1_2
MESSAGE_BYTES_SIZE = 4
AES_MODE = AES.MODE_CTR
