# Cliente-Servidor com múltiplas operações por requisição

Trabalho de Sistemas Distribuídos (Cap. 2, slide 5), a partir do template
[ClientServerBasics-2.0](https://github.com/professorfabio/ClientServerBasics-2.0).

O exemplo original é um servidor de eco: ele recebe bytes e devolve os mesmos bytes
com um `*` no final. Este projeto acrescenta duas coisas:

1. **Processamento real no servidor** — seis operações que recebem dados do cliente,
   processam e devolvem o resultado.
2. **Várias funcionalidades por requisição** — o cliente envia uma lista de operações
   em uma única mensagem e recebe todos os resultados juntos, na mesma ordem.

## Protocolo

Comunicação por sockets TCP. Cada mensagem é um objeto JSON em UTF-8 terminado por
`\n`. A requisição carrega a lista `operations`; a resposta carrega a lista `results`,
na mesma ordem das operações enviadas.

Requisição:

```json
{"operations": [{"op": "add", "args": [2, 3]},
                {"op": "reverse", "args": ["socket"]},
                {"op": "word_count", "args": ["ola mundo"]}]}
```

Resposta:

```json
{"results": [{"op": "add", "result": 5},
             {"op": "reverse", "result": "tekcos"},
             {"op": "word_count", "result": 2}]}
```

Cada item da resposta traz `result` (sucesso) **ou** `error` (falha). Uma operação
que falha não invalida as outras do mesmo lote.

## Operações disponíveis

| Operação | Argumentos | Retorno |
|---|---|---|
| `add` | dois números | soma |
| `subtract` | dois números | diferença |
| `multiply` | dois números | produto |
| `divide` | dois números | quociente (erro se o divisor for zero) |
| `reverse` | um texto | texto invertido |
| `word_count` | um texto | quantidade de palavras |

## Como executar

Requer apenas Python 3 (nenhuma dependência externa). Host e porta ficam em
`constCS.py` (`127.0.0.1:5678`).

Em um terminal:

```bash
python3 server.py
```

Em outro terminal:

```bash
python3 client.py        # envia um lote de demonstração com 4 operações
python3 client.py -i     # modo interativo: você monta o lote
```

No modo interativo, digite uma operação por linha (`add 2 3`); uma linha vazia envia
o lote acumulado e um lote vazio encerra o cliente. Textos com espaço vão entre
aspas: `reverse "ola mundo"`.

## Exemplo de execução

Cliente (`python3 client.py`):

```
Enviado: {"operations": [{"op": "add", "args": [2, 3]}, {"op": "divide", "args": [10, 4]}, {"op": "reverse", "args": ["sistemas distribuidos"]}, {"op": "word_count", "args": ["cliente e servidor trocam mensagens"]}]}
Recebido:
  add: 5
  divide: 2.5
  reverse: sodiubirtsid sametsis
  word_count: 5
```

Servidor:

```
Servidor ouvindo em 127.0.0.1:5678
Cliente conectado: ('127.0.0.1', 58894)
Requisicao: {'operations': [{'op': 'add', 'args': [2, 3]}, {'op': 'divide', 'args': [10, 4]}, {'op': 'reverse', 'args': ['sistemas distribuidos']}, {'op': 'word_count', 'args': ['cliente e servidor trocam mensagens']}]}
Resposta:   {'results': [{'op': 'add', 'result': 5}, {'op': 'divide', 'result': 2.5}, {'op': 'reverse', 'result': 'sodiubirtsid sametsis'}, {'op': 'word_count', 'result': 5}]}
Cliente desconectado: ('127.0.0.1', 58894)
```

Lote com erros (`python3 client.py -i`), mostrando que as operações válidas continuam
respondendo normalmente:

```
> add 40 2
> divide 1 0
> foo 1
> reverse "ola mundo"
>
Enviado: {"operations": [{"op": "add", "args": [40, 2]}, {"op": "divide", "args": [1, 0]}, {"op": "foo", "args": [1]}, {"op": "reverse", "args": ["ola mundo"]}]}
Recebido:
  add: 42
  divide: ERRO: divisao por zero
  foo: ERRO: operacao desconhecida
  reverse: odnum alo
```

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `constCS.py` | host e porta |
| `protocol.py` | `send_json` / `recv_json` — envio e leitura das mensagens JSON |
| `server.py` | registro de operações, despacho das requisições e laço de conexões |
| `client.py` | lote de demonstração e modo interativo |

O servidor atende um cliente por vez e volta a aceitar novas conexões quando o
cliente atual se desconecta. Requisições inválidas (JSON malformado, operação
desconhecida, argumentos errados, divisão por zero) são respondidas como erro,
sem derrubar o servidor.
