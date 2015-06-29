import socket

ADDR = ('127.0.0.1', 8001)
OK_REQUEST = b"GET / HTTP/1.1"
ERROR_REQUEST = b"Hey man how's it going"
RESPONSE_200 = b"HTTP/1.1 200 OK"
RESPONSE_500 = b"HTTP/1.1 500 Internal Server Error"


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
                conn.sendall(RESPONSE_200)
            else:
                conn.sendall(RESPONSE_500)

            # while True:
            #     msg = conn.recv(16)
            #     conn.sendall(msg)
            #     if len(msg) < 16:
            #         conn.close()
            #         break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_server()
