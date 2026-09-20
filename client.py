import json
import shlex
import sys
from socket import *

from constCS import *
from protocol import send_json, recv_json

DEMO_OPERATIONS = [
    {"op": "add", "args": [2, 3]},
    {"op": "divide", "args": [10, 4]},
    {"op": "reverse", "args": ["sistemas distribuidos"]},
    {"op": "word_count", "args": ["cliente e servidor trocam mensagens"]},
]


def parse_argument(token):
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return token


def read_batch():
    print("Digite uma operacao por linha (ex.: add 2 3).")
    print("Linha vazia envia o lote; lote vazio encerra o cliente.")
    operations = []
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            return operations
        if not line:
            return operations
        name, *tokens = shlex.split(line)
        operations.append({"op": name, "args": [parse_argument(t) for t in tokens]})


def request_operations(conn, operations):
    request = {"operations": operations}
    print("Enviado: " + json.dumps(request))
    send_json(conn, request)
    response = recv_json(conn)
    print("Recebido:")
    for entry in response.get("results", []):
        outcome = entry["result"] if "result" in entry else "ERRO: " + entry["error"]
        print("  {}: {}".format(entry["op"], outcome))
    if "error" in response:
        print("  ERRO: " + response["error"])


def main():
    conn = socket(AF_INET, SOCK_STREAM)
    conn.connect((HOST, PORT))
    if "-i" in sys.argv:
        while True:
            operations = read_batch()
            if not operations:
                break
            request_operations(conn, operations)
    else:
        request_operations(conn, DEMO_OPERATIONS)
    conn.close()


if __name__ == "__main__":
    main()
