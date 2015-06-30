import socket

ADDR = ('127.0.0.1', 8002)
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
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(ADDR)
    server.listen(1)
    return server


def start_server():
    server = config_server()
    accum = []

    while True:
        try:
            conn, addr = server.accept()
            while True:
                request = conn.recv(16)
                accum.append(request)
                if len(request) < 16:
                    break
            request_text = b''.join(accum)
            print request_text
            if OK_REQUEST in request_text:
                conn.sendall(response_ok())
            else:
                conn.sendall(response_error())
            conn.close()

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_server()
