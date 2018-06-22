# psimbols

Secure network message processor.

Most secure communications systems require a considerable amount of
configuration in both the clients and the servers. If you have a lot
of clients and servers, then that can be a lot of effort, which
also leads to a big disincentive to change anything once you have it
working.

This project is an exploration of whether you can put minimal configuration
into the clients and let the servers provide dynamic communications channels
on request. If there are a lot of clients, compared to the number of servers,
then minimising the work at the client end could save a lot of time.

## running the tests

The code requires at least python 3.2 and pycrypto 2.6.1
```
bin/test_psimbols.sh
```

If the tests all pass you have the right dependencies.

## channel creation

One way to uniquely identify a client is with its public key from a PKI
system like RSA. The public + private key can be installed in a client
and unlike a username + password pair the same public key can be used for
all the servers that it wants to talk to. Also, the safe lifespan of a PKI
key is years, compared to weeks or months for a basic password.

A client can send a message to a server to request a comms channel:
```json
{
  "public_key": {
    "type": "RSA",
    "data": "123456789012345678901234567890"
  },
  "request": "aa11bb22cc33dd44ee55ff66gg77hh88ii"
}
```

There is nothing secret here. The public key is public. So we can send
this message over an insecure channel like HTTP or on a message queue.

An important point is that the client encrypts the "request" field
with its *private* key. This can be decrypted by anyone with the public key,
so it is not secret. But it can only have been created by the owner of the
private key, so it proves that the client is legitimate and not someone who
has only copied the public key.

At this point the server has a choice. It can either create a channel
whatever the public key is (an open service). Or it can reject requests
that are not from pre-registered public keys (a closed service).

I am not going to make key registration part of this project. There are
lots of ways to do that. I will probably hand install the keys from my
test clients into my test servers and use only "closed services" because
that enables mitigation against man-in-the-middle attacks as explained below.

If the server decides the public key is acceptable, then it decrypts the
request and sees something like:
```json
{
  "channel_types": ["AES", "DES"],
  "request_salt": "something to make every request unique"
}
```

This tells the server which symmetric cipher algorithms are supported by
the client. If there is a sufficiently strong algorithm that the server
also supports, then it creates a comms channel and sends back a message:
```json
{
  "source": "http://psimbols.example.com:9393/",
  "response": "12345698888888888"
}
```

The "response" field is encrypted with the public key that was sent in
the channel request message. Therefore only the client with the matching
private key can decrypt the response string.

When the client decrypts the "response" field it can see the channel
configuration:
```json
{
  "channel": "123",
  "key": {
    "type": "AES",
    "data": "987"
  },
  "valid_until": "2018-09-09T00:00Z",
  "signature": "123456789987654321"
}
```

The "channel" field could be the same as the public key. Or it could be
a shortened version of it. The server knows all the currently active
channel identifiers so it can guarantee uniqueness.

The "key" is a shared secret between the server and client. A symmetric key
cipher typically needs a much shorter key than PKI and the encryption +
decryption is faster.

The channel may also have a nominal expiry time. And other properties. All
of this information is known only to the server and this particular client.

Finally the server adds a "signature" field which is encrypted with its
own *private* key. This enables the client to validate that the server is
who it thinks it is and not a man-in-the-middle. But this can *only* be
done if the client has the public key of the server. So this protection
mostly applies to a "closed service" - when the client's public key is
resistered with the server we also get the server's public key for the
client configuration.

## making a request

When the client wants to communicate securely it can now send a message
to the server over the channel that was dynamically created above:
```json
{
  "channel": "123",
  "request": "abcdefghijklmnopqrstuvwxyz"
}
```

Remember that the "channel" identifier is derived from the public key and
acts only as a proxy for it. It can be treated as public and is used to
identify the client to the server.

The "request" field is encrypted with the shared channel key. So, even
though someone else might send a message with the same "channel" identifier,
because it is public and easily copied, only the legitimate client can
send a message that decrypts into something valid.

## sending a response

On receipt of a valid request the server responds with a message:
```json
{
  "source": "http://psimbols.example.com:9393/",
  "channel": "123",
  "response": "abcdefghijklmnopqrstuvwxyz"
}
```

The "response" field is also encrypted with the shared channel key. So only
the legitimate client can decrypt it.

## channel expiry

A comms channel can be 'expired' at any time by either the server or the
client.

If the server expires the channel then the client finds out because its
requests are rejected with an 'unauthorised' response. Alternatively, if
the client is making regular requests, then the server may insert warnings
into responses that the channel is about to expire. 

If the client loses the channel data (because it has no persistence and
gets restarted, say) then it can simply request a new channel.

Obviously there will be limits on channel expiry. Because very frequent
expiry suggests that something bad is happening. In extreme circumstances
the server may block a client completely with a 'forbidden' response.
