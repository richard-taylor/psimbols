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
  "request": "new channel"
}
```

There is nothing secret here. The public key is public. So we can send
this message over an insecure channel like HTTP or on a message queue.

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
a channel challenge message:
```json
{
  "channel_types": ["AES", "DES"],
  "challenge_question": "something to do"
}
```

This challenge message has two purposes. Firstly it tells the client which
symmetric cipher algorithms are supported. And secondly it provides a test
that can only be passed by the legitimate owner of the public key. Since
anyone can know the public key we don't want bad actors to be able to
disrupt existing channels by creating new channels.

There is then a limited time window in which the client can respond with a
channel confirmation message:
```json
{
  "public_key": {
    "type": "RSA",
    "data": "123456789012345678901234567890"
  },
  "request": "abcdefghijklmnopqrstuvwxyz"
}
```

The important point here is that the client encrypts the request with its
*private* key. This can be decrypted by anyone with the public key, so it is
not secret. But it can only have been created by the owner of the private
key, so it proves that the client is legitimate and not someone who has only
copied the public key.

When the server decrypts the message with the public key it sees the message:
```json
{
  "channel_type": "AES",
  "challenge_solution": "the answer"
}
```

As long as the message decrypts properly and the challenge is answered
correctly, the server will create a new comms channel and respond with
a message:
```json
{
  "source": "http://psimbols.example.com:9393/",
  "response": "abcdefghijklmnopqrstuvwxyz"
}

```

The "response" is encrypted with the client's public key, so it can be
decrypted with the private key to see the final channel configuration:
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
cipher typically needs a much shorter key than PKI and the encryption +
decryption is faster.

The channel may also have a nominal expiry time. And other properties. All
of this information is known only to the server and this particular client.

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
expiry suggests that something bad is happening.

## man in the middle attacks

Without a trusted third party there is a risk that a bad actor could
insert themselves between a client and server. Pretending to be one to
the other it could read all the messages on the channels created.

This can only happen if *all* the communications between client and server
are intercepted by the man in the middle. So, in the same way that I am
not going to investigate public key distribution yet, I will also say that
man-in-the-middle attacks can be defeated by having additional communication
paths over which the owner of a client can check that their requests are
being processed by the server and not someone else.

For example, if the server has a completely separate portal which can
show the owner of a registered public key how many requests they have
made. Then that will show no requests against my public key if I am being
attacked; because all my requests are being intercepted and replaced by
the attackers requests. From the server's point of view I am not using it
at all, the attacker is.
