import json


def send_json(sock, payload):
    sock.sendall((json.dumps(payload) + "\n").encode())


def recv_json(sock):
    buffer = b""
    while not buffer.endswith(b"\n"):
        chunk = sock.recv(1024)
        if not chunk:
            return None
        buffer += chunk
    return json.loads(buffer.decode())
