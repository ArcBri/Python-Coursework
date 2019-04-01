from socket import *
import sys
import os

store = {}

class Response:
    status_names = {
        200: "OK",
        403: "Forbidden",
        404: "NotFound",
        400: "BadRequest",
    }

    def __init__(self, code, body=None):
        self.code = code
        self.body = body

    def process(self) :
        # returns a byte object that is ready to be sent to client
        header = str(self.code) + " " + self.status_names[self.code]
        if self.body:
            header += " content-length " + str(len(self.body))
        output = (header + "  ").encode()
        if self.body:
            output += self.body
        print('Sending response with header: "' + header + '"\n')
        return output

def main():
    server_port = int(sys.argv[1])
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print('Server listening at port ' + str(server_port))
    while True:
        client_socket, addr = server_socket.accept()
        print(addr, 'connected')
        leftover = None
        while True:
            print('Ready to receive request')
            header, body, leftover = get_full_request(client_socket, leftover)
            if not header:
                break
            print('Request fully processed, header is: "' + header + '"')
            res = form_response(header, body)
            client_socket.send(res.process())
        print(addr, 'disconnected')
        print()
        client_socket.close()

def get_full_request(client_socket, leftover):
    # returns header as a string
    # body as a bytes object
    # and leftover as a bytes object
    # double spaces between header and body are discarded
    full_req = b''
    partial_req = leftover if leftover else client_socket.recv(4096)
    # connection to client is detected as lost when request received is empty
    if len(partial_req) == 0:
        return None, None, None
    # keep receiving from client until latest message contains a ' '
    while b' ' not in partial_req:
        print('Method still undetermined, waiting for more')
        full_req += partial_req
        partial_req = client_socket.recv(4096)
        if len(partial_req) == 0:
            return None, None, None
        print('Received next')
    method = full_req.decode() +  partial_req.split(b' ', 1)[0].decode()
    print('Method is "' + method + '"')
    # keep receiving from client until all previous messages
    # and latest message together contains '  '
    while b'  ' not in (full_req + partial_req):
        print('Full header still undetermined, waiting for more')
        full_req += partial_req
        partial_req = client_socket.recv(4096)
        if len(partial_req) == 0:
            return None, None, None
        print('Received next')
    header = full_req.decode() + partial_req.split(b'  ', 1)[0].decode()
    print('Header is "' + header + '"')
    # assuming that only POST requests expect a body
    if method.upper() == 'POST':
        fields = [h.lower() for h in header.split(' ')]
        content_length = int(fields[fields.index('content-length') + 1])
        body = partial_req.split(b'  ', 1)[1]
        while len(body) < content_length:
            partial_req = client_socket.recv(4096)
            if len(partial_req) == 0:
                return None, None, None
            body += partial_req
        body, leftover = body[:content_length], body[content_length:]
    else:
        body = None
        try:
            leftover = partial_req.split(b'  ', 1)[1]
        except IndexError:
            leftover = None
    return header, body, leftover

def form_response(header, body):
    method = header.split(' ', 2)[0]
    prefix = header.split(' ', 2)[1].split('/', 2)[1]
    dest = header.split(' ', 2)[1].split('/', 2)[2]
    if prefix == 'key':
        key = dest
        if method.upper() == 'GET':
            return get_key(key)
        elif method.upper() == 'POST':
            return post_key(key, body)
        elif method.upper() == 'DELETE':
            return delete_key(key)
        else:
            return Response(400, ('Unrecognised method: ' + method).encode())
    elif prefix == 'file':
        path = dest
        if method.upper() == 'GET':
            return get_file(path)
        else:
            return Response(400, ('Unrecognised method: ' + method).encode())
    else:
        return Response(400, ('Unrecognised prefix: ' + prefix).encode())

def get_key(key):
    if key not in store:
        return Response(404)
    value = store[key]
    return Response(200, value)

def isfile_case_sensitive(path):
    # in windows path is case insensitive
    # hence the need for a custom function to check
    if not os.path.isfile(path):
        return False
    dir, filename = os.path.split(path)
    if not dir:
        dir = '.'
    return filename in os.listdir(dir)

def get_file(path):
    if not isfile_case_sensitive(path):
        return Response(404)
    try:
        with open(path, "rb") as f: # will read file as bytes. DONT ENCODE
            value = f.read()
            return Response(200, value)
    except (PermissionError, OSError):
        return Response(403)

def post_key(key, body):
    global store # how dirty!
    store[key] = body
    return Response(200)

def delete_key(key):
    if key not in store:
        return Response(404)
    value = store.pop(key)
    return Response(200, value)

main()
