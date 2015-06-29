import pytest
import socket

ADDR = ('127.0.0.1', 8001)

@pytest.fixture()
def client():
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.connect(ADDR)
    return client
