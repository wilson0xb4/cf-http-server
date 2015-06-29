import socket


def response_ok():
    return b"HTTP/1.1 200 OK"


def response_error():
    return b"HTTP/1.1 500 Internal Server Error"


def config_server():
    ADDR = ('127.0.0.1', 8001)

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
            while True:
                msg = conn.recv(16)
                conn.sendall(msg)
                if len(msg) < 16:
                    conn.close()
                    break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_server()
