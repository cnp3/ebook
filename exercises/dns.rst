.. Copyright |copy| 2013 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


*****************
Application layer
*****************


The DNS
=======

The Domain Name System (DNS) plays a key role in the Internet today as it allows applications to use fully qualified domain names (FQDN) instead of IPv4 or IPv6 addresses. When using the DNS, it is important to remember the role of the different types of DNS records.

.. inginious:: dns-truefalse


.. inginious:: dns-records


Several software tools can be used to send queries to DNS servers. For this exercise, we use dig_ which is installed on most Unix/Linux systems.

A typical usage of dig is as follows:

.. code-block:: console

  dig @server -t type fqdn

where

 - `server` is the IP address or the name of a DNS server or resolver
 - `type` is the type of DNS record that is requested by the query such as `NS` for a nameserver, `A` for an IPv4 address, `AAAA` for an IPv6 address, `MX` for a mail relay, ...
 - `fqdn` is the fully qualified domain name being queried

dig_ also contains some additional parameters and flags that are described in the man page. Among these, the `+trace` flag allows to trace all requests that are sent when recursively contacting DNS servers.

1. What are the IP addresses of the resolvers that the `dig` implementation you are using relies on [#fdig]_ ?

2. What are the nameservers that are responsible for the `info` top-level domain ? Is it possible to use IPv6 to query them ?

3. What is the IPv6 address that corresponds to `www.computer-networking.info` ? Which type of DNS query does `dig` send to obtain this information ?


4. When run without any parameter, `dig` queries one of the root DNS servers and retrieves the list of the names of all root DNS servers. For technical reasons, there are only 13 different root DNS servers. This information is also available as a text file from http://www.internic.net/zones/named.root. What are the IPv6 addresses of all these servers?

5. Assume now that you are residing in a network where there is no DNS resolver and that you need to perform your query manually starting from the DNS root.

   - Use `dig` to send a query to one of these root servers to find the IPv6 address of the DNS server(s) (NS record) responsible for the `org` top-level domain
   - Use `dig` to send a query to one of these DNS servers to find the IP address of the DNS server(s) (NS record) responsible for `root-servers.org`
   - Continue until you find the server responsible for `www.root-servers.org`
   - What is the lifetime associated to this IPv6 address ?

6. Perform the same analysis for a popular website such as `www.google.com`. What is the lifetime associated to the corresponding IPv6 address ? If you perform the same request several times, do you always receive the same answer ? Can you explain why a lifetime is associated to the DNS replies ?

7. Use `dig` to find the mail relays used by the `uclouvain.be` and `student.uclouvain.be` domains. What is the `TTL` of these records ? Can you explain the preferences used by the `MX` records. You can find more information about the MX records in :rfc:`5321`.

8. When `dig` is run, the header section in its output indicates the `id` the DNS identifier used to send the query. Does your implementation of `dig` generates random identifiers ?

.. code-block:: text

	dig -t MX gmail.com

	; <<>> DiG 9.4.3-P3 <<>> -t MX gmail.com
	;; global options:  printcmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25718


9. A DNS implementation such as `dig`, and more importantly a name resolver such as bind_ or unbound_, always checks that the received DNS reply contains the same identifier as the DNS request that it sent. Why is this so important ?

   - Imagine an attacker who is able to send forged DNS replies to, for example, associate `www.bigbank.com` to his own IP address. How could he attack a DNS implementation that

     - sends DNS requests containing always the same identifier
     - sends DNS requests containing identifiers that are incremented by one after each request
     - sends DNS requests containing random identifiers

10. The DNS protocol can run over UDP and over TCP. Most DNS servers prefer to use UDP because it consumes fewer resources on the server. However, TCP is useful when a large answer is expected. Compare `time dig +tcp` and `time dig` to query a root DNS server. Is it faster to receive an answer via TCP or via UDP ?


Besides `dig`, another way to analyze the DNS is to look at packet traces with tools such as `wireshark <https://www.wireshark.org>`_ or `tcpdump <https://www.tcpdump.org>`_ These tools can capture packets in a network and also display and analyze their content. `Wireshark <https://www.wireshark.org>`_  provides a flexible Graphical User Interface that eases the analysis of the captured packets. The three questions below should help you to better understand the important fields of DNS messages.


.. inginious:: mcq-pkt-dns-1

.. inginious:: mcq-pkt-dns-2

.. inginious:: mcq-pkt-dns-3

The next three questions ask you to go one step further by predicting the values of specific fields in the DNS messages.

.. inginious:: pkt-dns-port

.. inginious:: pkt-dns-id

.. inginious:: pkt-dns-tcp

When a client requests the mapping of a domain name into an IP address to its local resolver, the resolver may need to query a large number of nameservers starting from the root nameserver. The three exercises below show packet traces collected while the resolver was resolving the following names: `www.example.com`, `www.google.com` and `www.computer-networking.info`. If you understand how the DNS operates, you should be able to correctly reorder those packet traces.

.. inginious:: pkt-dns-example

.. inginious:: pkt-dns-google

.. inginious:: pkt-dns-computernetworking



.. rubric:: Footnotes

.. [#fdig] On a Linux machine, the *Description* section of the `dig` man page tells you where `dig` finds the list of nameservers to query.

.. [#rs] You may obtain additional information about the root DNS servers from http://www.root-servers.org


.. include:: /links.rst
