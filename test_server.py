import pytest
import socket
import server
from multiprocessing import Process

@pytest.yield_fixture
def server_process():
    process = Process(target=server.start_server)
    process.daemon = True
    process.start()
    yield process

@pytest.fixture()
def client():
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(server.ADDR)
    return client


def test_response_ok(server_process):
    assert server.response_ok() == server.RESPONSE_200


def test_response_error():
    assert server.response_error() == server.RESPONSE_500


def test_functional_ok(client):
    client.sendall(server.OK_REQUEST)
    response = client.recv(1024)
    assert response == server.RESPONSE_200
