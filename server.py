import socket
from pathlib import Path
import mimetypes

CRLF = b'\r\n'
ADDR = ('127.0.0.1', 8002)
RESPONSE = CRLF.join([
    b"HTTP/1.1 {code} {reason}",
    b"Content-Type: {content_type}",
    b"Content-Length: {content_length}",
    b"",
    b"{message}"])
WEB_ROOT = b'./webroot'


def response_ok(body, content_type):
    """Return a properly formatted HTTP 200 response."""
    return RESPONSE.format(
        code=200,
        reason=b'OK',
        content_type=content_type,
        content_length=len(body),
        message=body)


def response_error(code, reason):
    """Return a properly formatted HTTP 500 response."""
    return RESPONSE.format(
        code=code,
        reason=reason,
        content_type=b'text/plain',
        content_length=b'',
        message=b'')


def verify_first_line(parts):
    """Verify that the first line of the request is a GET request and
    using HTTP/1.1
    """

    if parts[0] != b'GET':
        raise NotImplementedError(b"Method Not Allowed")
    if parts[2] != b'HTTP/1.1':
        raise ValueError(b"Forbidden")


def verify_blank_line(rq):
    """Verify there is a blank line in the request.

    Will be at the end or between the headers and the body.
    """

    if CRLF+CRLF not in rq:
        raise SyntaxError(b"Bad Request")


def verify_host(header_dict):
    """Verify that the Host header is in the request."""
    if b'Host' not in header_dict.keys():
        raise KeyError(b"Bad Request")


def parse_request(rq):
    """Parse the request from the client and return the URI if valid.

    Valid request returns URI if all are True:
        - Only accept GET requests
        - Only accept HTTP/1.1 requests
        - Must include Host header
    Otherwise, exception is raised and the reason code is passed with
    the exception.
    """

    verify_blank_line(rq)
    header_and_body = rq.split(CRLF + CRLF, 1)
    header_dict = {}
    lines = header_and_body[0].split(CRLF)
    first = lines[0]
    first_line_parts = first.split()
    verify_first_line(first_line_parts)
    lines = lines[1:]
    temp = ''
    for line in lines:
        if b':' in line:
            header = line.split(b':')
            temp = header[0]
            header_dict[header[0]] = header[1:]
        else:
            header_dict[temp].append(line)

    verify_host(header_dict)

    body, content_type = resolve_uri(uri)

    return first_line_parts[1]


def resolve_uri(uri):
    p = Path(WEB_ROOT + uri)
    if not p.exists():
        raise LookupError(b'Not Found')

    body = b''
    content_type = b''
    if p.is_dir():
        gen = p.iterdir()
        body = CRLF.join([str(item) for item in gen])
        content_type = b'text/html'

    else:
        with p.open() as f:
            body = f.read()
            content_type = mimetypes.guess_type(uri)[0]

    return body, content_type


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

    while True:
        accum = []
        try:
            conn, addr = server.accept()
            while True:
                request = conn.recv(1024)
                accum.append(request)
                if len(request) < 1024:
                    break
            request_text = b''.join(accum)
            print request_text

            response = b''

            try:
                uri = parse_request(request_text)
                body, content_type = resolve_uri(uri)
                response = response_ok(body, content_type)
            except SyntaxError as e:
                response = response_error(400, e.message)
            except NotImplementedError as e:
                response = response_error(405, e.message)
            except KeyError as e:
                response = response_error(400, e.message)
            except ValueError as e:
                response = response_error(403, e.message)
            except LookupError as e:
                response = response_error(404, e.message)

            conn.sendall(response)

            conn.close()

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    start_server()
