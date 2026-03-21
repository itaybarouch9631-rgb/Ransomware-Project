from client_handler import ClientHandler
from config.server_config import ServerConfig, TLSConfig
from secure_server import SecureServer


def main() -> None:
    tls_config = TLSConfig(certfile="server.crt", private_keyfile="server.key")
    server_config = ServerConfig(host="127.0.0.1", port=8443)

    handler = ClientHandler()

    encryption_server = SecureServer(server_config=server_config, tls_config=tls_config, handler=handler)
    encryption_server.start()


if __name__ == "__main__":
    main()