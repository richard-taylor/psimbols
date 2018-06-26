# psimbols

Secure network message processor.

A small python server than can receive an encrypted request, decode it,
execute the predefined function and return an encrypted response.

## running the tests

The code was written for python 3.5.2 and pyaes 1.6.1
```
bin/test_psimbols.sh
```

If all the tests pass you have compatible dependencies.

## configuration

Each server has a shared symmetric key (for example AES) with each of
its registered clients. The client configuration for a given server is
something like:
```json
{
  "client": "123",
  "server": "http://psimbols.example.com:9393/",
  "key": {
    "type": "AES",
    "mode": "CBC",
    "data": "12345678901234567890123456789012"
  }
}
```

Here "client" is the name that uniquely identifies the client to the server.
The "server" field is the endpoint to connect to. And the "key" field is the
actual symmetric encryption key - the shared secret.

## making a request

When a client wants to communicate securely it can send a message
to the server via the configured endpoint:
```json
{
  "client": "123",
  "server": "http://psimbols.example.com:9393/",
  "request": "12345698888888888999999999999999999999999999999900000010101011"
}
```

The "request" field is encrypted with the shared key. So, even
though someone else might send a message with the same "client" identifier,
because it might be sniffed on the wire, only the legitimate client can
send a message that decrypts into something valid.

The decrypted request will look something like:
```json
{
  "request_id": "789",
  "run": {
    "module": "supermath",
    "function": "factorial",
    "params": {
      "n": 3
    }
  }
}
```

The "request_id" is useful if the client is making asynchronous requests
and needs to tie the response to the right question.

The main body of the request is the "run" field which describes a
predefined function at the server and the parameters that should be
passed to it.

## sending a response

On receipt of a valid request that results in a valid output, the server
responds with a message:
```json
{
  "client": "123",
  "server": "http://psimbols.example.com:9393/",
  "response": "1234569888888888815515118882828389949958800803485998449494"
}
```

The "response" field is also encrypted with the shared key. So only
the legitimate client can decrypt it.

The decrypted response will look something like:
```json
{
  "request_id": "789",
  "return": {
    "value": 6,
    "comment": "3! = 6"
  }
}
```

The "request_id" is the same value that the client sent in the request.

The main body of the response is the "return" field which describes the
output of the server function given the request parameters.

## rate limiting

Each client is only allowed a certain number of requests per hour.
When a client exceeds its limit the server rejects further requests
with a 'too many requests' response.
