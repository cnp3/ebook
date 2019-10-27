.. Copyright |copy| 2013,2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_

Internet email protocols
========================

Many Internet protocols are ASCII_-based protocols where the client sends requests as one line of ASCII_ text terminated by `CRLF` and the server replies with one of more lines of ASCII_ text. Using such ASCII_ messages has several advantages compared to protocols that rely on binary encoded messages

   - the messages exchanged by the client and the server can be easily understood by a developer or network engineer by simply reading the messages
   - it is often easy to write a small prototype that implements a part of the protocol
   - it is possible to test a server manually by using telnet Telnet is a protocol that allows to obtain a terminal on a remote server. For this, telnet opens a TCP connection with the remote server on port 23. However, most `telnet` implementations allow the user to specify an alternate port as `telnet hosts port` When used with a port number as parameter, `telnet` opens a TCP connection to the remote host on the specified port. `telnet` can thus be used to test any server using an ASCII-based protocol on top of TCP. Note that if you need to stop a running `telnet` session, ``Ctrl-C`` will not work as it will be sent by `telnet` to the remote host over the TCP connection. On many `telnet` implementations you can type ``Ctrl-]`` to freeze the TCP connection and return to the telnet interface.


1. Use your preferred email tool to send an email message to yourself containing a single line of text. Most email tools have the ability to show the `source` of the message, use this function to look at the message that you sent and the message that you received. Can you find an explanation for all the lines that have been added to your single line email ?


2. The TCP protocol supports 65536 different ports numbers. Many of these port numbers have been reserved for some applications. The official repository of the reserved port numbers is maintained by the Internet Assigned Numbers Authority (IANA_) on http://www.iana.org/assignments/port-numbers [#fservices]_ Using this information, what is the default port number for the POP3 protocol ? Does it run on top of UDP or TCP ?

3. The Post Office Protocol (POP) is a rather simple protocol described in :rfc:`1939`. POP operates in three phases. The first phase is the authorization phase where the client provides a username and a password. The second phase is the transaction phase where the client can retrieve emails. The last phase is the update phase where the client finalizes the transaction. What are the main POP commands and their parameters ? When a POP server returns an answer, how can you easily determine whether the answer is positive or negative ? 

4. On smartphones, users often want to avoid downloading large emails over a slow wireless connection. How could a POP client only download emails that are smaller than 5 KBytes ?

.. rubric:: Footnotes


.. [#fservices] On Unix hosts, a subset of the port assignments is often placed in `/etc/services`



.. include:: /links.rst
