from __future__ import annotations

import socket
import ssl

from config.server_config import ServerConfig, TLSConfig
from client_handler import ClientHandler

from consts.shared_consts import MINIMUM_SSL_VERSION
import threading

class SecureServer:
    """
    Simple TLS server that accepts clients and delegates
    the conversation to a ClientHandler instance.

    Less complex: no inheritance or factories here, just one handler object
    that knows how to process a connection.
    """

    def __init__(
        self,
        server_config: ServerConfig,
        tls_config: TLSConfig,
        handler: ClientHandler,
    ) -> None:
        self._cfg = server_config
        self._tls_cfg = tls_config
        self._handler = handler
        self._context = self._create_tls_context()

    def _create_tls_context(self) -> ssl.SSLContext:
        """Create and configure the TLS context for the server."""
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(
            certfile=self._tls_cfg.certfile,
            keyfile=self._tls_cfg.private_keyfile,
        )
        ctx.minimum_version = MINIMUM_SSL_VERSION
        return ctx

    def start(self) -> None:
        """Start the server loop (blocking)."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self._cfg.host, self._cfg.port))
            sock.listen(self._cfg.backlog)

            print(f"SecureServer listening on {self._cfg.host}:{self._cfg.port}")
            
            while True:
                client_sock, addr = sock.accept()
                print(f"Connection from {addr}")
                client_thread = threading.Thread(
                    target=self._handle_client, 
                    args=(client_sock,)
                )
                client_thread.start()

    def _handle_client(self, client_sock: socket.socket) -> None:
        try:
            with self._context.wrap_socket(client_sock, server_side=True) as tls_conn:
                print("TLS handshake completed with client")
                self._handler.handle(tls_conn)
        except ssl.SSLError as e:
            print(f"ERROR: TLS/SSL error: {e}")
        except Exception as e:
            print(f"ERROR: General error: {e}")
