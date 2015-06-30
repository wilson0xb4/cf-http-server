import pytest
import socket
import server
import time
from multiprocessing import Process


@pytest.yield_fixture
def server_process():
    process = Process(target=server.start_server)
    process.daemon = True
    process.start()
    time.sleep(0.1)
    yield process


@pytest.fixture()
def client(server_process):
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(server.ADDR)
    return client


def test_response_ok():
    response = server.response_ok().split(b'\r\n')
    assert b"HTTP/1.1 200 OK" in response[0]
    assert b"Content-Type: text/html" in response


def test_response_error():
    response = server.response_error().split(b'\r\n')
    assert b"HTTP/1.1 500 Internal Server Error" in response[0]
    assert b"Content-Type: text/plain" in response


def test_parse_request():
    requests = {
        'good': [
            b'GET / HTTP/1.1',
            b'Host: www.example.com',
            server.CRLF
        ],
        'bad': [
            b'Hi there'
        ],
        'long': [
            b'GET /path/to/a/thing HTTP/1.1',
            b'Host: www.longerexample.com:80',
            b'Content-Type: text/xml; charset=utf-8',
            b'Content-Length: 100',
            server.CRLF
        ],
        'post': [
            b'POST / HTTP/1.1',
            b'Host: www.example.com',
            server.CRLF
        ],
        'wrong_http': [
            b'GET / HTTP/1.0',
            b'Host: www.example.com',
            server.CRLF
        ],
    }

    expects = {
        'good': b'/',
        'bad': SyntaxError,
        'long': b'/path/to/a/thing',
        'post': NotImplementedError,
        'wrong_http': ValueError
    }

    request_text = server.CRLF.join(requests['good'])
    assert server.parse_request(request_text) == expects['good']

    request_text = server.CRLF.join(requests['bad'])
    with pytest.raises(expects['bad']):
        server.parse_request(request_text)

    request_text = server.CRLF.join(requests['long'])
    assert server.parse_request(request_text) == expects['long']

    request_text = server.CRLF.join(requests['post'])
    with pytest.raises(expects['post']):
        server.parse_request(request_text)

    request_text = server.CRLF.join(requests['wrong_http'])
    with pytest.raises(expects['wrong_http']):
        server.parse_request(request_text)
    #
    # for key, request in requests.iteritems():
    #     request_text = server.CRLF.join(request)
    #     if key in ('good', 'long'):
    #         assert server.parse_request(request_text) == expects[key]
    #     else:
    #         print key
    #         with pytest.raises(expects[key]):
    #             server.parse_request(request_text)


def test_functional_ok(client):
    client.sendall(server.OK_REQUEST)
    accum = []
    while True:
        response = client.recv(1024)
        accum.append(response)
        if len(response) < 1024:
            break
    response_str = b''.join(accum)
    assert b"HTTP/1.1 200 OK" in response_str
