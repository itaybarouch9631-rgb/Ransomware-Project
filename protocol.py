import struct
from consts.shared_consts import MESSAGE_BYTES_SIZE

def send_msg(sock, data: bytes) -> None:
    length_prefix = struct.pack("!I", len(data))
    sock.sendall(length_prefix + data)

def recvall(sock, n: int) -> bytes | None:
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)

def recv_msg(sock) -> bytes | None:
    raw_len = recvall(sock, MESSAGE_BYTES_SIZE)
    if not raw_len:
        return None
    msg_len = struct.unpack("!I", raw_len)[0]
    return recvall(sock, msg_len)