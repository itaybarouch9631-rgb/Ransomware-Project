from dataclasses import dataclass


@dataclass(frozen=True)
class ClientConfig:
    """Client connection and TLS settings."""

    host: str = "127.0.0.1"
    port: int = 8443
    cafile: str = "server.crt"
    hostname: str = "localhost"
    check_hostname: bool = True

