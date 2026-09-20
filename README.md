# Cliente-Servidor com múltiplas operações por requisição

Trabalho de Sistemas Distribuídos (Cap. 2, slide 5), a partir do template
[ClientServerBasics-2.0](https://github.com/professorfabio/ClientServerBasics-2.0).

O exemplo original é um servidor de eco. Aqui o servidor processa a requisição
através de seis operações, e o cliente pode chamar várias delas em uma única
requisição.

## Protocolo

Sockets TCP. Cada mensagem é um objeto JSON terminado por `\n`. A requisição traz a
lista `operations`; a resposta traz `results`, na mesma ordem.

```json
{"operations": [{"op": "add", "args": [2, 3]}, {"op": "reverse", "args": ["socket"]}]}

{"results": [{"op": "add", "result": 5}, {"op": "reverse", "result": "tekcos"}]}
```

Cada resultado traz `result` ou `error`. Uma operação que falha (operação
desconhecida, argumentos errados, divisão por zero) não invalida as outras do lote.

## Operações

| Operação | Argumentos | Retorno |
|---|---|---|
| `add` | dois números | soma |
| `subtract` | dois números | diferença |
| `multiply` | dois números | produto |
| `divide` | dois números | quociente |
| `reverse` | um texto | texto invertido |
| `word_count` | um texto | quantidade de palavras |

## Como executar

Requer apenas Python 3. Host e porta ficam em `constCS.py` (`127.0.0.1:5678`).

```bash
python3 server.py     # em um terminal

python3 client.py     # em outro: envia um lote de demonstração
python3 client.py -i  # modo interativo: uma operação por linha, linha vazia envia
```

Saída do cliente:

```
Enviado: {"operations": [{"op": "add", "args": [2, 3]}, {"op": "divide", "args": [10, 4]}, {"op": "reverse", "args": ["sistemas distribuidos"]}, {"op": "word_count", "args": ["cliente e servidor trocam mensagens"]}]}
Recebido:
  add: 5
  divide: 2.5
  reverse: sodiubirtsid sametsis
  word_count: 5
```

## Arquivos

`constCS.py` (host e porta), `protocol.py` (envio e leitura das mensagens JSON),
`server.py` (operações e laço de conexões), `client.py` (demonstração e modo
interativo).
