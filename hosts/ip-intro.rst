.. Copyright |copy| 2024 by `Olivier Bonaventure <https://perso.uclouvain.be/olivier.bonaventure>`_
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_



************   
IP addresses
************

Internet hosts such as laptops, smartphones, PCs, servers and various
Internet of Things (IoT) devices connect to the Internet through various
types of datalink layer technologies. Popular datalink layer
technologies include Wi-Fi, Ethernet, Bluetooth and the different types
of cellular network technologies such as 4G and 5G. Some of these technologies
will be discussed in the second part of this book. They have very specific
characteristics that we ignore in this part of the book. 

.. parler de frame et d'adresse ? peut-être pas


The Internet relies on a few architectural principles. First, all
the information that hosts exchange must be divided in :term:`IP packets`.
IP stands for the :term:`Internet Protocol`. This is the :term:`protocol`
or the send of rules than hosts apply when exchanging information. An IP packet is a variable-length sequence of bytes that contains two main
parts :

 - a header which contains control information specifying notably the source and the destination of the payload
 - a payload which contains the data to be exchanged


A second principle is that each host is identified by a unique :term:`IP address`. An :term:`IP address` is a fixed-length bit string that identifies
a host. Each Internet host has a unique :term:`IP address`. Each IP packet
contains both the IP address of the source or origin of the packet and
the IP address of the destination or recipient of the packet. The network
uses the destination address to deliver each packet to its final recipient.

Thanks to these architectural principles, any Internet host can send an IP
packet at any time to any other Internet host. A host could send a packet
to a server in America and shortly after another packet to a server in Australia or Africa. For a host, sending a packet is a cheap operation. It
creates a sequence of bytes containing the header and the payload and
then passes it to the network interface card. The other elements of the
network will handle the packet and deliver it to its final destination.

Two different versions of the Internet protocol are used on today's Internet.
The first one, named :term:`IP version 4` for historical reasons uses
32 bits long addresses. This version was designed when the Internet was a
research network that connected computers in universities and research
labs. At that time, having a maximum of :math:`2^{32}` IPv4 addresses was
not considered to be a severe limitation. Today, almost all the
available IPv4 addresses have been assigned to various organizations ranging
from enterprise or universities to :term:`Internet Service Providers`. An
IPv4 packet has a 20 bytes header which contains the source and destination
addresses of the packet and some control information. One of the control fields
of the IPv4 header is a 16 bits field that contains the total length of
the packet (header included). An IPv4 packet cannot be longer than 65535
bytes, header included. In practice hosts rarely send really long packets and
most IPv4 packets are shorter than about 1500 bytes.

The second deployed version of IP is :term:`IP version 6`. This version of
IP introduces several changes compared to IP version 4 that will be discussed
later. The most important one is the length of the IPv6 addresses.
An IPv6 address is 128 bits long. This implies that in theory, there
are :math:`2^128=340,282,366,920,938,463,463,374,607,431,768,211,456` unique IPv6 addresses. The number of IPv6 addresses, is
obviously much larger than the number of IPv4 addresses, and we do not
expect the IPv6 addressing space to become exhausted one day. An IPv6 packet
starts with a header of at least 40 bytes. It contains the source
and destination IPv6 addresses as well as a 16 bits long length field. This
implies that IPv6 packets cannot be longer than 65535 bytes. As for IPv4,
most observed IPv6 packets are shorter than about 1500 bytes.

