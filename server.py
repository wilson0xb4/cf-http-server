import socket

ADDR = ('127.0.0.1', 8001)
OK_REQUEST = b"GET / HTTP/1.1"
RESPONSE_200 = (b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/html\r\n"
                b"Accept-Ranges: bytes\r\n"
                b"\r\n"
                b"Hello world!")
RESPONSE_500 = (b"HTTP/1.1 500 Internal Server Error\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: 58\r\n"
                b"\r\n"
                b"The server encountered an unexpected internal server error")


def response_ok():
    return RESPONSE_200


def response_error():
    return RESPONSE_500


def config_server():
    server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

    server.bind(ADDR)
    server.listen(1)
    return server


def start_server():
    print "starting server"
    server = config_server()

    while True:
        try:
            conn, addr = server.accept()
            request = conn.recv(1024)
            if request == OK_REQUEST:
                conn.sendall(response_ok())
            else:
                conn.sendall(response_error())

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_server()
