.. Copyright |copy| 2024, 2025 by `Olivier Bonaventure <https://perso.uclouvain.be/olivier.bonaventure>`_
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


   
**************  
Internet hosts
**************

Internet hosts such as laptops, smartphones, PCs, servers, and various
Internet of Things (IoT) devices connect to the Internet through various
types of datalink layer technologies. Popular datalink layer
technologies include Wi-Fi, Ethernet, Bluetooth, and the different types
of cellular network technologies such as 4G and 5G. Some of these technologies will be discussed in the second part of this book. They have very specific
characteristics that we ignore in this part of the book. 

The Internet relies on a few architectural principles. First, all
the information that hosts exchange must be divided into :term:`IP packets`.
IP stands for the :term:`Internet Protocol`. This is the :term:`protocol`
or the set of rules that hosts apply when exchanging information. An IP packet is a variable-length sequence of bytes that contains two main
parts :

 - a header which contains control information specifying notably the source and the destination of the payload
 - a payload which contains the data to be exchanged


A second principle is that each host is identified by a unique :term:`IP address`. An :term:`IP address` is a fixed-length bit string that identifies
a host. Each Internet host has a unique :term:`IP address`. Each IP packet
contains both the IP address of the source or origin of the packet and
the IP address of the destination or recipient of the packet. The network
uses the destination address to deliver each packet to its final recipient.

Throughout this part, we will consider the Internet as a blackbox as shown in :numref:`fig-network-blackbox`. We will focus on hos hosts interact and will reveal how the network really operates in the second part of the book. 

   .. _fig-network-blackbox:
   .. tikz:: Internet hosts can exchange packets
      :libs: positioning, matrix, shapes
      \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
      
      \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }                                      
      \node[host] (B) {B}; 
      \node[cloud, draw, right=of B] (C) {Internet};

      \node[host, right=of C] (A) {A};          
      \path[draw,thick] (A) edge (C);
      \path[draw,thick] (B) edge (C);                                              

Thanks to these architectural principles, any Internet host can send an IP
packet at any time to any other Internet host. A host could send a packet
to a server in America and shortly after another packet to a server in Australia or Africa. For a host, sending a packet is a cheap operation. It
creates a sequence of bytes containing the header and the payload and
then passes it to the network interface card. The other elements of the
network will handle the packet and deliver it to its final destination.

Two different versions of the Internet protocol are used on today's Internet.
The first one, named :term:`IP version 4` uses 32-bit long addresses. IPv4 addresses are often represented in `dotted-decimal` format as a sequence of four integers separated by a `dot`. The first integer is the decimal representation of the most significant byte of the 32-bit IPv4 address, ... For example, 

 * ``1.2.3.4`` corresponds to ``00000001 00000010 00000011 00000100``
 * ``127.0.0.1`` corresponds to ``01111111 00000000 00000000 00000001``
 * ``255.255.255.255`` corresponds to ``1111111 1111111 11111111 1111111111``


.. todo:: Prepare ingenious exercises to convert IPv4 addresses in binary and vice versa
   
This version was designed when the Internet was a research network that connected computers in universities and research labs. At that time, having a maximum of :math:`2^{32}` IPv4 addresses was not considered to be a severe limitation. Today, almost all the available IPv4 addresses have been assigned to various organizations ranging from enterprises or universities to :term:`Internet Service Providers`.

An IPv4 address is composed of two parts : a `subnetwork identifier` and a `host identifier`. The `subnetwork identifier` is composed of the high-order bits of the address, and the host identifier is encoded in the low-order bits of the address. This is illustrated below with a 22-bit subnetwork identifier shown in blue and a 12-bit host identifier in red.


.. tikz:: The subnetwork (blue) and host identifiers (red) inside an IPv4 address
   :libs: positioning, matrix, arrows
	   
   \node[text=blue] {\texttt{01101111 10010101 111110}     \textit{\textcolor{red}{01 01001011}}};
	   
Flexibility in the IPv4 addressing architecture was added with the introduction of `variable-length subnets` in :rfc:`1519`. IPv4 supports `variable-length` subnets where the subnet identifier can be any size, from 1 to 31 bits. `Variable-length` subnets allow the network operators to use a subnet that better matches the number of hosts that are placed inside the subnet. A subnet identifier or IPv4 prefix is usually [#fnetmask]_ represented as A.B.C.D/p where A.B.C.D is the network address obtained by concatenating the subnet identifier with a host identifier containing only 0 and p is the length of the subnet identifier in bits. The table below provides examples of IP subnets.

============== 	==========  ============  ===============
Subnet      	Number of   Smallest      Highest
	    	addresses   address	  address
============== 	==========  ============  ===============
10.0.0.0/8  	16,777,216  10.0.0.0      10.255.255.255	
192.168.0.0/16	65,536	    192.168.0.0   192.168.255.255
198.18.0.0/15	131,072	    198.18.0.0 	  198.19.255.255
192.0.2.0/24	256	    192.0.2.0 	  192.0.2.255
10.0.0.0/30	4	    10.0.0.0	  10.0.0.3
10.0.0.0/31	2	    10.0.0.0	  10.0.0.1
============== 	==========  ============  ===============

.. note:: Special IPv4 addresses

   Most unicast IPv4 addresses can appear as source and destination addresses in packets on the global Internet. However, it is worth noting that some blocks of IPv4 addresses have a special usage, as described in RFC :`5735`. These include :

  - `0.0.0.0/8`, which is reserved for self-identification. A common address in this block is `0.0.0.0`, which is sometimes used when a host boots and does not yet know its IPv4 address.
  - `127.0.0.0/8`, which is reserved for loopback addresses. Each host implementing IPv4 must have a loopback interface (that is not attached to a datalink layer). By convention, IPv4 address `127.0.0.1` is assigned to this interface. This allows processes running on a host to use TCP/IP to contact other processes running on the same host. This can be very useful for testing purposes. 
  - `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16` are reserved for private networks that are not directly attached to the Internet. These addresses are often called private addresses or :rfc:`1918` addresses. 
  - `169.254.0.0/16` is used for link-local addresses :rfc:`3927`. Some hosts use an address in this block when they are connected to a network that does not allocate addresses as expected.
 - `192.0.2.0/24`, `198.51.100.0/24`, and `203.0.113.0/24` are reserved for use in documentation. These addresses cannot be used on the public Internet and should not be accepted by hosts. This book should ideally use these addresses when providing examples.


The unit of information for IPv4 is the :term:`packet`. An IPv4 packet has a 20-byte header which contains the source and destination addresses of the packet and some control information. One of the control fields of the IPv4 header is a 16-bit field that contains the total length of
the packet (header included). An IPv4 packet cannot be longer than 65535
bytes, header included. In practice, hosts rarely send really long packets and
most IPv4 packets are shorter than about 1500 bytes.

.. figure:: /pkt/ipv4.*
   :align: center
   :scale: 80
    
   The IP version 4 header

The second deployed version of IP is :term:`IP version 6`. This version of
IP introduces several changes compared to IP version 4 that will be discussed
later. The most important one is the length of the IPv6 addresses.
An IPv6 address is 128 bits long. This implies that in theory, there
are :math:`2^128=340,282,366,920,938,463,463,374,607,431,768,211,456` unique IPv6 addresses. The number of IPv6 addresses is
much larger than the number of IPv4 addresses, and we do not
expect the IPv6 addressing space to become exhausted one day.


.. note:: Textual representation of IPv6 addresses

   It is sometimes necessary to write IPv6 addresses in text format, e.g. when manually configuring addresses or for documentation purposes. The preferred format for writing IPv6 addresses is ``x:x:x:x:x:x:x:x``, where the ``x`` 's are hexadecimal digits representing the eight 16-bit parts of the address. Here are a few examples of IPv6 addresses :

  - ``abcd:ef01:2345:6789:abcd:ef01:2345:6789``
  - ``2001:db8:0:0:8:800:200c:417a``
  - ``fe80:0:0:0:219:e3ff:fed7:1204``

 IPv6 addresses often contain a long sequence of bits set to ``0``. In this case, a compact notation has been defined. With this notation, `::` is used to indicate one or more groups of 16-bit blocks containing only bits set to `0`. For example,

  - ``2001:db8:0:0:8:800:200c:417a``  is represented as  ``2001:db8::8:800:200c:417a``
  - ``ff01:0:0:0:0:0:0:101``   is represented as ``ff01::101``
  - ``0:0:0:0:0:0:0:1`` is represented as ``::1``
  - ``0:0:0:0:0:0:0:0`` is represented as ``::``

 An IPv6 prefix can be represented as `address/length`, where `length` is the length of the prefix in bits. For example, the three notations below correspond to the same IPv6 prefix :

  - ``2001:0db8:0000:cd30:0000:0000:0000:0000`` / ``60``
  - ``2001:0db8::cd30:0:0:0:0`` / ``60``
  - ``2001:0db8:0:cd30::`` / ``60``



    
An IPv6 packet
starts with a header of at least 40 bytes. It contains the source
and destination IPv6 addresses as well as a 16-bit-long length field. This
implies that IPv6 packets cannot be longer than 65535 bytes. As for IPv4,
most observed IPv6 packets are shorter than about 1500 bytes.

The standard IPv6 header defined in :rfc:`2460` occupies 40 bytes and contains 8 different fields, as shown in the figure below. The structure of this packet will be explained in more detail in the second part of this book.


.. figure:: /pkt/ipv6.*
   :align: center
   :scale: 80

   The IP version 6 header
