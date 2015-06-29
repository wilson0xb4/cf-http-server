import pytest
import socket
import server
from multiprocessing import Process

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
    client.connect(server.ADDR)
    client.sendall(server.OK_REQUEST)
    response = client.recv(1024)
    assert response == server.RESPONSE_200
