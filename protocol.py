import struct
import socket
import ssl
from typing import Union

from consts.shared_consts import MESSAGE_BYTES_SIZE

SocketType = Union[socket.socket, ssl.SSLSocket]

def send_msg(sock: SocketType, data: bytes) -> None:
    length_prefix = struct.pack("!I", len(data))
    sock.sendall(length_prefix + data)

def recvall(sock: SocketType, n: int) -> bytes | None:
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)

def recv_msg(sock: SocketType) -> bytes | None:
    raw_len = recvall(sock, MESSAGE_BYTES_SIZE)
    if not raw_len:
        return None
    msg_len = struct.unpack("!I", raw_len)[0]
    return recvall(sock, msg_len)