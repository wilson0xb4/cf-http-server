import server


def start_server(conn, addr):
    """Start server and begin loop to accept requests.

    While in loop, server will respond to appropriate HTTP requests with
    a valid resonpse, logging requests to standard out.
    """

    while True:
        accum = []
        try:
            while True:
                request = conn.recv(64)
                accum.append(request)
                if len(request) < 64:
                    break
            request_text = b''.join(accum)
            print request_text

            response = b''

            try:
                uri = server.parse_request(request_text)
                body, content_type = server.resolve_uri(uri)
                response = server.response_ok(body, content_type)
            except SyntaxError as e:
                response = server.response_error(400, e.message)
            except NotImplementedError as e:
                response = server.response_error(405, e.message)
            except KeyError as e:
                response = server.response_error(400, e.message)
            except ValueError as e:
                response = server.response_error(403, e.message)
            except LookupError as e:
                response = server.response_error(404, e.message)


            conn.sendall(response)

            conn.close()

        except KeyboardInterrupt:
            break


def start_gen_server():
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    gserver = StreamServer(server.ADDR, start_server)
    print('Starting gen server on port 8002')
    gserver.serve_forever()


if __name__ == '__main__':
    start_gen_server()
