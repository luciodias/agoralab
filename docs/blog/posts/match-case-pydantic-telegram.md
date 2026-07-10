---
date:
  created: 2026-07-09
readtime: 10
categories:
  - Python 
tags:
  - python
  - pydantic
  - match-case
  - telegram
  - padrões
authors:
  - luciodias
slug: match-case-pydantic-com-telegram
---

# Match/case de modelos Pydantic de forma pytônica

Pattern matching (`match/case`) chegou no Python 3.10 e, combinado com Pydantic, dá um código limpo e expressivo para rotear diferentes tipos de mensagem.

<!-- more -->

## Consumindo a API do Telegram

A API do Telegram devolve objetos JSON com uma estrutura que varia conforme o tipo de mensagem. Uma chamada a `getUpdates` retorna algo assim:

```python
import httpx

TOKEN = "seu-token"
resp = httpx.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
data = resp.json()

for result in data["result"]:
    message = result["message"]
    print(message.keys())  # varia conforme o tipo
```

Um texto vem com a chave `text`. Uma foto vem com `photo` (uma lista). Um documento vem com `document` (um dict). Um áudio com `audio`. E por aí vai.

Sem tipagem, tratar cada caso exige várias checagens manuais:

```python
if "text" in message:
    print(f"Texto: {message['text']}")
elif "photo" in message:
    print(f"Foto: {message['photo'][-1]['file_id']}")
elif "document" in message:
    print(f"Documento: {message['document']['file_name']}")
```

Funciona, mas é frágil, repetitivo e nada pytônico.

## O que é Pydantic

Pydantic é uma biblioteca de validação de dados que usa type hints do Python para definir a forma dos dados. Com ela, você declara classes que são validadas e convertidas automaticamente:

```python
from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: int
    nome: str
    email: Optional[str] = None

user = Usuario(id=1, nome="Lúcio", email="lucio@exemplo.com")
print(user.model_dump())
# {'id': 1, 'nome': 'Lúcio', 'email': 'lucio@exemplo.com'}
```

Se os dados vierem de um JSON, o Pydantic faz a conversão e validação na hora:

```python
raw = {"id": "42", "nome": "Lúcio"}  # id veio como string
user = Usuario.model_validate(raw)
print(user.id)       # 42 (convertido para int)
print(type(user.id)) # <class 'int'>
```

Isso é poderoso: você garante que os dados estão no formato esperado antes de usá-los.

## Modelando a Message do Telegram

Vamos modelar o objeto `Message` do Telegram com Pydantic. A mensagem pode ser de texto, foto, documento, áudio, vídeo, sticker, etc. Cada tipo tem campos opcionais específicos:

```python
from pydantic import BaseModel
from typing import Optional

class PhotoSize(BaseModel):
    file_id: str
    width: int
    height: int

class Document(BaseModel):
    file_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

class Audio(BaseModel):
    file_id: str
    duration: int
    title: Optional[str] = None

class Message(BaseModel):
    message_id: int
    text: Optional[str] = None
    photo: Optional[list[PhotoSize]] = None
    document: Optional[Document] = None
    audio: Optional[Audio] = None
    # Outros campos: video, sticker, voice, etc.
```

Agora, ao invés de acessar `message["text"]` e torcer para existir, você usa um objeto tipado e validado:

```python
msg = Message.model_validate(raw_message)
```

A `Message` real do Telegram tem dezenas de outros campos (`chat`, `date`, `from`, `entities`...). O Pydantic ignora campos extras por padrão (`extra="ignore"`), então `model_validate` não quebra com um payload completo — ele só preenche o que declaramos.

## Match/case de forma pytônica

Com os modelos definidos, o pattern matching do Python entra em cena. A sintaxe `match`/`case` permite desestruturar o objeto e casar com base nos campos presentes:

```python
def handle(msg: Message) -> str:
    match msg:
        case Message(text=str() as texto):
            return f"Texto: {texto[:50]}"
        case Message(photo=list() as fotos):
            file_id = fotos[-1].file_id
            return f"Foto: {file_id}"
        case Message(document=Document() as doc):
            return f"Documento: {doc.file_name or 'sem nome'}"
        case Message(audio=Audio() as a):
            return f"Áudio: {a.duration}s - {a.title or 'sem título'}"
        case _:
            return "Tipo não suportado"
```

Cada `case` testa se o campo relevante está presente e, se estiver, extrai o valor numa variável. O `_` no último caso funciona como coringa.

A mágica está no `str()` e `list()` dentro dos padrões: eles casam **qualquer** string ou lista, respectivamente. E `Document()` casa com qualquer instância válida de `Document`. O Python testa se o campo existe e tem o tipo esperado.

Se usássemos um capture simples como `case Message(text=txt)`, o padrão casaria mesmo quando `text` é `None` — afinal `txt` aceita qualquer valor. Por isso usamos `str()` no subpadrão: ele só casa quando o campo é de fato uma string.

### Exemplo completo

Juntando tudo num fluxo real:

```python
import httpx
from pydantic import BaseModel, ValidationError
from typing import Optional

# --- Modelos ---

class PhotoSize(BaseModel):
    file_id: str
    width: int
    height: int

class Document(BaseModel):
    file_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

class Audio(BaseModel):
    file_id: str
    duration: int
    title: Optional[str] = None

class Message(BaseModel):
    message_id: int
    text: Optional[str] = None
    photo: Optional[list[PhotoSize]] = None
    document: Optional[Document] = None
    audio: Optional[Audio] = None

# --- Roteador com match/case ---

def processar(msg: Message) -> str:
    match msg:
        case Message(text=str() as t):
            return f"📝 {t[:100]}"
        case Message(photo=list() as p):
            return f"🖼️ {p[-1].file_id}"
        case Message(document=Document() as d):
            return f"📄 {d.file_name or 'arquivo'}"
        case Message(audio=Audio() as a):
            title = a.title or "áudio"
            return f"🎵 {title} ({a.duration}s)"
        case _:
            return "❓ tipo desconhecido"

# --- Consumo da API ---

TOKEN = "seu-token"
resp = httpx.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")

for result in resp.json()["result"]:
    try:
        msg = Message.model_validate(result["message"])
        print(processar(msg))
    except ValidationError as e:
        print(f"Erro ao validar: {e}")
```

### Por que isso é pytônico

O `match`/`case` com Pydantic segue os princípios do Python por vários motivos:

- **Legibilidade** — Cada tipo de mensagem é tratado numa linha clara e auto-documentada
- **Segurança** — O Pydantic valida os dados na entrada; o `case` só casa se o campo existir
- **Extensibilidade** — Adicionar um novo tipo de mensagem é só criar o modelo e mais um `case`
- **Validação em tempo de construção** — O Pydantic valida os tipos ao instanciar o modelo, falhando cedo em vez de quebrar em runtime

Sem Pydantic, você teria que fazer algo como:

```python
match raw:
    case {"text": str() as t}:
        ...
    case {"photo": [_, *_] as p}:
        ...
```

Funciona, mas perde a validação de tipos aninhados e a documentação explícita dos campos. Com Pydantic, o modelo já documenta a estrutura esperada.

### Variante com modelos distintos

Dá para ir além: em vez de um único `Message` com campos opcionais, modele cada tipo como uma classe separada e use um `Union` para representar a mensagem:

```python
from typing import Union

class TextMessage(BaseModel):
    message_id: int
    text: str

class PhotoMessage(BaseModel):
    message_id: int
    photo: list[PhotoSize]

class DocumentMessage(BaseModel):
    message_id: int
    document: Document

MessageUnion = Union[TextMessage, PhotoMessage, DocumentMessage]
```

Para fazer o parsing, um `match` no dict cru seleciona o modelo certo:

```python
def parse(raw: dict) -> MessageUnion:
    match raw:
        case {"text": str()}:
            return TextMessage.model_validate(raw)
        case {"photo": list()}:
            return PhotoMessage.model_validate(raw)
        case {"document": dict()}:
            return DocumentMessage.model_validate(raw)
```

Aí o `match` final roteia por classe:

```python
match parse(raw):
    case TextMessage(text=t):
        print(f"Texto: {t}")
    case PhotoMessage(photo=p):
        print(f"Foto: {p[-1].file_id}")
    case DocumentMessage(document=d):
        print(f"Documento: {d.file_name}")
```

Nessa abordagem, cada modelo só expõe os campos relevantes para aquele tipo, e o `match`/`case` dispensa subpadrões como `str()` — o simples casamento de classe já basta. A desvantagem é que você precisa de um parsing explícito para separar os tipos antes de rotear.

## Conclusão

Pydantic + `match`/`case` formam uma dupla natural para processar dados estruturados com variações de formato. A API do Telegram é um ótimo exemplo por ter múltiplos tipos de mensagem com campos opcionais, mas o padrão se aplica a qualquer API que retorne JSON.

Se você ainda usa cadeias de `if`/`elif` para inspecionar dicts, experimente essa combinação. O código fica mais declarativo, mais seguro e mais pythônico.
