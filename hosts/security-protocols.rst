.. Copyright |copy| 2015, 2019, 2025 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


******************
Security protocols
******************

.. todo: brief introduction


.. _Remote login:

.. index:: telnet
   
One of the initial motivations for building computer networks was
to allow users to access remote computers over the networks. In the 1960s
and 1970s, the mainframes and the emerging minicomputers were composed
of a central unit and a set of terminals connected through serial
lines or modems. The simplest protocol that was designed to access
remote computers over a network is probably :term:`telnet` :rfc:`854`.
:term:`telnet` runs over TCP and a telnet server listens on port `23` by
default. The TCP connection used by telnet is bidirectional, both the client
and the server can send data over it. The data exchanged over such a
connection is essentially the characters that are typed by the user on the
client machine and the text output of the processes running on the server
machine with a few exceptions (e.g. control characters, characters to control
the terminal like VT-100, ...) . The default character set for
telnet is the ASCII character set, but the extensions specified
in :rfc:`5198` support the utilization
of Unicode characters.

From a security viewpoint, the main drawback of :term:`telnet` is that all
the information, including the usernames, passwords and commands,
is sent in cleartext over a TCP connection. This implies that
an eavesdropper could easily capture the passwords used by anyone
on an unprotected network. Various software tools exist to
automate this collection of information. For this reason,
:term:`telnet` is rarely used today to access remote computers.
It is usually replaced by :term:`ssh` or similar protocols.

.. index:: ssh

The secure shell (ssh)
======================

.. spelling::

   Ylonen

The secure shell protocol was designed in the mid 1990s by T. Ylonen
to counter the eavesdropping attacks against :term:`telnet` and
similar protocols [Ylonen1996]_. :term:`ssh` became quickly popular and system
administrators encouraged its usage. The original version of :term:`ssh`
was freely available. After a few years, his author created a company
to distribute it commercially, but other programmers continued to
develop an open-source version of :term:`ssh` called
`OpenSSH <http://www.openssh.com>`_.
Over the years, :term:`ssh` evolved
and became a flexible applicable whose usage extends beyond remote
login to support features such as file transfers, protocol tunneling, ...
In this section, we only discuss the basic features of :term:`ssh` and explain
how it differs from :term:`telnet`. Entire books have been written to describe
:term:`ssh` in details [BS2005]_. An overview of the protocol
appeared in [Stallings2009]_.

The :term:`ssh` protocol runs directly above the TCP protocol.
Once the TCP bytestream
has been established, the client and the server exchange messages. The
first message exchanged is an ASCII line that announces the version of the
protocol and the version of the software implementation used by the client
and the server. These two lines are useful when debugging interoperability
problems and other issues.

The next message is the ``SSH_MSG_KEX_INIT`` message that is used
to negotiate the cryptographic algorithms that will be used for the
``ssh`` session. It is very important for security protocols to
include mechanisms that enable a negotiation of the cryptographic
algorithms that are used. First, these
algorithms provide different levels of security. Some algorithms might
be considered totally secure and are recommended today while they could
become deprecated a few years later after the publication of some
attacks. Second, these algorithms provide different levels of
performance and have different CPU and memory impacts.

In practice, an ``ssh`` implementation supports four types of
cryptographic algorithms :

 - key exchange
 - encryption
 - Message Authentication Code (MAC)
 - compression

The IANA_ maintains a `list of the cryptographic algorithms <http://www.iana.org/assignments/ssh-parameters/ssh-parameters.xhtml#ssh-parameters-16>`_
that can be used by ``ssh`` implementations. For each type of algorithm,
the client provides an ordered list of the algorithms that it supports
and agrees to use. The server compares the received list with its own list.
The outcome of the negotiation is a set of four algorithms [#fnull]_
that will be combined for this session.

  .. msc::

      a [label="", linecolour=white],
      b [label="Client",linecolour=black],
      z [label="", linecolour=white],
      c [label="Server", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "" ] ,
      b>>c [ label = "SSH-clientP-clientS comments", arcskip="1"];
      c=>d [ label = "" ];

      d=>c [ label = "" ] ,
      c>>b [ label = "SSH-serverP-serverS comments", arcskip="1"];
      b=>a [ label = "" ];

      a=>b [ label = "" ] ,
      b>>c [ label = "SSH_MSG_KEX_INIT", arcskip="1"];
      c=>d [ label = "" ];

      d=>c [ label = "" ] ,
      c>>b [ label = "SSH_MSG_KEX_INIT", arcskip="1"];
      b=>a [ label = "" ];


This negotiation of the cryptographic algorithms allows the implementations
to evolve when new algorithms are proposed. If a client is upgraded, it can
announce a new algorithm as its preferred one even if the server is not
yet upgraded.

.. spelling::

   Diffie
   Hellman

Once the cryptographic algorithms have been negotiated, the key exchange algorithm is
used to negotiate a secret key that will be shared by the client and the server.
These key exchange algorithms include some variations over
the basic algorithms. As an example, let us analyze how the
Diffie-Hellman key exchange algorithm is used within the
``ssh`` protocol. In this case, each host has both a private and a public key.  (Note that
:math:`g` is a generator for the subgroup of the Galois field of order :math:`p`, where
:math:`p` is a prime number, and || is the concatenation operator.  For additional background
information, see [Schneier1996]_.)

 - the client generates the random number :math:`a` and sends
   :math:`A=g^{a} \mod p` to the server
 - the server generates the random number :math:`b`. It then computes
   :math:`B=g^{b} \mod p`, :math:`K=B^{a} \mod p` and signs with its private
   key :math:`hash(V_{Client} || V_{Server} || KEX\_INIT_{Client} || KEX\_INIT_{Server} || Server_{pub} || A || B || K )`
   where :math:`V_{Server}` (resp. :math:`V_{Client}`) is the initial
   messages sent by the client (resp. server), :math:`KEX\_INIT_{Client}`
   (resp.  :math:`KEX\_INIT_{Server}`) is the key exchange message sent by
   the client (resp. server) and :math:`A`, :math:`B` and :math:`K` are the
   messages of the Diffie-Hellman key exchange
 - the client can recompute :math:`K=A^{b} \mod p` and verify the
   signature provided by the server

This is a slightly modified authenticated Diffie-Hellman key exchange
with two interesting points. The first point is that
when the server authenticates the key exchange it does not provide a
certificate. This is because ``ssh`` assumes that the client will store
inside its cache the public key of the servers that it uses on a
regular basis. This assumption is valid for a protocol like ``ssh``
because users typically use it to interact with a small number of
servers, typically a few or a few tens. Storing this information does
not require a lot of storage. In practice, most ``ssh`` clients will
accept to connect to remote servers without knowing their public key before
the connection. In this case, the client issues a warning to the user who
can decide to accept or reject the key. This warning can be associated
with a fingerprint of the key, either as a sequence of letters or as
an ASCII art which can be posted on the web or elsewhere [#fdnsssh]_ by the
system administrator of the server. If a client connects to a server
whose public key does not match the stored one, a stronger warning is
issued because this could indicate a man-in-the-middle attack or that
the remote server has been compromised. It can also indicate that the server
has been upgraded and that a new key has been generated during this upgrade.

.. index:: downgrade attack

The second point is that the server authenticates not only the result
of the Diffie-Hellman exchange but also a hash of all the information
sent and received during the exchange. This is important to prevent
`downgrade attacks`. A `downgrade attack` is an attack where an
active attacker modifies the messages sent by the communicating hosts
(typically the client) to request the utilization of weaker encryption
algorithms. Consider a client that supports two encryption schemes. The
preferred one uses 128 bits secret keys and the second one is an old
encryption scheme that uses 48 bits keys. This second algorithm is
kept for backward compatibility with older implementations. If an attacker
can remove the preferred algorithm from the list of encryption algorithms
supported by the client, he can force the server to use a weaker
encryption scheme that will be easier to break. Thanks
to the hash that covers all the messages exchanged by the server,
the downgrade attack cannot occur against ``ssh``. Algorithm agility is
a key requirement for security protocols that need to evolve when
encryption algorithms are broken by researchers. This agility cannot be
used without care and signing a hash of all the messages exchanged
is a technique that is frequently used to prevent downgrade attacks.

.. note:: Single use keys

   Thanks to the Diffie-Hellman key exchange, the client and the
   servers share key :math:`K`. A naive implementation would probably
   directly use this key for all the cryptographic algorithms that
   have been negotiated for this session. Like most security protocols,
   ``ssh`` does not directly use key :math:`K`. Instead, it uses
   the negotiated hash function with different parameters [#fsshkeys]_
   to allow the
   client and the servers to compute six keys from :math:`K` :

      - a key used by the client (resp. server) to encrypt the data that
        it sends
      - a key used by the client (resp. server) to authenticate the
        data that it sends
      - a key used by the client (resp. server) to initialize the
        negotiated encryption scheme (if required by this scheme)

   It is common practice among designers of security protocols to never
   use the same key for different purposes. For example, allowing the
   client and the server to use the same key to encrypt data could
   enable an attacker to launch a replay attack by sending to the
   client data that it has itself encrypted.


At this point, all the messages sent over the TCP connection will be encrypted
with the negotiated keys. The ``ssh`` protocol uses messages
that are encoded according to the Binary Packet Protocol defined in
:rfc:`4253`. Each of these messages contains the following information :

 - ``length`` : this is the length of the message in bytes, excluding the MAC
   and length fields
 - ``padding length`` : this is the number of random bytes that have been added
   at the end of the message.
 - ``payload`` : the data (after optional compression) passed by the user
 - ``padding`` : random bytes added in each message (at least four) to
   ensure that the message length is a multiple of the block size
   used by the negotiated encryption algorithm
 - ``MAC`` : this field is present if a Message Authentication Code has been
   negotiated for the session (in practice, using ``ssh`` without
   authentication is risky and this field should always be present). Note
   that to compute the MAC, an ``ssh`` implementation must maintain
   a message counter. This counter is incremented by one every time a
   message is sent and the MAC is computed with the negotiated authentication
   algorithm using the MAC key over the concatenation of
   the message counter and the cleartext message.
   The message counter is not transmitted,
   but the recipient can easily recover its value. The ``MAC`` is computed as
   :math:`mac = MAC(key, sequence\_number || unencrypted\_message)` where the
   key is the negotiated authentication key.

.. index:: HMAC

.. note:: Authenticating messages with HMAC

   `ssh` is one example of a protocol that uses Message Authentication Codes
   (MAC) to authenticates the messages that are sent. A naive implementation
   of such a MAC would be to simply use a hash function like SHA-1. However,
   such a construction would not be safe from a security viewpoint. Internet
   protocols usually rely on the HMAC construction defined in :rfc:`2104`.
   It works with any hash function (`H`) and a key (`K`). As an example, let
   us consider HMAC with the SHA-1 hash function. SHA-1 uses 20 bytes
   blocks and the block size will play an important role in the operation
   of HMAC. We first require the key to be as long as the block size. Since this
   key is the output of the key generation algorithm, this is one parameter
   of this algorithm.

   HMAC uses two padding strings : `ipad` (resp. `opad`)  which is a
   string containing 20 times byte ``0x36`` (resp. byte ``0x5C``). The HMAC
   is then computed as :math:`H[K \oplus opad, H(K \oplus ipad, data) ]`
   where :math:`\oplus` denotes the bitwise XOR operation. This computation
   has been shown to be stronger than the naive :math:`H(K,data)` against
   some types of cryptographic attacks.



Among the various features of the ``ssh`` protocol, it is interesting
to mention how users are authenticated by the server. The ``ssh`` protocol
supports the classical username/password authentication (but both
the username and the password are transmitted over the secure encrypted
channel). In addition, ``ssh`` supports two authentication mechanisms that
rely on public keys. To use the first one, each user needs to generate
his/her own public/private key pair and store the public key on the server.
To be authenticated, the user needs to sign a message containing his/her
public key by using his/her private key. The server can easily verify the
validity of the signature since it already knows the user's public key.
The second authentication scheme is designed for hosts that trust each
other. Each host has a public/private key pair and stores the public keys
of the other hosts that it trusts. This is typically used in environments
such as university labs where each user could access any of the available
computers. If Alice has logged on ``computer1`` and wants to execute a
command on ``computer2``, she can create an ``ssh`` session on this computer
and type (again) her password. With the host-based authentication scheme,
``computer1`` signs a message with its private key to confirm that
it has already authenticated Alice. ``computer2`` would then accept
Alice's session without asking for her credentials.

The ``ssh`` protocol includes other features that are beyond the
scope of this book. Additional details may be found in [BS2005]_.

.. todo: provide examples using kathara, telnet has not really been deployed with tls support although sume implementatons support it

.. _TLS:

Transport Layer Security
========================

.. index:: SSL

The Transport Layer Security family of protocols were initially
proposed under the name Secure Socket Layer (SSL). The first deployments
used this name and many researchers still refer to this security
protocol as SSL [FKC1996]_. In this chapter, we use the official name that was
standardized by the IETF: TLS for `Transport Layer Security`.

The TLS protocol was designed to be usable by a wide range of applications
that use the transport layer to reliably exchange information. TLS is mainly
used over the TCP protocol. There are variants of TLS that operate
over SCTP :rfc:`3436` or UDP :rfc:`6347`,
but these are outside the scope of  this chapter.

A TLS session operates over a TCP connection. TLS is responsible for the
encryption and the authentication of the SDUs exchanged by the application
layer protocol while TCP provides the reliable delivery of this encrypted
and authenticated bytestream. TLS is used by many different
application layer protocols. The most frequent ones are HTTP (HTTP over TLS
is called HTTPS), SMTP :rfc:`3207` or POP and IMAP :rfc:`2595`, but proprietary application-layer protocols also use TLS [AM2019]_.

A TLS session can be initiated in two different ways. First, the application
can use a dedicated TCP port number for application layer protocol x-over-TLS.
This is the solution used by many HTTP servers that reserve port :math:`443`
for HTTP over TLS. This solution works, but it requires to reserve two ports
for each application : one where the application-layer protocol is used
directly over TCP and another one where the application-layer protocol
is used over TLS. Given the limited number of TCP ports that are available,
this is not a scalable solution. The table below provides some of
the reserved port numbers for application layer protocols on top of TLS.

==================   ============  ==========
Application          TCP port      TLS port
==================   ============  ==========
POP3                 110           995
IMAP                 143           993
NNTP                 119           563
HTTP                 80            443
FTP                  21            990
==================   ============  ==========


A second approach to initiate a TLS session is to use the standard
TCP port number for the application layer protocol and define a special
message in this protocol to trigger the start of the
TLS session. This is the solution used for SMTP with the ``STARTTLS`` message.
This extension to SMTP :rfc:`3207` defines the new STARTTLS command.
The client can issue this command to indicate to the server that
it wants to start a TLS session as shown in the example below
captured during a session on port 25.


.. code-block:: console

          220 server.example.org ESMTP
          EHLO client.example.net
          250-server.example.org
          250-PIPELINING
          250-SIZE 250000000
          250-ETRN
          250-STARTTLS
          250-ENHANCEDSTATUSCODES
          250-8BITMIME
          250 DSN
          STARTTLS
          220 2.0.0 Ready to start TLS


In the remaining parts of this chapter, we assume that the TLS session
starts immediately after the establishment of the TCP connection. This
corresponds to the deployments on web servers. We focus our presentation
of TLS on this very popular use case. TLS is a complex protocol that
supports other features than the one used by web servers. A more detailed
presentation of TLS may be found in [KPS2002]_ and [Ristic2015]_.

A TLS session is divided in two phases: the handshake and the data transfer.
During the handshake, the client
and the server negotiate the security parameters and the keys that will
be used to secure the data transfer. During the second phase, all the messages
exchanged are encrypted and authenticated with the negotiated algorithms
and keys.


The TLS handshake
-----------------

When used to interact with a regular web server, the TLS handshake has
three important objectives:

 1. Securely negotiate the cryptographic algorithms that will be used by the
    client and the server over the TLS session
 2. Verify that the client interacts with a valid server
 3. Securely agree on the keys that will be used to encrypt and authenticate
    the messages exchanged over the TLS session


The TLS handshake is a four-way handshake illustrated in the figure below.

  .. msc::

      a [label="", linecolour=white],
      b [label="Client",linecolour=black],
      z [label="", linecolour=white],
      c [label="Server", linecolour=black],
      d [label="", linecolour=white];

      b>>c [ label = "ClientHello[Random]", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "ServerHello[Random], Certificate", arcskip="2"];
      |||;
      |||;
      b>>c [ label = "E(K,MasterSecret), Finished=MAC(MasterSecret||Handshake)", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "Finished=MAC(MasterSecret||Handshake)", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "Encrypted Record", linecolour="red", textcolour="red"];
      b>>c [ label = "Encrypted Record", linecolour="red", textcolour="red"];

In a nutshell, the client starts the TLS handshake by proposing a random nonce. The server replies with its random nonce and a certificate that binds its name to a public key. The client generates a MasterSecret that will be used later to derive the session keys and encrypts it with the public key of the server. It also generates a `Finished` message that contains a MAC of all the messages exchanged to allow the server to detect any modification of the messages sent by the client. The server also sends its own `Finished` message. At that point, the client and the server sent encrypted records thanks to the keys derived from the MasterSecret.



.. spelling::

   cryptanalysts

.. index:: TLS ClientHello

Let us first discuss the negotiation of the cryptographic algorithms and
parameters. Like all security protocols, TLS includes some agility in its
design since new cryptographic algorithms appear over the years and
some older algorithms become deprecated once cryptanalysts find flaws.
The TLS handshakes starts with the ``ClientHello`` message
that is sent by the client. This message carries the following information :

 - `Protocol version number`: this is the version of the TLS protocol supported
   by the client. The server should use the same version of the TLS protocol as
   the client, but may opt for an older version. Both versions 1.2 and 1.3 of TLS are deployed today. Older versions are being deprecated.
 - `Random number`: security protocols rely on random numbers. The client
   sends a 32 bytes long random number where usually four of these bytes
   correspond
   to the client's clock. This random number is used, together with the
   server's random number, as a seed to generate the security keys.
 - `Cipher suites` : this ordered list contains the set of cryptographic
   algorithms that are supported by the client, with the most preferred one
   listed first. In contrast with ``ssh`` that allows negotiating independent
   algorithms for encryption, key exchange and authentication, TLS relies on
   suites that combine these algorithms together. Many cryptographic suites
   have been defined for TLS. Various recommendations
   have been published on the security of some of these suites :rfc:`7525`.
 - `Compression algorithm` : the client may propose the utilization of a
   specific compression algorithm (e.g. zlib). In theory, compressing the data
   before encrypting it is an intelligent way to reduce the amount of data
   exchanged. Unfortunately, its implementation in TLS has caused several security problems [PHG2013]_. For
   this reason, compression is usually disabled in TLS :rfc:`7525`.
 - `Extensions` : TLS supports various extensions in the ``ClientHello``
   message. These extensions :rfc:`6066` are important to allow the protocol
   to evolve, but many of them go beyond the scope of this chapter.

.. index:: TLS SNI

.. note:: The ``Server Name Indication (SNI)``

   The ``Server Name Indication (SNI)`` extension defined in :rfc:`6066`
   is an important TLS extension for web servers.
   It is used by the client to indicate the name of the server
   that it wishes to contact. The IP address associated to this name
   has been queried from the DNS and used to establish the TCP connection.
   Why should the client indicate the server name in the TLS
   ``ClientHello`` ?  The motivation is the same as for the ``Host``
   header line in HTTP/1.0. With the SNI extension, a single TLS server
   can support several web sites that use different domain names. Thanks
   to the SNI extension, the server knows the concerned domain name at
   the start of the TLS session. Without this extension, hosting providers
   would have been forced use one IP address per TLS-enabled server.

.. index:: TLS ServerHello, TLS Certificate

The server replies to the ``ClientHello`` with several messages:

 - the ``ServerHello`` message that contains the protocol version chosen by
   the server (assumed to be the same as the client version in this chapter),
   the 32 random bytes chosen by the server, the `Cipher Suite` selected by
   the server from the list advertised by the client
   and a `Session Id`. This `Session Id` is an identifier which
   is chosen by the server. It identifies the TLS session and the
   security parameters (algorithms and keys) negotiated for this session.
   It is used to support session resumption.
 - the ``Certificate`` message provides the certificate (or usually a chain of
   certificates) that binds a domain name to the public key used by
   the server. TLS uses the server certificates
   to authenticate the server. It relies on a Public Key Infrastructure that
   is composed of a set of root certification authorities that
   issue certificates to certification authorities that in the end
   issue certificates to servers. TLS clients are usually configured with
   the public keys of several root certification authorities and use
   this information to validate the certificates that they receive from
   servers. For historical reasons, the TLS certificates are encoded
   in ASN.1 format. The details of the ASN.1 syntax [Dubuisson2000]_
   are outside the scope of this book.
 - the ``ServerKeyExchange`` message is used by the server to transmit the
   information that is required to perform the key exchange. The content
   of this message is function of the selected key exchange algorithm.
 - the ``ServerHelloDone`` indicates that the server has sent all the messages
   for the first phase of the handshake.

.. index:: TLS Key exchange

At this point, it is time to describe the TLS key exchange. TLS supports
different key exchange mechanisms that can be negotiated as part of the
selection of the cipher suite. We focus on two of them to highlight
their differences:

 - ``RSA``. This key exchange algorithm uses the encryption capabilities of
   the RSA public-key algorithm. The client has validated the server's
   public key thanks to the ``Certificate`` message. It then generates
   a (48 bytes) random number, encrypts it with the server public key
   and sends the encrypted number to the server in the ``ClientKeyExchange``
   message. The server uses its private key to decrypt the random
   number. At this point, the client and the server share the same
   (48 bytes long) secret and use it to derive the secret keys required
   to encrypt and authenticate data in the second phase. With this
   key exchange algorithm, the server does not need to send a
   ``ServerKeyExchange`` message.
 - ``DHE_RSA``. This key exchange algorithm is the Ephemeral Diffie Hellman
   key exchange with RSA signatures to authenticate the key exchange. It
   operates as a classical authenticated Diffie Hellman key exchange.
   If this key exchange
   has been selected by the server, it sends its Diffie Hellman parameters
   in the ``ServerKeyExchange`` message and signs them with its private
   key. The client then continues the key exchange and sends the results of
   its own computation in the ``ClientKeyExchange`` message. ``DHE_RSA``
   is thus an authenticated Diffie Hellman key exchange where the initial
   message is sent by the server (instead of the client as in our first example
   but since the protocol is symmetric, this does not matter).

.. index:: Perfect Forward Secrecy

An important difference between ``DHE_RSA`` and ``RSA`` is their reaction
against attacks. ``DHE_RSA`` is considered by many to be stronger than ``RSA``
because it supports `Perfect Forward Secrecy`. This property is important
against attackers that are able to eavesdrop all the (encrypted) data
sent and received by a server. Consider that Terrence is such an attacker
that has stored all the packets exchanged by Bob's server during the last
six months. If he manages, by any means, to obtain Bob's private key, he
will be able to decrypt all the keys used to secure the TLS sessions with
Bob's server during this period. With ``DHE_RSA``, a similar attack is
less devastating. If Terrence knows Bob's private key, he will be able to launch
a man-in-the-middle attack against future TLS sessions with Bob's server.
However, he will not be able to recover the keys used for all the past
sessions that he captured.

.. index:: Perfect Forward Secrecy

.. note:: Perfect Forward Secrecy

   Perfect Forward Secrecy (PFS) is an important property for key
   exchange protocols. A protocol provides PFS if its design guarantees that
   the keys used for former sessions will not be compromised even if the
   private key of the server is compromised. This is a very important
   property. ``DHE_RSA`` provides Perfect Forward Secrecy, but the
   ``RSA`` key exchange does not provide this property. In practice,
   ``DHE_RSA`` is costly from a computational viewpoint. Recent implementations
   of TLS thus prefer  ``ECDHE_RSA`` or ``ECDHE_ECDSA`` when
   Perfect Forward Secrecy is required.


All the information required for the key exchange has now been transmitted.
There are two important messages that will be sent by the client and the server
to conclude the handshake and start the data transfer phase.

The client sends the ``ChangeCipherSpec`` message followed by the ``Finished``
message. The ``ChangeCipherSpec`` message indicates that the client has received
all the information required to generate the security keys for this TLS
session. This messages can also appear later in the session to indicate a
change in the encryption algorithms that are used, but this usage is outside
the scope of this book. The ``Finished`` message is more important. It confirms
to the server that the TLS handshake has been performed correctly and that no
attacker has been able to modify the data sent by the client or the server.
This is the first message that is encrypted with the selected security keys.
It contains a hash of all the messages that were exchanged during the handshake.

The server also sends a ``ChangeCipherSpec`` message followed by a ``Finished``
message.

.. note:: TLS Cipher suites

   A TLS cipher suite is usually represented as an ASCII string
   that starts with TLS and contains the acronym of the key exchange algorithm,
   the encryption scheme with the key size and its mode of operation and
   the authentication algorithm. For example,
   ``TLS_DHE_RSA_WITH_AES_128_GCM_SHA256`` is a TLS cipher suite that uses
   the ``DHE_RSA`` key exchange algorithm with 128 bits AES in GCM mode for
   encryption and SHA-256 for authentication. The official list of TLS
   cipher suites is maintained by IANA [#fianaTLS]_. The NULL acronym
   indicates that no algorithm has been specified. For example,
   ``TLS_ECDH_RSA_WITH_NULL_SHA`` is a cipher suite that does not use
   any encryption but still uses the ``ECDH_RSA`` key exchange and
   ``SHA`` for authentication.

The TLS record protocol
-----------------------

The handshake is now finished. The client and the server will exchange
authenticated and encrypted records. TLS defines different formats for the
records depending on the cryptographic algorithms that have been negotiated
for the session. A detailed discussion of these different types of
records is outside the scope of this introduction. For illustration, we
briefly describe one record format.

As other security protocols, TLS uses different keys to encrypt and
authenticate records. These keys are derived from the MasterSecret that
is either randomly generated by the client after the ``RSA`` key exchange
or derived from the Diffie Hellman parameters after the ``DH_RSA``
key exchange. The exact algorithm used to derive the keys is defined
in :rfc:`5246`.

A TLS record is always composed of four different fields :

 - a `Type` that indicates the type of record. The most frequent type
   is `application data` which corresponds to a record containing encrypted
   data. The other types are `handshake`, `change_cipher_spec` and
   `alert`.
 - a `Protocol Version` field that indicates the version of the TLS protocol
   used. This version is composed of two sub fields : a major and a
   minor version number.
 - a `Length` field. A TLS record cannot be longer than 16,384 bytes.
 - a `TLSPlainText` that contains the encrypted data

TLS supports several methods to encrypted records. The selected
method depends on the cryptographic algorithms that have been negotiated for
the TLS session. A detailed presentation of the different methods that can
be used to produce the `TLSPlainText` from the user data is outside the scope
of this book. As an example, we study one method: Stream Encryption. This
method is used with cryptographic algorithms which can operate on a stream
of bytes. The method starts with a sequence of bytes provided by the
user application: the plain text. The first step is to compute the
authentication code to verify the integrity of the data. For this, TLS
computes :math:`MAC(SeqNum, Header, PlainText)` using HMAC
where `SeqNum` is a sequence
number which is incremented by one for each new TLS record transmitted. The
`Header` is the header of the TLS record described above and `PlainText` is
the information that needs to be encrypted. Note that the sequence number
is maintained at the two endpoints of the TLS session, but it is not transmitted
inside the TLS record. This sequence number is used to prevent replay attacks.


.. index:: MAC-then-encrypt, Encrypt-then-MAC

.. note:: MAC-then-encrypt or Encrypt-then-MAC

   When secure protocols use Message Authentication and Encryption, they
   need to specify how these two algorithms are combined. A first
   solution, which is used by the current version of TLS, is to compute
   the authentication code and then encrypt both the data and the
   authentication code. A drawback of this approach is that the receiver
   of an encrypted TLS record must first attempt to decrypt data that
   has potentially been modified by an attacker before being able
   to verify the authenticity of the record. A better approach is
   for the sender to first encrypt the data and then compute the
   authentication code over the encrypted data. This is the encrypt-then-MAC
   approach proposed in :rfc:`7366`. With encrypt-then-MAC, the receiver
   first checks the authentication code before attempting to decrypt the
   record.


Improving TLS
-------------

During the last two decades, the deployment of TLS has continued to grow. The early TLS servers were only used for critical services such as e-commerce websites or online banks. As CPU performance improved, it became much more cost-effective to use TLS to secure non-critical parts of web servers, including the delivery of HTML pages and even video services. There is now a growing number of applications that rely on TLS [AM2019]_.

In 2013, the statistics collected by the Firefox Telemetry project [#ftelemetry]_ revealed that 30% of the web pages loaded by Firefox users were done over HTTPS. In October 2019, 80% of the web pages are loaded over HTTPS. In six years, HTTPS became the dominant protocol to access web services. Another look at the deployment of HTTPS on web sites may be found in [Helme2019]_.

Measurement studies that analyzed the evolution of TLS over the years have identified several important changes in the TLS ecosystem [KRA2018]_. First, the preferred cryptographic algorithms have changed. While RC4 was used by 60% of the connections in 2012, its usage has dropped since 2015. AES started to be deployed in 2013 and is now used for more than 90% of the connections. The deployed versions of TLS have also changed. TLS 1.0 and TLS 1.1 are now rarely used. The deployment of TLS 1.2 started in 2013 and reached 70% of the connections in 2015. Version 1.3 of TLS, that is described below, is also widely deployed.

.. spelling::

   Snowden
   RSA

Another interesting fact is the key exchange schemes. In 2012, RSA was the dominant solution, used by more than 80% of the observed connections [KRA2018]_. In 2013, Edward Snowden revealed the surveillance activities of several governments. These revelations had a huge impact on the Internet community. The IETF, which standardizes Internet protocols, considered in :rfc:`7258` that such pervasive monitoring was an attack. Since then, several IETF working groups have developed solutions to counter pervasive monitoring. One of these solutions is to encourage `Perfect Forward Security`. Within TLS, this implies replacing RSA by an authenticated Diffie Hellman key exchange such as ECDHE. Measurements indicate
that since summer 2014, ECDHE is more popular than RSA. In 2018, more than 90% of the observed TLS connections used ECDHE.

The last point is the difficulty of deploying TLS servers [KMS2017]_. When TLS servers are installed, the system administrator needs to obtain certificates and configure a range of servers. Initially, getting certificates was complex and costly, but initiatives such as https://letsencrypt.org have simplified this workflow.

.. spelling::

   workflow

In 2014, the IETF TLS working started to work on the development of version 1.3 of the TLS protocol. Their main objectives [Rescorla2015]_ for this new version were:

 - simplify the design by removing unused or unsafe protocol features
 - improve the security of TLS by leveraging the lessons learned from TLS 1.2 and some documented attacks
 - improve the privacy of the protocol
 - reduce the latency of TLS

Since 2014, latency has become an important concern for web services. As access networks bandwidth continue to grow, latency is becoming a key factor that affects the performance of interactive web services. With TLS 1.2, the download of a web page requires a minimum of four round-trip-times, one to create the underlying TCP connection, one to exchange the ClientHello/ServerHello, one to exchange the keys and then one to send the HTTP GET and retrieve the response. This can be very long when the server is not near the client. TLS 1.3 aimed at reducing this handshake to one round-trip-time and even zero by placing some of the cryptographic handshake in the TCP handshake. This part will be discussed in the TCP chapter. We focus here on the reducing the TLS handshake to a single round-trip-time.

To simplify both the design and the implementations, TLS 1.3 uses only a small number of cipher suites. Five of them are specified in :rfc:`8446` and ``TLS_AES_128_GCM_SHA256`` must be supported by all implementations. To ensure privacy, all cipher suites that did not provide Perfect Forward Secrecy have been removed. Compression has also been removed from TLS since several attacks on TLS 1.2 exploited its compression capability :rfc:`7457`.


.. note:: Enterprises, privacy and TLS

   By supporting only cipher suites that provide Perfect Forward Secrecy in TLS 1.3, the IETF aims at protecting the privacy of users against a wide range of attacks. However, this choice has resulted in intense debates in some enterprises. Some enterprises, notably in financial organizations, have deployed TLS, but wish to be able to decrypt TLS traffic for various security-related activities. These enterprises tried to lobby within the IETF to maintain RSA-based cipher suites that do not provide Perfect Forward Secrecy. Their arguments did not convince the IETF. Eventually, these enterprises moved to ETSI, another standardization body, and convinced them to adopt `entreprise TLS`, a variant of TLS 1.3 that does not provide Perfect Forward Secrecy [eTLS2018]_.

The TLS 1.3 handshake differs from the TLS 1.2 handshake in several ways. First, the TLS 1.3 handshake requires a single round-trip-time when the client connects for the first time to a server. To achieve this, the TLS designers look at the TLS 1.2 handshake in details and found that the first round-trip-time is mainly used to select the set of cryptographic algorithms and the cryptographic exchange scheme that will be used over the TLS session. TLS 1.3 drastically simplifies this negotiation by requiring to use the Diffie Hellman exchange with a small set of possible parameters. This means that the client can guess the parameters used by the server (i.e. the modulus, p and the base g) and immediately start the Diffie Hellman exchange. A simplified version of the TLS 1.3 handshake is shown in the figure below.


  .. msc::

      a [label="", linecolour=white],
      b [label="Client",linecolour=black],
      z [label="", linecolour=white],
      c [label="Server", linecolour=black],
      d [label="", linecolour=white];

      b>>c [ label = "ClientHello[Random, g^c]", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "ServerHello[Random, g^s]", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "Certificate, Sign(K,Handshake), Finished, Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;
      b>>c [ label = "Finished", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;
      b>>c [ label = "Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;

There are several important differences with the TLS 1.2 handshake. First, the Diffie Hellman key exchange is required in TLS 1.3 and this exchange is initiated by the client (before having validated the server identity). To initiate the Diffie Hellman key exchange, the client needs to guess the modulus and the base that can be accepted by the server. Either the client uses standard parameters that most server supports or the client remembers the last modulus/base that it used with this particular server. If the client guessed incorrectly, the server replies with the parameters that it expects and one round-trip-time is lost. When the server sends its `ServerHello`, it already knows the session key. This implies that the server can encrypt all subsequent messages. After one round-trip-time, all data exchanged over the TLS 1.3 session is encrypted and authenticated. In TLS 1.3, the server certificate is encrypted with the session key, as well as the `Finished` message. The server signs the handshake to confirm that it owns the public key of its certificate. If the server wants to send application data, it can already encrypt it and send it to the client. Upon reception of the server Certificate, the client verifies it and checks the signature of the handshake and the `Finished` message. The client confirms the end of the handshake by sending its own `Finished` message. At that time, the client can send encrypted data. This means that the client only had to wait one round-trip-time before sending encrypted data. This is much faster than with TLS 1.2.

.. spelling::

   pre
   rtt

For some applications, waiting one round-trip-time before being able to send data is too long. TLS 1.3 allows the client to send encrypted data immediately after the `ClientHello`, without having to wait for the `ServerHello` message. At this point in the handshake, the client cannot know the key that will be derived by the Diffie Hellman key exchange. The trick is that the server and the client need to have previously agreed on a `pre-shared-key`. This key could be negotiated out of band, but usually it was exchanged over a previous TLS session between the client and the server. Both the client and the server can store this key in their cache. When the client creates a new TLS session to a server, it checks whether it already knows a pre-shared key for this server. If so, the client announces the identifier of this key in its `ClientHello` message. Thanks to this identifier, the server can recover the key and use it to decrypt the 0-rtt Encrypted record. A simplified version of the 0-rtt TLS 1.3 handshake [#fhandshake]_ is shown in the figure below.

  .. msc::

      a [label="", linecolour=white],
      b [label="Client",linecolour=black],
      z [label="", linecolour=white],
      c [label="Server", linecolour=black],
      d [label="", linecolour=white];

      b>>c [ label = "ClientHello[Random, g^c,server_conf=abcd]", arcskip="2"];
      |||;
      b>>c [ label = "0-rtt Encrypted record", textcolour="magenta", arcskip="2"];
      |||;
      c>>b [ label = "ServerHello[Random, g^s]", arcskip="2"];
      |||;
      c>>b [ label = "Certificate, Sign(K,Handshake), Finished, Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;
      b>>c [ label = "Finished", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      c>>b [ label = "Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      b>>c [ label = "Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;


On the web, TLS clients use certificates to authenticate servers but the clients are not authenticated. However, there are environments such as enterprise networks where servers may need to authenticate clients as well. A popular deployment is to authenticate remote clients who wish to access the enterprise network through a Virtual Private Network service. Some of these services run above TLS (or more precisely a variant of TLS named DTLS that runs above UDP [MoR2004]_ but is outside the scope of this chapter). In such services, each client is authenticated thanks to a public key and a certificate that is trusted by the servers. To establish a TLS session, such a client needs to prove that it owns the public key associated with the certificate. This is done by the server thanks to the CertificateRequest message. The TLS handshake becomes the following one:

  .. msc::

      a [label="", linecolour=white],
      b [label="Client",linecolour=black],
      z [label="", linecolour=white],
      c [label="Server", linecolour=black],
      d [label="", linecolour=white];

      b>>c [ label = "ClientHello[Random, g^c,server_conf=abcd]", arcskip="2"];
      |||;
      b>>c [ label = "0-rtt Encrypted record", textcolour="magenta", arcskip="2"];
      |||;

      c>>b [ label = "ServerHello[Random, g^s]", arcskip="2"];
      |||;
      |||;
      c>>b [ label = "CertificateRequest, Certificate, Sign(K,Handshake), Finished, Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      b>>c [ label = "Certificate, Sign(Kc, Handshake), Finished", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      c>>b [ label = "Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      b>>c [ label = "Encrypted Record", textcolour="red", linecolour="red", arcskip="2"];
      |||;
      |||;

The server sends a CertificatRequest message. The client returns its certificate and signs the Handshake with is private key. This confirms to the server that the client owns the public key indicated in its certificate.

There are many more differences between TLS 1.2 and TLS 1.3. Additional details may be found in their respective specifications, :rfc:`5246` and :rfc:`8446`.

.. spelling::

   dataset

.. _DNSSEC:

Securing the Domain Name System
===============================

The Domain Name System provides a critical service in the Internet
infrastructure since it maps the domain names that are used by end users
onto IP addresses. Since end users rely on names to identify the servers
that they connect to, any incorrect information distributed by the DNS
would direct end users' connections to invalid destinations. Unfortunately,
several attacks of this kind occurred in the past. A detailed analysis
of the security threats against the DNS appeared in :rfc:`3833`. We consider
three of these threats in this section and leave the others to :rfc:`3833`.

The first type of attack is `eavesdropping`. An attacker who can capture
packets sent to a DNS resolver or a DNS server can gain valuable information
about the DNS names that are used by a given end user. If the attacker can
capture all the packets sent to a DNS resolver, he/she can collect a lot of
meta data about the domain names used by the end user. Preventing this type
of attack has not been an objective of the initial design of the DNS.
There are currently discussions with the IETF to carry DNS messages over
TLS sessions to protect against such attacks. However, these solutions
are not yet widely deployed.

The second type of attack is the `man-in-the-middle` attack. Consider that
Alice is sending DNS requests to her DNS resolver. Unfortunately, Mallory
sits in front of this resolver and can capture and modify all the packets
sent by Alice to her resolver. In this case, Mallory can easily modify
the DNS responses sent by the resolver to redirect Alice's packets to
a different IP address controlled by Mallory. This enables Mallory
to observe (and possibly modify) all the packets sent and received by
Alice. In practice, executing this attack is not simple since DNS resolvers
are usually installed in protected datacenters. However, if Mallory controls
the WiFi access point that Alice uses to access the Internet, he could easily
modify the packets on this access point and some software packages
automate this type of attacks.

If Mallory cannot control a router on the path
between Alice and her resolver, she could still launch a different attack.
To understand this attack, it is important to correctly understand how
the DNS protocol operates and the roles of the different fields of
the DNS header which is reproduced in :numref:`fig-dns-header2`.

.. _fig-dns-header2:
.. figure:: /pkt/dnsheader.*
   :align: center
   :scale: 100

   DNS header

The first field of the header is the `Identification` field. When Alice
sends a DNS request, she places a 16-bits integer in this field and
remembers it. When she receives a response, she uses this `Identification`
field to locate the initial DNS request that she sent. The response is
only used if its `Identification` matches a pending DNS request (containing
the same question).

.. index:: cache poisoning attack (DNS)

Mallory has studied the DNS protocol and understands how it works. If he
can predict a popular domain for which Alice will regularly send DNS requests,
then he can prepare a set of DNS responses that map the name requested
by Alice to an IP address controlled by Mallory instead of the legitimate
DNS response. Each DNS response has a different `Identification`. Since there
are only 65,536 values for the `Identification` field, it is possible
for Mallory to
send them to Alice hoping that one of them will be received while Alice
is waiting for a DNS response with the same identifier. In the past,
it was difficult to send 65,536 DNS responses quickly enough. However, with
the high speed links that are available today, this is not an issue anymore.
A second concern for Mallory is that he must be able to send
the DNS responses as if they were coming directly from the DNS resolver.
This implies that Mallory must be able to send IP packets that appear to
originate from a different address. Although networks should be configured
to prevent this type of attack, this is not always the case and there
are networks where it is possible for a host to send packets with a
different source IP address [#fspoof]_. If the attack targets a single
end user, e.g. Alice, this is annoying for this user. However, if the
attacker can target a DNS resolver that serves an entire company or an
entire ISP, the impact of the attack can be much larger in particular if
the injected DNS response carries a long TTL and thus resides in the
resolver's cache for a long period of time.

Fortunately, designers of DNS servers and resolvers have found solutions to mitigate this type
of attack. The easiest approach would have been to update the format of the
DNS requests and responses to include a larger `Identifier` field.
Unfortunately, this elegant solution was not possible with the DNS because
the DNS messages do not include any version number that would have enabled
such a change. Since the DNS messages are exchanged inside UDP segments,
the DNS developers found an alternate solution to counter this attack.
There are two ways for the DNS library used by Alice to send her DNS requests.
A first solution is to bind one UDP source port and always send the
DNS requests from this source port (the destination port is always port
``53``). The advantage of this solution is that Alice's DNS library can
easily receive the DNS responses by listening to her chosen port.
Unfortunately, once the attacker has found the source port used by Alice,
he only needs to send 65,536 DNS responses to inject an invalid response.
Fortunately, Alice can send her DNS requests in a different way. Instead
of using the same source port for all DNS requests, she can use a different
source port for each request. In practice, each DNS request will be sent
from a different source port. From an implementation viewpoint, this
implies that Alice's DNS library will need to listen to one different port
number for each pending DNS request. This increases the complexity of
her implementation. From a security viewpoint there is a clear benefit
since the attacker needs to guess both the 16 bits `Identifier` and the
16 bits `UDP source port` to inject a fake DNS response. To generate all
possible DNS responses, the attacker would need to generate almost
:math:`2^{32}` different messages, which is excessive in today's networks.
Most DNS implementations use this second approach to prevent these cache
poisoning attacks.

These attacks affect the DNS messages that are exchanged between a client
and its resolver or between a resolver and name servers. Another type of
attack exploits the possibility of providing several resource records inside
one DNS response. A frequent optimization used by DNS servers and resolvers
is to include several related resource records in each response. For
example, if a client sends a DNS query for an `NS` record, it usually
receives in the response both the queried record, i.e. the name of
the DNS server that serves the queried domain, and the IP addresses of this
server. Some DNS servers return several `NS` records and the associated IP
addresses. The `cache poisoning` attack exploits this DNS optimization.

Let us illustrate it on an example.
Assume that Alice frequently uses the `example.net` domain and in
particular the
web server whose name is `www.example.net`. Mallory would like to redirect
the TCP connections established by Alice towards `www.example.net` to one
IP address that he controls. Assume that Mallory controls the
`mallory.net` domain. Mallory can tune the DNS server of his domain and add
special DNS records to the responses that it sends. An attack could go
roughly as follows. Mallory forces Alice to visit the `www.mallory.net` web
site. He can achieve this by sending a spam message to Alice or buying
advertisements on a web site visited by Alice and redirect one of these
advertisements to `www.mallory.net`. When visiting the advertisement, Alice's
DNS resolver will send a DNS request for `www.mallory.net`. Since Mallory
control the DNS server, he can easily add in the response a `AAAA`
record that associates `www.example.net` to the IP address controlled by
Mallory. If Alice's DNS library does not check the returned response,
the cache entry for `www.example.net` will be replaced by the `AAAA` record
sent by Mallory.

To cope with these security threats and improve the security of the
DNS, the IETF has defined several extensions that are known as DNSSEC.
DNSSEC exploits public-key cryptography to authenticate the content
of the DNS records that are sent by DNS servers and resolvers. DNSEC is
defined in three main documents :rfc:`4033`, :rfc:`4034`, :rfc:`4035`.
With DNSSEC, each DNS zone uses one public-private key pair. This key pair
is only used to sign and authenticate DNS records. The DNS records are
not encrypted and DNSSEC does not provide any confidentiality. Other DNS
extensions are being developed to ensure the confidentiality of the
information exchanged between a client and its resolvers :rfc:`7626`.
Some of these extensions exchange DNS records over a TLS session which
provides the required confidentiality, but they are not yet deployed
and outside the scope of this chapter.

DNSSEC defines four new types of DNS records that are used together to
authenticate the information distributed by the DNS.

 - the `DNSKEY` record allows storing the public key associated with
   a zone. This record is encoded as a TLV and includes a `Base64`
   representation of the key and the identification of the public key
   algorithm. This allows the `DNSKEY` record to support different public
   key algorithms.
 - the `RRSIG` record is used to encode the signature of a DNS record. This
   record contains several sub-fields. The most important ones are the
   algorithm used to generate the signature, the identifier of the public
   key used to sign the record, the original TTL of the signed record and
   the validity period for the signature.
 - the `DS` record contains a hash of a public key. It is used by a parent
   zone to certify the public key used by one of its child zones.
 - the `NSEC` record is used when non-existent domain names are queried.
   Its usage will be explained later

The simplest way to understand the operation of DNSSEC is to rely on a simple
example. Let us consider the `example.org` domain and assume that Alice
wants to retrieve the `AAAA` record for `www.example.org` using DNSSEC.

.. index:: anchored key

The security of DNSSEC relies on `anchored keys`. An `anchored key` is a
public key that is considered as trusted by a resolver. In our example,
we assume that Alice's resolver has obtained the public key of the servers
that manage the root zone in a secure way. This key
has been distributed outside of the DNS, e.g. it has been published in a
newspaper or has been received in a sealed letter.

To obtain an authenticated record for `www.example.org`, Alice's resolver
first needs to retrieve the `NS` which is responsible for the `.org`
Top-Level Domain (TLD). This record is served by the DNS root server
and Alice's resolver can retrieve the signature (`RRSIG` record) for this
`NS` record. Since Alice knows the `DNSKEY` of the root, she can verify
the validity of this signature.

The next step is to contact `ns.org`, the `NS` responsible for
the `.org` TLD to retrieve the `NS` record for the `example.org` domain.
This record is accompanied by a `RRSIG` record that authenticates it. This
`RRSIG` record is signed with the key of the `.org` domain. Alice's resolver
can retrieve this public key as the `DNSKEY` record for the `.org`, but how
can it trust this key since it is distributed by using the DNS and
could have been modified by attackers ? DNSSEC solves this problem by
using the `DS` record that is stored in the parent zone (in this case,
the root zone). This record contains a hash of a public key that
is signed with a `RRSIG` signature. Since Alice's resolver's
trusts the root key, it can validate the signature of the `DS` record
for the `.org` domain. It can then retrieve the `DNSKEY` record for this
domain from the DNS and compare the hash of this key with the `DS` record.
If they match, the public key of the `.org` domain can be trusted.
The same technique is used to obtain and validate the key of
the `example.org` domain. Once this key is trusted, Alice's resolver
can request the `AAAA` record for `www.example.org` and validate its
signature.

Thanks to the `DS` record, a resolver can validate the public keys of client
zones as long as their is a chain of `DS` -> `DNSKEY` records from an
anchored key. If the resolver trusts the public key of the root zone, it
can validate all DNS replies for which this chain exists.

There are several details of the operation of DNSSEC that are worth
being discussed. First, a server that supports DNSSEC must have a
public-private key pair. The public key is distributed with the
`DNSKEY` record. The private key is never distributed and it does not
even need to be stored on the server that uses the public key. DNSSEC does
not require the DNSSEC servers to perform any operation that requires
a private key in real time. All the `RRSIG` records can be computed
offline, possibly on a different server than the server that returns
the DNSSEC replies. The initial motivation for this design choice was
the CPU complexity of computing the `RRSIG` signatures for zones that
contain millions of records. In the early days of DNSSEC, this was an
operational constraint. Today, this is less an issue, but avoiding
costly signature operations in real time has two important benefits.
First, this reduces the risk of denial of service attacks since an attacker
cannot force a DNSSEC server to perform computationally intensive signing
operations. Second, the private key can be stored offline, which means that
even if an attacker gains access to the DNSSEC server, it cannot retrieve
its private key. Using offline signatures for the `RRSIG` records has some
practical implications that are reflected in the content of this
record. First, each `RRSIG` record contains the original TTL of the
signed record.
When DNS resolvers cache records, they change the value of the TTL of
these cached records and then return the modified records to their clients.
When a resolver receives a signed DNS record, it must replace the
received TTL of the record with the original TTL (and check that the
received TTL is smaller than the original one) before checking the
signature. Second, the `RRSIG` records contain a validity period, i.e.
a starting time and an ending time for the validity of the signature. This
period is specified as two timestamps. This period is only the
validity of the signature. It does not affect the TTL of the signed record
and is independent from the TTL. In practice, the validity period is
important to allow DNS server operators to update their public/private
keys. When such a key is changed, e.g. because the private could have been
compromised, there is some period of time during which records signed
with the two keys coexist in the network. The validity period allows
ensuring that old signatures do not remain in DNS caches for ever.

.. spelling::

   timestamps

.. index:: NSEC

The last record introduced by DNSSEC is the `NSEC` record. It is used to
authenticate a negative response returned by a DNS server. If a resolver
requests a domain name that is not defined in the zone, the server
replies with an error message. The designers of the original version
of the DNS thought that these errors would not be very frequent
and resolvers were not required to cache those negative responses.
However, operational experience showed that queries for invalid domain
names are more frequent than initially expected and a large fraction
of the load on some servers is caused by repeated queries for invalid
names. Typical examples include queries for invalid TLDs to the root
DNS servers or queries caused by configuration errors [WF2003]_.
Current DNS deployments allow resolvers to cache those negative answers
to reduce the load on the entire DNS :rfc:`2308`.

The simplest way to allow a DNSSEC server to return signed negative responses
would be for the server to return a signed response that contains the
received query and some information indicating the error.
The client could then easily check the validity of the negative response.
Unfortunately, this would force the DNSSEC server to generate signatures
in real time. This implies that the private key must be stored in the
server memory, which leads to risks if an attacker can take control
of the server. Furthermore, those signatures are computationally complex
and a simple denial of service attack would be to send invalid queries
to a DNSSEC server.

Given the above security risks, DNSSEC opted for a different approach that
allows the negative replies to be authenticated by using offline signatures.
The `NSEC` record exploits the lexicographical ordering of all the domain
names. To understand its usage, consider a simple domain that contains
three names (the associated `AAAA` and other records that are not
shown) :

.. code-block:: console

   alpha.example.org
   beta.example.org
   gamma.example.org


In this domain, the DNSSEC server adds three `NSEC` records. A `RRSIG`
signature is also computed for each of these records.

.. code-block:: console

   alpha.example.org
   alpha.example.org NSEC beta.example.org

   beta.example.org
   beta.example.org NSEC gamma.example.org

   gamma.example.org
   gamma.example.org NSEC alpha.example.org


If a resolver queries `delta.example.org`, the server will parse its
zone. If this name were present, it would have been placed, in lexicographical
order, between the `beta.example.org` and the `gamma.example.org` names.
To confirm that the `delta.example.org` name does not exist, the server
returns the `NSEC` record for `beta.example.org` that indicates that the
next valid name after `beta.example.org` is `gamma.example.org`. If
the server receives a query for `pi.example.org`, this is the `NSEC` record
for `gamma.example.org` that will be returned. Since this record
contains a name that is before `pi.example.org` in lexicographical
order, this indicates that `pi.example.org` does not exist.


.. todo: explain DoT and DoH (DoQ will be discussed later at the end of the QUIC chapter)


.. rubric:: Footnotes
	    
.. [#fnull] For some of the algorithms, it is possible to negotiate the
           utilization of no algorithm. This happens frequently for the
           compression algorithm that is not always used. For this,
           both the client and the server must announce ``null``
           in their ordered list of supported algorithms.

.. [#fdnsssh] For example, :rfc:`4255` describes a DNS record that can be
              used to associate an ``ssh`` fingerprint to a DNS name.

.. [#fsshkeys] The exact algorithms used for the computation of these
               keys are defined in :rfc:`4253`

.. [#fianaTLS] See http://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-parameters-4

.. [#fhandshake] A detailed explanation of the TLS 1.3 handshake may be found at https://tls13.ulfheim.net/
.. [#ftelemetry] See https://letsencrypt.org/stats/ for a graph and https://docs.telemetry.mozilla.org/datasets/other/ssl/reference.html for additional information on the dataset

.. [#fspoof] See http://spoofer.caida.org/summary.php for an ongoing measurement study that analyses the networks where an attacker could send packets with any source IP address.
	       
.. include:: /links.rst
