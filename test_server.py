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
    response = server.response_ok().split(b'\r\n')
    assert b"HTTP/1.1 200 OK" in response[0]
    assert b"Content-Type: text/html" in response


def test_response_error():
    response = server.response_error().split(b'\r\n')
    assert b"HTTP/1.1 500 Internal Server Error" in response[0]
    assert b"Content-Type: text/plain" in response


def test_functional_ok(client):
    client.sendall(server.OK_REQUEST)
    accum = []
    while True:
        response = client.recv(16)
        accum.append(response)
        if len(response) < 16:
            break
    response_str = b''.join(accum)
    assert b"HTTP/1.1 200 OK" in response_str
