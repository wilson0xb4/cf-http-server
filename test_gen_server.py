from multiprocessing import Process
import pytest
import socket
import time

import gen_server
import server

CRLF = b'\r\n'


@pytest.fixture(scope='session')
def server_process(request):
    process = Process(target=gen_server.start_gen_server)
    process.daemon = True
    process.start()
    time.sleep(0.1)

    def cleanup():
        process.terminate()

    request.addfinalizer(cleanup)
    return process


@pytest.fixture()
def client(server_process):
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(server.ADDR)
    return client


@pytest.fixture()
def requests():
    requests = {
        'good': [
            b'GET / HTTP/1.1',
            b'Host: www.example.com',
            CRLF
        ],
        'bad': [
            b'Hi there'
        ],
        'long': [
            b'GET /path/to/a/thing HTTP/1.1',
            b'Host: www.longerexample.com:80',
            b'Content-Type: text/xml; charset=utf-8',
            b'Content-Length: 100',
            CRLF
        ],
        'post': [
            b'POST / HTTP/1.1',
            b'Host: www.example.com',
            CRLF
        ],
        'wrong_http': [
            b'GET / HTTP/1.0',
            b'Host: www.example.com',
            CRLF
        ],
    }
    return requests


def test_functional_ok(client, requests):
    request_text = CRLF.join(requests['good'])
    client.sendall(request_text)
    accum = []
    while True:
        response = client.recv(1024)
        accum.append(response)
        if len(response) < 1024:
            break
    response_str = b''.join(accum)
    assert b"HTTP/1.1 200 OK" in response_str


def test_functional_bad(client, requests):
    request_text = CRLF.join(requests['bad'])
    client.sendall(request_text)
    accum = []
    while True:
        response = client.recv(1024)
        accum.append(response)
        if len(response) < 1024:
            break
    response_str = b''.join(accum)
    assert b"HTTP/1.1 400 Bad Request" in response_str
