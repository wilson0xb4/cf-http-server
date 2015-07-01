import socket

CRLF = b'\r\n'
ADDR = ('127.0.0.1', 8002)
RESPONSE_200 = (b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/html\r\n"
                b"Accept-Ranges: bytes\r\n"
                b"\r\n"
                b"Hello world!")
RESPONSE = [
    b"HTTP/1.1 {code} {reason}",
    b"Content-Type: text/plain",
    CRLF,
    b"{message}"]


def response_ok():
    """Return a properly formatted HTTP 200 response."""
    return RESPONSE_200


def response_error(code, reason):
    """Return a properly formatted HTTP 500 response."""
    response = CRLF.join(RESPONSE)
    return response.format(code=code, reason=reason, message=b'')


def verify_first_line(line):
    if b'GET' not in line:
        raise NotImplementedError(b"Method Not Allowed")
    if b'HTTP/1.1' not in line:
        raise ValueError(b"Forbidden")


def verify_blank_line(rq):
    if CRLF+CRLF not in rq:
        raise SyntaxError(b"Bad Request")


def verify_host(header_dict):
    if b'Host' not in header_dict.keys():
        raise KeyError(b"Bad Request")


def parse_request(rq):
    verify_blank_line(rq)
    header_dict = {}
    lines = rq.split(CRLF)
    first = lines[0]
    lines = lines[1:]
    verify_first_line(first)
    temp = ''
    for line in lines:
        if b':' in line:
            header = line.split(b':')
            temp = header[0]
            header_dict[header[0]] = header[1:]
        else:
            header_dict[temp].append(line)

    verify_host(header_dict)

    #get uri from first line of request
    return first.split()[1]


def config_server():
    """Configure server: create socket, bind and set to listen."""
    server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(ADDR)
    server.listen(1)
    return server


def start_server():
    """Start server and begin loop to accept requests.

    While in loop, server will respond to appropriate HTTP requests with
    a valid resonpse, logging requests to standard out.
    """
    server = config_server()
    accum = []

    while True:
        try:
            conn, addr = server.accept()
            while True:
                request = conn.recv(1024)
                accum.append(request)
                if len(request) < 1024:
                    break
            request_text = b''.join(accum)
            print request_text

            response = response_ok()

            try:
                parse_request(request_text)
            except SyntaxError as e:
                response = response_error(400, e.message)
            except NotImplementedError as e:
                response = response_error(405, e.message)
            except KeyError as e:
                response = response_error(400, e.message)
            except ValueError as e:
                response = response_error(403, e.message)

            conn.sendall(response)

            conn.close()

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_server()
