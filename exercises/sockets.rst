

Using sockets for inter-process communication
=============================================


Popular operating systems allow isolating different programs by executing them in separate `processes`. A :term:`socket` is a tool provided by the operating system that enables two separated processes to communicate with each other. A socket takes the form of a file descriptor and can be seen as a communication pipe through which the communicating processes can exchange arbitrary information. In order to receive a message, a process must be attached to a specific :term:`address` that the peer can use to reach it.

.. add the two socket images


.. tikz:: Connecting two processes communicating on the same computer
    :libs: calc

    % processes
	\begin{scope}[local bounding box=processes]
	% process A
	\draw (1,1) rectangle (3.5,4) node[midway] {\texttt{Process A}};
	% process B
	\draw (10,1) rectangle (12.5,4) node[midway] {\texttt{Process B}};


	\draw[fill=gray] (3.25, 1.75) rectangle (3.75, 3.25) node[midway, rotate=90] {socket}; % socket 1


	\draw[fill=gray] (9.75, 1.75) rectangle (10.25, 3.25) node[midway, rotate=270] {socket}; % socket 2

	% pipe 1
	\draw (3.75, 2) -- (9.75, 2);
	\draw (3.75, 2.15) -- (9.75, 2.15);
	% arrow of pipe 1
	\draw[->, thick] (6, 1.8) -- (7.5, 1.8);

	% pipe 2
	\draw (3.75, 3) -- (9.75, 3);
	\draw (3.75, 2.85) -- (9.75, 2.85);
	% arrow of pipe 2
	\draw[<-, thick] (6, 3.2) -- (7.5, 3.2);


	\end{scope}

	\draw (0,0) rectangle (13.5, 5) node[midway] {};

	\node[anchor=south west] at (0.1, 0.1) {\texttt{Computer 1}};


	\draw ($(processes.south west) + (-1,-1)$) rectangle ($(processes.north east) + (1,1)$);



The socket is a powerful abstraction as it allows processes to communicate even if they are located on different computers. In this specific cases, the inter-processes communication will go through a network.

.. tikz:: Connecting two processes communicating on different computers
    :libs: calc

    % processes
	\begin{scope}[local bounding box=processes]
	% process A
	\draw (1,1) rectangle (3.5,4) node[midway] {\texttt{Process A}};
	% process B
	\draw (10,1) rectangle (12.5,4) node[midway] {\texttt{Process B}};


	\draw[fill=gray] (3.25, 1.75) rectangle (3.75, 3.25) node[midway, rotate=90] {socket}; % socket 1


	\draw[fill=gray] (9.75, 1.75) rectangle (10.25, 3.25) node[midway, rotate=270] {socket}; % socket 2

	% pipe 1
	\draw (3.75, 2) -- (9.75, 2);
	\draw (3.75, 2.15) -- (9.75, 2.15);
	% arrow of pipe 1
	\draw[->, thick] (6, 1.8) -- (7.5, 1.8);

	% pipe 2
	\draw (3.75, 3) -- (9.75, 3);
	\draw (3.75, 2.85) -- (9.75, 2.85);
	% arrow of pipe 2
	\draw[<-, thick] (6, 3.2) -- (7.5, 3.2);


	\end{scope}

	% computer 1
	\draw (0,0) rectangle (4.5, 5) node[midway] {};

	\node[anchor=south west] at (0.1, 0.1) {\texttt{Computer 1}};

	% computer 2
	\draw (9,0) rectangle (13.5, 5) node[midway] {};
	\node[anchor=south east] at (13.4, 0.1) {\texttt{Computer 2}};



Networked applications were usually implemented by using the :term:`socket` :term:`API`. This API was designed when TCP/IP was first implemented in the `Unix BSD`_ operating system [Sechrest]_ [LFJLMT]_, and has served as the model for many APIs between applications and the networking stack in an operating system. Although the socket API is very popular, other APIs have also been developed. For example, the STREAMS API has been added to several Unix System V variants [Rago1993]_. The socket API is supported by most programming languages and several textbooks have been devoted to it. Users of the C language can consult [DC2009]_, [Stevens1998]_, [SFR2004]_ or [Kerrisk2010]_. The Java implementation of the socket API is described in [CD2008]_ and in the `Java tutorial <http://java.sun.com/docs/books/tutorial/networking/sockets/index.html>`_. Python's socket module documentation can be found in the `Python documentation <https://docs.python.org/3/library/socket.html>`_.

The socket API is quite low-level and should be used only when you need a complete control of the network access. If your application simply needs, for instance, to retrieve data from a web server, there are much simpler and higher-level APIs.

A detailed discussion of the socket API is outside the scope of this section and the references cited above provide a detailed discussion of all the  details of the socket API. In this section, we will use the Python socket API to illustrate the key concepts. Python provides a simple and portable interface to sockets through its built-in ``socket`` module.

As a starting point, it is interesting to compare the socket API with the service primitives that we have discussed in the previous chapter. Let us first consider the connectionless service that consists of the following two primitives :

 - `DATA.request(destination,message)` is used to send a message to a specified destination. In this socket API, this corresponds to the ``send`` method.
 - `DATA.indication(message)` is issued by the transport service to deliver a message to the application. In the socket API, this corresponds to the return of the ``recv`` method that is called by the application.

The `DATA` primitives are exchanged through a service access point. In the socket API, the equivalent to the service access point is the `socket`. A `socket` is a data structure which is maintained by the networking stack and is used by the application every time it needs to send or receive data through the networking stack.

Sending data to a peer using a socket
-------------------------------------

In order to reach a peer, a process must know its :term:`address`. An address is a value that identifies a peer in a given network. There exists many different kinds of address families. For example, some of them allow reaching a peer using the file system on the computer. Some others enable communicating with a remote peer through a network. The socket API provides generic functions that work with different address families. This is partly why sockets are a powerful abstraction.

The ``sendto`` method allows sending data to a peer identified by its socket address through a given socket.

.. code-block:: python

    socket.sendto(data, address)

The ``data`` argument is a bytes object containing the data to send to the peer. The ``address`` is the socket address of the destination, which is typically a tuple ``(host, port)`` for network sockets.

In the following example, a Python program sends the bytes ``'h'``, ``'e'``, ``'l'``, ``'l'`` and ``'o'`` to a remote process located at address ``peer_addr``, using the already created socket ``sock``.

.. code-block:: python

    import socket

    def send_hello_to_peer(sock, peer_addr):
        """
        Send the message 'hello' to a peer.

        Args:
            sock: A socket object used to send the data
            peer_addr: The address of the peer (e.g., ('::1', 55555) for IPv6)
        """
        try:
            # sendto() sends the bytes to the specified address
            # The message must be encoded to bytes (strings are Unicode in Python)
            sent = sock.sendto(b"hello", peer_addr)
            print(f"Sent {sent} bytes to {peer_addr}")
        except OSError as e:
            # OSError is raised when a socket operation fails
            print(f"Could not send the message: {e}")
            raise

As the ``sendto`` method is generic, this function will work correctly independently from the fact that the peer's address is defined as a path on the computer filesystem or a network address.


Receiving data from a peer using a socket
-----------------------------------------

Operating systems allow assigning an address to a socket using the ``bind`` method. This is useful when you want to receive messages from another program to which you announced your socket address.
Once the address is assigned to the socket, the program can receive data from others using methods such as ``recv`` and ``recvfrom``.

The following program binds its socket to a given socket address and then waits for receiving new bytes, using the already created socket ``sock``.

.. code-block:: python

    import socket

    MAX_MESSAGE_SIZE = 2500

    def bind_and_receive_from_peer(sock, local_addr):
        """
        Bind the socket to a local address and receive a message.

        Args:
            sock: A socket object
            local_addr: The local address to bind to (e.g., ('', 55555) for any interface)
        """
        try:
            # bind() assigns our address to the socket so others can reach us
            sock.bind(local_addr)
        except OSError as e:
            print(f"Could not bind on the socket: {e}")
            raise

        try:
            # recv() blocks until data is received
            # It returns a bytes object containing the received data
            data = sock.recv(MAX_MESSAGE_SIZE)
        except OSError as e:
            print(f"Could not receive the message: {e}")
            raise

        # Print what we received
        print(f"Received {len(data)} bytes:")
        # Display each byte in hexadecimal and as a character
        for byte in data:
            # byte is already an integer in Python 3
            char = chr(byte) if 32 <= byte < 127 else '.'
            print(f"0x{byte:02x} ('{char}') ", end="")
        print()

        return data

.. note::

    Depending on the socket address family, the operating system might implicitly assign an address to an unbound socket upon a call to ``send`` or ``sendto``. While this is a useful behavior, describing it precisely is out of the scope of this section.

.. note::

    In Python, socket operations work with ``bytes`` objects, not strings. To convert a string to bytes, use ``string.encode('utf-8')``. To convert bytes to a string, use ``bytes.decode('utf-8')``. When working with binary protocols, you should work directly with bytes.

Using this code, the program will read and print an arbitrary message received from an arbitrary peer who knows the program's socket address. If we want to know the address of the peer that sent us the message, we can use the ``recvfrom`` method. This is what a modified version of ``bind_and_receive_from_peer`` is doing below.

.. code-block:: python

    import socket

    MAX_MESSAGE_SIZE = 2500

    def bind_and_receive_from_peer_with_addr(sock, local_addr):
        """
        Bind the socket and receive a message, also retrieving the sender's address.

        Args:
            sock: A socket object
            local_addr: The local address to bind to
        """
        try:
            # Assign our address to the socket
            sock.bind(local_addr)
        except OSError as e:
            print(f"Could not bind on the socket: {e}")
            raise

        try:
            # recvfrom() returns both the data AND the sender's address
            # This is useful when we need to reply to the sender
            data, peer_addr = sock.recvfrom(MAX_MESSAGE_SIZE)
        except OSError as e:
            print(f"Could not receive the message: {e}")
            raise

        # Print what we received
        print(f"Received {len(data)} bytes:")
        for byte in data:
            char = chr(byte) if 32 <= byte < 127 else '.'
            print(f"0x{byte:02x} ('{char}') ", end="")
        print()

        # Print the address of the peer who sent the message
        # For IPv6, peer_addr is a tuple: (host, port, flowinfo, scope_id)
        # For IPv4, peer_addr is a tuple: (host, port)
        print(f"Message received from: {peer_addr}")

        return data, peer_addr


This function is now using the ``recvfrom`` method that returns both the data and the address of the peer who sent the message. In Python, the address is returned as a tuple, making it easy to use directly with ``sendto`` for sending a reply.

``connect``: connecting a socket to a remote address
----------------------------------------------------

Operating systems enable linking a socket to a remote address so that every information sent through the socket will only be sent to this remote address, and the socket will only receive messages sent by this remote address. This can be done using the ``connect`` method shown below.

.. code-block:: python

    socket.connect(address)

This method will assign the socket to the ``address`` remote socket address. The process can then use the ``send`` method without needing to specify the destination socket address.
Furthermore, calls to ``recv`` will only deliver messages sent by this remote address. This is useful when we only care about the other peer's messages.

The following program connects a socket to a remote address, sends a message and waits for a reply.

.. code-block:: python

    import socket

    MAX_MESSAGE_SIZE = 2500

    def send_hello_and_read_reply(sock, peer_addr):
        """
        Connect to a peer, send 'hello', and wait for a reply.

        Args:
            sock: A socket object
            peer_addr: The address of the peer to connect to
        """
        try:
            # connect() links the socket to the remote address
            # After this, we can use send() instead of sendto()
            sock.connect(peer_addr)
        except OSError as e:
            print(f"Could not connect the socket: {e}")
            raise

        try:
            # After connect(), we can use send() without specifying the address
            # The socket remembers the peer's address
            sent = sock.send(b"hello")
            print(f"Sent {sent} bytes")
        except OSError as e:
            print(f"Could not send the message: {e}")
            raise

        try:
            # recv() will only receive messages from the connected peer
            data = sock.recv(MAX_MESSAGE_SIZE)
        except OSError as e:
            print(f"Could not read on the socket: {e}")
            raise

        # Print what we received
        print(f"Received {len(data)} bytes:")
        for byte in data:
            char = chr(byte) if 32 <= byte < 127 else '.'
            print(f"0x{byte:02x} ('{char}') ", end="")
        print()

        return data


Creating a new socket to communicate through a network
------------------------------------------------------

Until now, we learned how to use sockets that were already created. When writing a whole program, you will have to create your own sockets and choose the concrete technology that it will use to communicate with others. In this section, we will create new sockets and allow a program to communicate with processes located on another computer using a network. The most recent standardized technology used to communicate through a network is the :term:`IPv6` network protocol.
In the IPv6 protocol, hosts are identified using *IPv6 addresses*. Modern operating systems allow IPv6 network communications between programs to be done using the socket API, just as we did in the previous sections.

A program can use the ``socket.socket()`` constructor to create a new socket.

.. code-block:: python

    import socket
    sock = socket.socket(family, type, proto=0)

The ``family`` parameter specifies the address family that we will use to concretely perform the communication. For an IPv6 socket, the ``family`` parameter will be set to the value ``socket.AF_INET6``, telling the operating system that we plan to communicate using IPv6 addresses.
The ``type`` parameter specifies the communication guarantees that we need. For now, we will use the type ``socket.SOCK_DGRAM`` which allows us to send *unreliable messages* (UDP datagrams). This means that each data that we send at each call of ``sendto`` will either be completely received or not received at all. The following line creates a socket, telling the operating system that we want to communicate using IPv6 addresses and that we want to send unreliable messages.


.. code-block:: python

    import socket

    # Create an IPv6 UDP socket
    # AF_INET6: use IPv6 addresses
    # SOCK_DGRAM: use unreliable datagrams (UDP)
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)


Sending a message to a remote peer using its IPv6 address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we created an IPv6 socket, we can use it to reach another program if we know its IPv6 address. IPv6 addresses have a human-readable format that can be represented as a string of characters. The details of IPv6 addresses are out of scope of this section but here are some examples :
 - The ``::1`` IPv6 address identifies the computer on which the current program is running (the loopback address).
 - The ``2001:6a8:308f:9:0:82ff:fe68:e520`` IPv6 address identifies the computer serving the ``https://beta.computer-networking.info`` website.

An IPv6 address often identifies a computer and not a program running on the computer. In order to identify a specific program running on a specific computer, we use a *port number* in addition to the IPv6 address. A program using an IPv6 socket is thus identified using :
 - The IPv6 address of the computer
 - The port number identifying the program running on the computer

In Python, IPv6 socket addresses are represented as tuples. The following code creates an address tuple that identifies the program that reserved the port number ``55555`` on the computer identified by the ``::1`` IPv6 address.


.. code-block:: python

    # In Python, IPv6 addresses are simple tuples: (host, port, flowinfo, scope_id)
    # For most use cases, flowinfo and scope_id can be set to 0
    # The host is a string containing the IPv6 address
    # The port is an integer

    peer_addr = ("::1", 55555, 0, 0)  # IPv6 address ::1, port 55555

    # For convenience, you can also use just (host, port) and Python will fill in the rest
    peer_addr = ("::1", 55555)

Now, we have built everything we need to send a message to the remote program. The ``create_socket_and_send_message`` function below assembles all the building blocks we created until now in order to send the message ``"hello"`` to the program running on port ``55555`` on the computer identified by the ``::1`` IPv6 address.

.. code-block:: python

    import socket

    def create_socket_and_send_message():
        """
        Create an IPv6 UDP socket and send 'hello' to a peer.
        This function demonstrates the complete workflow of socket communication.
        """
        try:
            # Create an IPv6 UDP socket
            # AF_INET6: use IPv6 addresses
            # SOCK_DGRAM: use unreliable datagrams (UDP)
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        except OSError as e:
            print(f"Could not create the IPv6 SOCK_DGRAM socket: {e}")
            raise

        # Define the peer's address as a tuple (host, port)
        # ::1 is the IPv6 loopback address (equivalent to 127.0.0.1 in IPv4)
        # 55555 is the port number where the peer is listening
        peer_addr = ("::1", 55555)

        try:
            # Use the send_hello_to_peer function we defined previously
            send_hello_to_peer(sock, peer_addr)
        finally:
            # Always close the socket to release system resources
            # Using a try/finally block ensures the socket is closed even if an error occurs
            sock.close()

.. note::

    In Python, it's recommended to use the ``with`` statement for automatic resource management:

    .. code-block:: python

        with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as sock:
            send_hello_to_peer(sock, ("::1", 55555))
        # Socket is automatically closed when exiting the 'with' block

Note that we can reuse our ``send_hello_to_peer`` function without any modification as we wrote it to handle any kind of sockets, including sockets using the IPv6 network protocol.


Endianness: exchanging integers between different computers
-----------------------------------------------------------

Besides character strings, some applications also need to exchange 16 bits and 32 bits fields such as integers. A naive solution would have been to send the 16- or 32-bits field as it is encoded in the host's memory. Unfortunately, there are different methods to store 16- or 32-bits fields in memory. Some CPUs store the most significant byte of a 16-bits field in the first address of the field while others store the least significant byte at this location. When networked applications running on different CPUs exchange 16 bits fields, there are two possibilities to transfer them over the transport service :

  - send the most significant byte followed by the least significant byte
  - send the least significant byte followed by the most significant byte

The first possibility was named  `big-endian` in a note written by Cohen [Cohen1980]_ while the second was named `little-endian`. Vendors of CPUs that used `big-endian` in memory insisted on using `big-endian` encoding in networked applications while vendors of CPUs that used `little-endian` recommended the opposite. Several studies were written on the relative merits of each type of encoding, but the discussion became almost a religious issue [Cohen1980]_. Eventually, the Internet chose the `big-endian` encoding, i.e. multi-byte fields are always transmitted by sending the most significant byte first, :rfc:`791` refers to this encoding as the :term:`network-byte order`. Most libraries [#fhtonl]_ used to write networked applications contain functions to convert multi-byte fields from memory to the network byte order and the reverse.

Besides 16 and 32 bit words, some applications need to exchange data structures containing bit fields of various lengths. For example, a message may be composed of a 16 bits field followed by eight, one bit flags, a 24 bits field and two 8 bits bytes. Internet protocol specifications will define such a message by using a representation such as the one below. In this representation, each line corresponds to 32 bits and the vertical lines are used to delineate fields. The numbers above the lines indicate the bit positions in the 32-bits word, with the high order bit at position `0`.

.. figure:: /exercises/figures/message.png
   :align: center
   :scale: 100

   Message format

The message mentioned above will be transmitted starting from the upper 32-bits word in network byte order. The first field is encoded in 16 bits. It is followed by eight one bit flags (`A-H`), a 24 bits field whose high order byte is shown in the first line and the two low order bytes appear in the second line followed by two one byte fields. This ASCII representation is frequently used when defining binary protocols. We will use it for all the binary protocols that are discussed in this book.

Exercises
---------

Here are some exercises that will help you to learn how to use sockets.

.. inginious:: sockets-creating-a-socket


.. inginious:: sockets-creating-a-listening-socket


.. inginious:: sockets-sending-strings


.. inginious:: sockets-client-application


.. inginious:: sockets-server-application


During this course, you will be asked to implement a transport protocol running on Linux devices. To prepare yourself, try to implement the protocol described in the above tasks on your Linux personal machine. In addition to the previously produced code, you will need

 - to wrap the ``create_socket_and_send_message`` in a ``client.py`` script that can parse user arguments (Python's ``argparse`` module is useful for this) and appropriately call the wrapped function;
 - to wrap a ``recv_and_handle_message`` server function in a ``server.py`` script, similarly to what you have done with the client script.

As an example, here is what you could have to invoke your programs.

.. code-block:: bash

    # Put the server on port 10000 (ports below 1024 are privileged) and run it in the background
    $ python server.py :: 10000 &
    # Call the client and request an addition result, as an int
    $ python client.py --op + ::1 10000 1 3 5 7 9
    Result: 25
    # Request now a multiplication, but returned as a string
    $ python client.py --op '*' -s ::1 10000 1 3 5 7 9
    Result: 945

If you want to observe the packets exchanged over the network, use a packet dissector such as `wireshark`_ or `tcpdump`_, listen the loopback interface (``lo``) and filter UDP packets using port 10000 (``udp.port==10000`` in `wireshark`_, ``udp port 10000`` with `tcpdump`_).

.. rubric:: Footnotes


.. [#fhtonl] For example, in C, the ``htonl(3)`` (resp. ``ntohl(3)``) function from the standard library converts a 32-bits unsigned integer from the byte order used by the CPU to the network byte order (resp. from the network byte order to the CPU byte order). In Python, the ``struct`` module provides similar functionality. For example, ``struct.pack('!I', value)`` packs a 32-bit unsigned integer in network byte order (big-endian), where ``'!'`` specifies network byte order and ``'I'`` specifies an unsigned 32-bit integer. To unpack, use ``struct.unpack('!I', data)[0]``.



.. include:: /links.rst
