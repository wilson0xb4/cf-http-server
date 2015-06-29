import pytest
import socket
import server
from multiprocessing import Process

ADDR = ('127.0.0.1', 8001)
OK_REQUEST = b"GET / HTTP/1.1"
ERROR_REQUEST = b"Hey man how's it going"
RESPONSE_200 = b"HTTP/1.1 200 OK"
RESPONSE_500 = b"HTTP/1.1 500 Internal Server Error"

# @pytest.fixture()
# def server_process():
#     process = Process(target=server.start_server())
#     process.start()
#     # process.join()
#     return process
#
# @pytest.fixture()
# def client(server_process=None):
#     client = socket.socket(
#         socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
#     )
#     client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     client.connect(ADDR)
#     return client
#
#
# def test_response_ok():
#     assert server.response_ok() == RESPONSE_200
#
#
# def test_response_error():
#     assert server.response_error() == RESPONSE_500
#
#
# def test_functional_ok(client):
#     client.sendall(OK_REQUEST)
#     response = client.recv(1024)
#     assert response == RESPONSE_200
#
#
# def test_functional_error(client):
#     client.sendall(ERROR_REQUEST)
#     response = client.recv(1024)
#     assert response == RESPONSE_500


def test_temp():
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    client.sendall(OK_REQUEST)
    response = client.recv(1024)
    assert response == RESPONSE_200
