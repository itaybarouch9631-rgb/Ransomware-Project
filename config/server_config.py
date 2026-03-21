from dataclasses import dataclass


@dataclass(frozen=True)
class TLSConfig:
    """TLS-related configuration for the server."""

    certfile: str
    private_keyfile: str


@dataclass(frozen=True)
class ServerConfig:
    """Basic TCP server settings."""

    host: str = "127.0.0.1"
    port: int = 8443
    backlog: int = 5

