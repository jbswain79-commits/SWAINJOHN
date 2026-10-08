import socket
import threading
import time

from swainjohn_nexus.packet_factory import create_valid_packet
from swainjohn_nexus.socket_server import handle_client_payload, launch_secure_listener


def test_handle_client_payload_accepts_valid_packet():
    packet = create_valid_packet()
    result = handle_client_payload(packet)
    assert result["status"] == "accepted"
    assert result["packet"]["security_tag"] == "usg-ai-node"


def test_handle_client_payload_rejects_invalid_packet():
    result = handle_client_payload(b"bad-packet")
    assert result["status"] == "rejected"


def test_listener_binds_and_accepts():
    started, server = launch_secure_listener(host="127.0.0.1", port=0, timeout=1.0)
    assert started is True
    assert server is not None

    bound_port = server.getsockname()[1]

    def client_sender():
        time.sleep(0.2)
        client = socket.create_connection(("127.0.0.1", bound_port), timeout=2)
        client.sendall(create_valid_packet())
        client.close()

    sender = threading.Thread(target=client_sender)
    sender.start()

    client_socket, _ = server.accept()
    payload = client_socket.recv(4096)
    assert payload == create_valid_packet()
    client_socket.close()
    server.close()
    sender.join()
