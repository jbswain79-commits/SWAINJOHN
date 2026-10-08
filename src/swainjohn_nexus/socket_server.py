import socket
from typing import Any

from swainjohn_nexus.core import parse_soggy011_header

HOST = "0.0.0.0"
PORT = 8443


def launch_secure_listener(
    host: str = HOST,
    port: int = PORT,
    timeout: float = 2.0,
) -> tuple[bool, socket.socket | None]:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(timeout)

    try:
        server.bind((host, port))
        server.listen(1)
        return True, server
    except OSError:
        return False, None


def handle_client_payload(payload: bytes) -> dict[str, Any]:
    parsed = parse_soggy011_header(payload)
    if parsed is False:
        return {"status": "rejected", "reason": "invalid_packet"}
    return {"status": "accepted", "packet": parsed}


def _read_payload(client_socket: socket.socket) -> bytes:
    chunks: list[bytes] = []
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            chunks.append(data)
            if len(data) < 4096:
                break
        except socket.timeout:
            break
    return b"".join(chunks)


def run_server_once(host: str = HOST, port: int = PORT, timeout: float = 2.0) -> dict[str, Any]:
    started, server = launch_secure_listener(host=host, port=port, timeout=timeout)
    if not started or server is None:
        return {"status": "failed", "reason": "bind_failed"}

    try:
        server.settimeout(timeout)
        client_socket, _ = server.accept()
        payload = _read_payload(client_socket)
        client_socket.close()
        return {"status": "ok", "result": handle_client_payload(payload)}
    except socket.timeout:
        return {"status": "timeout"}
    except OSError:
        return {"status": "failed", "reason": "accept_failed"}
    finally:
        try:
            server.close()
        except OSError:
            pass
