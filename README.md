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
then minimising the work at the client end could save a lot of work.

## running the tests

```
bin/test_psimbols.sh
```

## channel creation

One way to uniquely identify a client is with its public key from a PKI
system like RSA. The public + private key can be configured into a client
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
  "channel_types": ["AES", "DES"]
}
```

There is nothing very secret here. The public key is public. The list of
acceptable channel encryption types is arguably not... but lets try and
live with that for now.

At this point the server has a choice. It can either create a channel
whatever the public key is (an open service). Or it can reject requests
that are not from pre-registered public keys (a closed service).

I am not going to make key registration part of this project. There are
lots of ways to do that. And I will probably hand install the keys from
my test clients into my test servers.

If the server decides the public key is acceptable, then it sends back
a message:
```json
{
  "source": "http://psimbols.example.com:9393/",
  "response": "12345698888888888"
}
```

The "response" field is encrypted with the public key that was sent in
the channel request message. Therefore only the client with the matching
private key can decrypt the response string.

When the client decrypts the response with its private key, it becomes
a channel description message:
```json
{
  "channel": "123",
  "key": {
    "type": "AES",
    "data": "987"
  },
  "valid_until": "2018-09-09T00:00Z"
}
```

The "channel" field could be the same as the public key. Or it could be
a shortened version of it. The server knows all the currently active
channel identifiers so it can guarantee uniqueness.

The "key" is a shared secret between the server and client. A symmetric key
cypher typically needs a much shorter key than PKI.

The channel may also have a nominal expiry time. And other properties. All
of this information is known only to the server and this particular client.

Remember that the "channel" identifier is derived from the public key and
acts only as a proxy for it. It can be treated as public and is used to
identify the client to the server.

## making a request

When the client wants to send a message to the server:
```json
{
  "channel": "123",
  "request": "abcdefghijklmnopqrstuvwxyz"
}
```

The "request" field is encrypted with the shared channel key. So, even
though someone else might send a message with the same "channel" identifier,
because it is public and easily copied, only the legitimate client can
send a message that decrypts into something valid.

## sending a response

On receipt of a valid request the server responds with a message:
```
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
requests are rejected with an 'unauthorised' response.

If the client loses the channel data (because it has no persistence and
gets restarted, say) then it can simply request a new channel.

This is where we need to be careful and think about malicious actors.
For example, what if a bad actor sends a channel request with someone
else's public key? We do not want the server to delete the current
channel until it is sure that the new channel is to the genuine owner
of the public key.

Maybe this is confirmation that the channel creation negotiation should
have more steps? We probably do not have to expose that "channel_types"
field to public view after all... THINK ABOUT THIS SOME MORE.
