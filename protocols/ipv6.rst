.. Copyright |copy| 2010, 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


*****************
The network layer
*****************

The main objective of the network layer is to allow hosts, connected to different networks, to exchange information through intermediate systems called :term:`router`. The unit of information in the network layer is called a :term:`packet`.

    .. tikz:: The network layer in the reference model
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,<->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=8em}, }

        \node[elem] (pm) {Physical layer};
        \node[elem, above=0em of pm] (dm) {Datalink};
        \node[elem, above=0em of dm] (nm) {\color{blue}Network};

        \node[elem, left=8em of pm] (pl) {Physical layer};
        \node[elem, above=0em of pl] (dl) {Datalink};
        \node[elem, above=0em of dl] (nl) {\color{blue}Network};
        \node[elem, above=0em of nl] (tl) {Transport};

        \node[elem, right=8em of pm] (pr) {Physical layer};
        \node[elem, above=0em of pr] (dr) {Datalink};
        \node[elem, above=0em of dr] (nr) {\color{blue}Network};
        \node[elem, above=0em of nr] (tr) {Transport};

        \draw[rectangle, thick, draw, fill=gray!20] ([xshift=1em, yshift=-1em]pl.south) rectangle ([xshift=-1em]pm.south);
        \draw[rectangle, thick, draw, fill=gray!80] ([xshift=1em, yshift=-1em]pm.south) rectangle ([xshift=-1em]pr.south);

        \draw[arrow, blue] (nl.east) -- (nm.west) node [midway, above] {Packets};
        \draw[arrow, blue] (nm.east) -- (nr.west) node [midway, above] {Packets};

Before explaining the network layer in detail, it is useful to begin by analyzing the service provided by the `datalink` layer. There are many variants of the datalink layer. Some provide a connection-oriented service while others provide a connectionless service. In this section, we focus on connectionless datalink layer services as they are the most widely used. Using a connection-oriented datalink layer causes some problems that are beyond the scope of this chapter. See :rfc:`3819` for a discussion on this topic.

    .. tikz:: The point-to-point datalink layer
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,<->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=8em}, }

        \node[elem] (pm) {Physical};
        \node[elem, above=0em of pm] (dm) {\color{blue}Datalink};
        \node[elem, above=0em of dm] (nm) {Network};

        \node[elem, left=8em of pm] (pl) {Physical};
        \node[elem, above=0em of pl] (dl) {\color{blue}Datalink};
        \node[elem, above=0em of dl] (nl) {Network};

        \draw[rectangle, thick, draw, fill=gray!20] ([xshift=1em, yshift=-1em]pl.south) rectangle ([xshift=-1em]pm.south);

        \draw[arrow, blue] (dl.east) -- (dm.west) node [midway, above] {Frames};

There are three main types of datalink layers. The simplest datalink layer is when there are only two communicating systems that are directly connected through the physical layer. Such a datalink layer is used when there is a point-to-point link between the two communicating systems. The two systems can be hosts or routers. :abbr:`PPP (Point-to-Point Protocol)`, defined in :rfc:`1661`, is an example of such a point-to-point datalink layer. Datalink layers exchange `frames` and a datalink :term:`frame` sent by a datalink layer entity on the left is transmitted through the physical layer, so that it can reach the datalink layer entity on the right. Point-to-point datalink layers can either provide an unreliable service (frames can be corrupted or lost) or a reliable service (in this case, the datalink layer includes retransmission mechanisms similar to the ones used in the transport layer). The unreliable service is frequently used above physical layers (e.g. optical fiber, twisted pairs) having a low bit error ratio while reliability mechanisms are often used in wireless networks to recover locally from transmission errors.

The second type of datalink layer is the one used in Local Area Networks (LAN). Conceptually, a LAN is a set of communicating devices such that any two devices can directly exchange frames through the datalink layer. Both hosts and routers can be connected to a LAN. Some LANs only connect a few devices, but there are LANs that can connect hundreds or even thousands of devices.

.. figure:: /protocols/figures/simple-lan.png
   :align: center
   :scale: 80

   A local area network

In the next chapter, we describe the organization and the operation of Local Area Networks. An important difference between the point-to-point datalink layers and the datalink layers used in LANs is that in a LAN, each communicating device is identified by a unique `datalink layer address`. This address is usually embedded in the hardware of the device and different types of LANs use different types of datalink layer addresses. Most LANs use 48-bits long addresses that are usually called `MAC` addresses. A communicating device attached to a LAN can send a datalink frame to any other communicating device that is attached to the same LAN. Most LANs also support special broadcast and multicast datalink layer addresses. A frame sent to the broadcast address of the LAN is delivered to all communicating devices that are attached to the LAN. The multicast addresses are used to identify groups of communicating devices. When a frame is sent towards a multicast datalink layer address, it is delivered by the LAN to all communicating devices that belong to the corresponding group.

.. index:: NBMA, Non-Broadcast Multi-Access Networks

The third type of datalink layers are used in Non-Broadcast Multi-Access (NBMA) networks. These networks are used to interconnect devices like a LAN. All devices attached to an NBMA network are identified by a unique datalink layer address. However, and this is the main difference between an NBMA network and a traditional LAN, the NBMA service only supports unicast. The datalink layer service provided by an NBMA network supports neither broadcast nor multicast.

Unfortunately no datalink layer is able to send frames of unlimited side. Each datalink layer is characterized by a maximum frame size. There are more than a dozen different datalink layers and unfortunately most of them use a different maximum frame size. The network layer must cope with the heterogeneity of the datalink layer.


IP version 6
============

In the late 1980s and early 1990s the growth of the Internet was causing several operational problems on routers. Many of these routers had a single CPU and up to 1 MByte of RAM to store their operating system, packet buffers and routing tables. Given the rate of allocation of IPv4 prefixes to companies and universities willing to join the Internet, the routing tables where growing very quickly and some feared that all IPv4 prefixes would quickly be allocated. In 1987, a study cited in :rfc:`1752`, estimated that there would be 100,000 networks in the near future. In August 1990, estimates indicated that the class B space would be exhausted by March 1994.
Two types of solution were developed to solve this problem. The first short term solution was the introduction of Classless Inter Domain Routing (:term:`CIDR`). A second short term solution was the Network Address Translation (:term:`NAT`) mechanism, defined in :rfc:`1631`. NAT allowed multiple hosts to share a single public IPv4 address.


.. spelling::

   IPng

However, in parallel with these short-term solutions, which have allowed the IPv4 Internet to continue to be usable until now, the Internet Engineering Task Force started working on developing a replacement for IPv4. This work started with an open call for proposals, outlined in :rfc:`1550`. Several groups responded to this call with proposals for a next generation Internet Protocol (IPng) :

 * TUBA proposed in :rfc:`1347` and :rfc:`1561`
 * PIP proposed in :rfc:`1621`
 * SIPP proposed in :rfc:`1710`

The IETF decided to pursue the development of IPng based on the SIPP proposal. As IP version `5` was already used by the experimental ST-2 protocol defined in :rfc:`1819`, the successor of IP version 4 is IP version 6. The initial IP version 6 defined in :rfc:`1752` was designed based on the following assumptions :

 * IPv6 addresses are encoded as a 128 bits field
 * The IPv6 header has a simple format that can easily be parsed by hardware devices
 * A host should be able to configure its IPv6 address automatically
 * Security must be part of IPv6

.. note:: The IPng address size

   When the work on IPng started, it was clear that 32 bits was too small to encode an IPng address and all proposals used longer addresses. However, there were many discussions about the most suitable address length. A first approach, proposed by SIPP in :rfc:`1710`, was to use 64 bit addresses. A 64 bits address space was 4 billion times larger than the IPv4 address space and, furthermore, from an implementation perspective, 64 bit CPUs were being considered and 64 bit addresses would naturally fit inside their registers. Another approach was to use an existing address format. This was the TUBA proposal (:rfc:`1347`) that reuses the ISO CLNP 20 bytes addresses. The 20 bytes addresses provided room for growth, but using ISO CLNP was not favored by the IETF partially due to political reasons, despite the fact that mature CLNP implementations were already available. 128 bits appeared to be a reasonable compromise at that time.

IPv6 addressing architecture
----------------------------

The experience of IPv4 revealed that the scalability of a network layer protocol heavily depends on its addressing architecture. The designers of IPv6 spent a lot of effort defining its addressing architecture :rfc:`3513`. All IPv6 addresses are 128 bits wide. This implies that there are :math:`340,282,366,920,938,463,463,374,607,431,768,211,456 (3.4 \times 10^{38})` different IPv6 addresses. As the surface of the Earth is about 510,072,000 :math:`km^2`, this implies that there are about :math:`6.67 \times 10^{23}` IPv6 addresses per square meter on Earth. Compared to IPv4, which offers only 8 addresses per square kilometer, this is a significant improvement on paper.

.. note:: Textual representation of IPv6 addresses

   It is sometimes necessary to write IPv6 addresses in text format, e.g. when manually configuring addresses or for documentation purposes. The preferred format for writing IPv6 addresses is ``x:x:x:x:x:x:x:x``, where the ``x`` 's are hexadecimal digits representing the eight 16-bit parts of the address. Here are a few examples of IPv6 addresses :

  - ``abcd:ef01:2345:6789:abcd:ef01:2345:6789``
  - ``2001:db8:0:0:8:800:200c:417a``
  - ``fe80:0:0:0:219:e3ff:fed7:1204``

 IPv6 addresses often contain a long sequence of bits set to ``0``. In this case, a compact notation has been defined. With this notation, `::` is used to indicate one or more groups of 16 bits blocks containing only bits set to `0`. For example,

  - ``2001:db8:0:0:8:800:200c:417a``  is represented as  ``2001:db8::8:800:200c:417a``
  - ``ff01:0:0:0:0:0:0:101``   is represented as ``ff01::101``
  - ``0:0:0:0:0:0:0:1`` is represented as ``::1``
  - ``0:0:0:0:0:0:0:0`` is represented as ``::``

 An IPv6 prefix can be represented as `address/length`, where `length` is the length of the prefix in bits. For example, the three notations below correspond to the same IPv6 prefix :

  - ``2001:0db8:0000:cd30:0000:0000:0000:0000`` / ``60``
  - ``2001:0db8::cd30:0:0:0:0`` / ``60``
  - ``2001:0db8:0:cd30::`` / ``60``

IPv6 supports unicast, multicast and anycast addresses. An IPv6 unicast address is used to identify one datalink-layer interface on a host. If a host has several datalink layer interfaces (e.g. an Ethernet interface and a WiFi interface), then it needs several IPv6 addresses. In general, an IPv6 unicast address is structured as shown in the figure below.

    .. tikz:: Structure of IPv6 unicast addresses
        :libs: positioning, matrix, arrows

        \tikzstyle{biarrow} = [thick,<->,>=stealth]
        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=8em}, }

        \node[elem] (gpr) {Global routing prefix};
        \node[elem, right=0em of gpr] (sid) {Subnet ID};
        \node[elem, right=0em of sid] (iid) {Interface ID};

        \draw[biarrow] ([yshift=1em] gpr.north west) -- ([yshift=1em] gpr.north east) node [midway, above] {N bits};
        \draw[biarrow] ([yshift=1em] sid.north west) -- ([yshift=1em] sid.north east) node [midway, above] {M bits};
        \draw[biarrow] ([yshift=1em] iid.north west) -- ([yshift=1em] iid.north east) node [midway, above] {128 - N - M bits};
        \draw[biarrow] ([yshift=4em] gpr.north west) -- ([yshift=4em] iid.north east) node [midway, above] {128 bits};

        \draw[arrow] (gpr.south) -- ([yshift=-2em]gpr.south) node [below, font=\scriptsize, align=center] {Can be used to identify the\\ISP responsible for this address};
        \draw[arrow] (sid.south) -- ([yshift=-4em]sid.south) node [below, font=\scriptsize, align=center] {A subnet in this ISP or\\a customer of this ISP};
        \draw[arrow] (iid.south) -- ([yshift=-2em]iid.south) node [below, font=\scriptsize, align=center] {Usually 64 bits\\Based on MAC address};


An IPv6 unicast address is composed of three parts :

 #. A `global routing prefix` that is assigned to the Internet Service Provider that owns this block of addresses
 #. A `subnet identifier` that identifies a customer of the ISP
 #. An `interface identifier` that identifies a particular interface on a host

The subnet identifier plays a key role in the scalability of network layer addressing architecture. An important point to be defined in a network layer protocol is the allocation of the network layer addresses. A naive allocation scheme would be to provide an address to each host when the host is attached to the Internet on a first come first served basis. With this solution, a host in Belgium could have address ``2001:db8::1`` while another host located in Africa would use address ``2001:db8::2``. Unfortunately, this would force all routers on the Internet to maintain one route towards each host. In the network layer, scalability is often a function of the number of routes stored on the router. A network will usually work better if its routers store fewer routes and network administrators usually try to minimize the number of routes that are known by their routers. For this, they often divide their network prefix in smaller blocks. For example, consider a company with three campuses, a large one and two smaller ones. The network administrator would probably divide his block of addresses as follows :

 - the bottom half is used for the large campus
 - the top half is divided in two smaller blocks, one for each small campus

Inside each campus, the same division can be done, for example on a per building basis, starting from the buildings that host the largest number of nodes, e.g. the company datacenter. In each building, the same division can be done on a per floor basis, ... The advantage of such a hierarchical allocation of the addresses is that the routers in the large campus only need one route to reach a router in the smaller campus. The routers in the large campus would know more routes about the buildings in their campus, but they do not need to know the details of the organization of each smaller campus.

To preserve the scalability of the routing system, it is important to minimize the number of routes that are stored on each router. A router cannot store and maintain one route for each of the almost 1 billion hosts that are connected to today's Internet. Routers should only maintain routes towards blocks of addresses and not towards individual hosts. For this, hosts are grouped in `subnets` based on their location in the network. A typical subnet groups all the hosts that are part of the same enterprise. An enterprise network is usually composed of several LANs interconnected by routers. A small block of addresses from the Enterprise's block is usually assigned to each LAN.

In today's deployments, interface identifiers are always 64 bits wide. This implies that while there are :math:`2^{128}` different IPv6 addresses, they must be grouped in :math:`2^{64}` subnets. This could appear as a waste of resources, however using 64 bits for the host identifier allows IPv6 addresses to be auto-configured and also provides some benefits from a security point of view, as explained in section ICMPv6_.


.. index:: Provider Independent address
.. index:: Provider Aggregatable address

In practice, there are several types of IPv6 unicast address. Most of the `IPv6 unicast addresses <http://www.iana.org/assignments/ipv6-address-space/ipv6-address-space.xhtml>`_ are allocated in blocks under the responsibility of IANA_. The current IPv6 allocations are part of the `2000::/3` address block. Regional Internet Registries (RIR) such as RIPE_ in Europe,  ARIN_ in North-America or AfriNIC in Africa have each received a `block of IPv6 addresses <http://www.iana.org/assignments/ipv6-unicast-address-assignments/ipv6-unicast-address-assignments.xhtml>`_ that they sub-allocate to Internet Service Providers in their region.  The ISPs then sub-allocate addresses to their customers.

When considering the allocation of IPv6 addresses, two types of address allocations are often distinguished. The RIRs allocate `provider-independent (PI)` addresses. PI addresses are usually allocated to Internet Service Providers and large companies that are connected to at least two different ISPs [CSP2009]_. Once a PI address block has been allocated to a company, this company can use its address block with the provider of its choice and change its provider at will. Internet Service Providers allocate `provider-aggregatable (PA)` address blocks from their own PI address block to their customers. A company that is connected to only one ISP should only use PA addresses. The drawback of PA addresses is that when a company using a PA address block changes its provider, it needs to change all the addresses that it uses. This can be a nightmare from an operational perspective and many companies are lobbying to obtain `PI` address blocks even if they are small and connected to a single provider. The typical size of the IPv6 address blocks are :

 - ``/32`` for an Internet Service Provider
 - ``/48`` for a single company
 - ``/56`` for small user sites
 - ``/64`` for a single user (e.g. a home user connected via ADSL)
 - ``/128`` in the rare case when it is known that no more than one host will be attached

.. spelling::

   Belnet
   ULg

There is one difficulty with the utilization of these IPv6 prefixes. Consider Belnet, the Belgian research  ISP that has been allocated the ``2001:6a8::/32`` prefix. Universities are connected to Belnet. UCLouvain uses prefix ``2001:6a8:3080::/48`` while the University of Liege uses ``2001:6a8:2d80::/48``. A commercial ISP uses prefix ``2a02:2788::/32``. Both Belnet and the commercial ISP are connected to the global Internet.

.. figure:: /protocols/figures/belnet.png
   :align: center
   :scale: 70


The Belnet network advertises prefix ``2001:6a8::/32`` that includes the prefixes from both UCLouvain and ULg. These two subnetworks can be easily reached from any internet connected host. After a few years, UCLouvain decides to increase the redundancy of its Internet connectivity and buys transit service from ISP1. A direct link between UCLouvain and the commercial ISP appears on the network and UCLouvain expects to receive packets from both Belnet and the commercial ISP.


Now, consider how a router inside ``alpha.com`` would reach a host in the ``UCLouvain`` network. This router has two routes towards ``2001:6a8:3080::1``. The first one, for prefix ``2001:6a8:3080::/48`` is via the direct link between the commercial ISP and UCLouvain. The second one, for prefix ``2001:6a8::/32`` is via the Internet and Belnet. Since :rfc:`1519` when a router knows several routes towards the same destination address, it must forward packets along the route having the longest prefix length. In the case of ``2001:6a8:3080::1``, this is the route ``2001:6a8:3080::/48`` that is used to forward the packet. This forwarding rule is called the `longest prefix match` or the `more specific match`. All IP routers implement this forwarding rule.

To understand the `longest prefix match` forwarding, consider the IPv6 routing below.

.. code-block:: console

   Destination                          Gateway
   ::/0                                 fe80::dead:beef
   ::1                                  ::1
   2a02:2788:2c4:16f::/64               eth0
   2001:6a8:3080::/48                   fe80::bad:cafe
   2001:6a8:2d80::/48                   fe80::bad:bad
   2001:6a8::/32                        fe80::aaaa:bbbb


With the longest match rule, the route ``::/0`` plays a particular role. As this route has a prefix length of `0` bits, it matches all destination addresses. This route is often called the `default` route.

 - a packet with destination ``2a02:2788:2c4:16f::1`` received by router `R` is destined to a host on interface ``eth0`` .
 - a packet with destination ``2001:6a8:3080::1234`` matches three routes : ``::/0``, ``2001:6a8::/32`` and ``2001:6a8:3080::/48``. The packet is forwarded via gateway ``fe80::bad:cafe``
 - a packet with destination ``2001:1890:123a::1:1e`` matches one route : ``::/0``. The packet is forwarded via ``fe80::dead:beef``
 - a packet with destination ``2001:6a8:3880:40::2`` matches two routes : ``2001:6a8::/32`` and ``::/0``. The packet is forwarded via ``fe80::aaaa:bbbb``

.. spelling::

   trie

The longest prefix match can be implemented by using different data structures One possibility is to use a trie. Details on how to implement efficient packet forwarding algorithms may be found in [Varghese2005]_.


.. index:: Unique Local Unicast IPv6

For the companies that want to use IPv6 without being connected to the IPv6 Internet, :rfc:`4193` defines the `Unique Local Unicast (ULA)` addresses (``fc00::/7``). These ULA addresses play a similar role as the private IPv4 addresses defined in :rfc:`1918`. However, the size of the ``fc00::/7`` address block allows ULA to be much more flexible than private IPv4 addresses.

.. index:: ::1, ::

Furthermore, the IETF has reserved some IPv6 addresses for a special usage. The two most important ones are :

 - ``0:0:0:0:0:0:0:1`` (``::1`` in compact form) is the IPv6 loopback address. This is the address of a logical interface that is always up and running on IPv6 enabled hosts.
 - ``0:0:0:0:0:0:0:0`` (``::`` in compact form) is the unspecified IPv6 address. This is the IPv6 address that a host can use as source address when trying to acquire an official address.

.. index:: Link Local address

The last type of unicast IPv6 addresses are the `Link Local Unicast` addresses. These addresses are part of the `fe80::/10` address block and are defined in :rfc:`4291`. Each host can compute its own link local address by concatenating the `fe80::/64` prefix with the 64 bits identifier of its interface. Link local addresses can be used when hosts that are attached to the same link (or local area network) need to exchange packets. They are used notably for address discovery and auto-configuration purposes. Their usage is restricted to each link and a router cannot forward a packet whose source or destination address is a link local address. Link local addresses have also been defined for IPv4 :rfc:`3927`. However, the IPv4 link local addresses are only used when a host cannot obtain a regular IPv4 address, e.g. on an isolated LAN.

    .. tikz:: IPv6 link local address structure
        :libs: positioning, matrix, arrows

        \tikzstyle{biarrow} = [thick,<->,>=stealth]
        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=3em}, }

        \node[elem] (gpr) {FE80};
        \node[elem, right=0em of gpr] (sid) {0000000000.....0000000000};
        \node[elem, right=0em of sid,minimum width=12em] (iid) {Interface ID};

        \draw[biarrow] ([yshift=1em] gpr.north west) -- ([yshift=1em] gpr.north east) node [midway, above] {10 bits};
        \draw[biarrow] ([yshift=1em] sid.north west) -- ([yshift=1em] sid.north east) node [midway, above] {54 bits};
        \draw[biarrow] ([yshift=1em] iid.north west) -- ([yshift=1em] iid.north east) node [midway, above] {64 bits};
        \draw[biarrow] ([yshift=4em] gpr.north west) -- ([yshift=4em] iid.north east) node [midway, above] {128 bits};

.. note:: All IPv6 hosts have several addresses

   An important consequence of the IPv6 unicast addressing architecture and the utilization of link-local addresses is that each IPv6 host has several IPv6 addresses. This implies that all IPv6 stacks must be able to handle multiple IPv6 addresses.



The addresses described above are unicast addresses. These addresses are used to identify (interfaces on) hosts and routers. They can appear as source and destination addresses in the IPv6 packets. When a host sends a packet towards a unicast address, this packet is delivered by the network to its final destination. There are situations, such as when delivering video or television signal to a large number of receivers, where it is useful to have a network that can efficiently deliver the same packet to a large number of receivers. This is the `multicast` service. A multicast service can be provided in a LAN. In this case, a multicast address identifies a set of receivers and each frame sent towards this address is delivered to all receivers in the group. Multicast can also be used in a network containing routers and hosts. In this case, a multicast address identifies also a group of receivers and the network delivers efficiently each multicast packet to all members of the group. Consider for example the network below.

    .. tikz::
       :libs: positioning

       \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \node[host] (A) {A};
       \node[router, below =of A] (R1) {R1};
       \node[router, below right=of R1] (R3) {R3};
       \node[router, below left=of R1] (R2) {R2};
       \node[host, left=of R2] (B) {B};
       \node[host, right=of R3] (C) {C};
       \node[router, below left=of R3] (R4) {R4};
       \node[host, left =of R4] (D) {D};
       \draw[black] (A) -- (R1);
       \draw[black] (B) -- (R2);
       \draw[black] (C) -- (R3);
       \draw[black] (D) -- (R4);
       \draw[black] (R1) -- (R3);
       \draw[black] (R1) -- (R2);
       \draw[black] (R3) -- (R4);


Assume that ``B`` and ``D`` are part of a multicast group. If ``A`` sends a multicast packet towards this group, then ``R1`` will replicate the packet to forward it to ``R2`` and ``R3``. ``R2`` would forward the packet towards ``B``. ``R3`` would forward the packet towards ``R4`` that would deliver it to ``D``.

Finally, :rfc:`4291` defines the structure of the IPv6 multicast addresses [#fmultiiana]_. This structure is depicted in the figure below.

    .. tikz:: IPv6 multicast address structure
        :libs: positioning, matrix, arrows

        \tikzstyle{biarrow} = [thick,<->,>=stealth]
        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=4em}, }

        \node[elem] (ones) {11111111};
        \node[elem, right=0em of ones] (f) {Flags};
        \node[elem, right=0em of f] (s) {Scope};
        \node[elem, right=0em of s, minimum width=16em] (g) {Group ID};

        \draw[biarrow] ([yshift=1em] ones.north west) -- ([yshift=1em] ones.north east) node [midway, above] {8 bits};
        \draw[biarrow] ([yshift=1em] f.north west) -- ([yshift=1em] f.north east) node [midway, above] {4 bits};
        \draw[biarrow] ([yshift=1em] s.north west) -- ([yshift=1em] s.north east) node [midway, above] {4 bits};
        \draw[biarrow] ([yshift=1em] g.north west) -- ([yshift=1em] g.north east) node [midway, above] {112 bits};
        \draw[biarrow] ([yshift=4em] ones.north west) -- ([yshift=4em] g.north east) node [midway, above] {128 bits};

        \draw[arrow] (f.south) -- ([yshift=-2em]f.south west) node [below, font=\scriptsize, align=center] {Permanent address\\Temporary address};
        \draw[arrow] (s.south) -- ([yshift=-2em]s.south east) node [below, font=\scriptsize, align=center] {Node local-scope\\Link-local scope\\Subnet local-scope\\Site local-scope\\Organization local-scope\\Global scope};

The low order 112 bits of an IPv6 multicast address are the group's identifier. The high order bits are used as a marker to distinguish multicast addresses from unicast addresses. Notably, the 4-bit `Flags` field indicates whether the address is temporary or permanent. Finally, the `Scope` field indicates the boundaries of the forwarding of packets destined to a particular address. A link-local scope indicates that a router should not forward a packet destined to such a multicast address. An organization local-scope indicates that a packet sent to such a multicast destination address should not leave the organization. Finally the global scope is intended for multicast groups spanning the global Internet.

Among these addresses, some are well known. For example, all hosts automatically belong to the ``ff02::1`` multicast group while all routers automatically belong to the ``ff02::2`` multicast group. A detailed discussion of IPv6 multicast is outside the scope of this chapter.

.. _IPv6Packet:

IPv6 packet format
------------------

The IPv6 packet format was heavily inspired by the packet format proposed for the SIPP protocol in :rfc:`1710`. The standard IPv6 header defined in :rfc:`2460` occupies 40 bytes and contains 8 different fields, as shown in the figure below.

.. figure:: /pkt/ipv6.png
   :align: center
   :scale: 120

   The IP version 6 header (:rfc:`2460`)

Apart from the source and destination addresses, the IPv6 header contains the following fields :

 - `Version` : a 4 bits field set to `6` and intended to allow IP to evolve in the future if needed
 - `Traffic class` : this 8 bits field indicates the type of service expected by this packet and contains the ``CE`` and ``ECT`` flags that are used by `Explicit Congestion Notification`
 - `Flow Label` : this field was initially intended to be used to tag packets belonging to the same `flow`. A recent document, :rfc:`6437` describes some possible usages of this field, but it is too early to tell whether it will be really used.
 - `Payload Length` : this is the size of the packet payload in bytes. As the length is encoded as a 16 bits field, an IPv6 packet can contain up to 65535 bytes of payload.
 - `Next Header` : this 8-bit field indicates the type [#fianaprotocol]_ of header that follows the IPv6 header. It can be a transport layer header (e.g. `6` for TCP or `17` for UDP) or an IPv6 option.
 - `Hop Limit` : this 8-bit field indicates the number of routers that can forward the packet. It is decremented by one by each router and prevents packets from looping forever inside the network.


It is interesting to note that there is no checksum inside the IPv6 header. This is mainly because all datalink layers and transport protocols include a checksum or a CRC to protect their frames/segments against transmission errors. Adding a checksum in the IPv6 header would have forced each router to recompute the checksum of all packets, with limited benefit in detecting errors. In practice, an IP checksum allows for catching errors that occur inside routers (e.g. due to memory corruption) before the packet reaches its destination. However, this benefit was found to be too small given the reliability of current memories and the cost of computing the checksum on each router [#fipv4checksum]_.

When a host receives an IPv6 packet, it needs to determine which transport protocol (UDP, TCP, SCTP, ...) needs to handle the payload of the packet. This is the first role of the `Next header` field. The IANA_ which manages the allocation of Internet resources and protocol parameters, maintains an official list of transport protocols [#fianaprotocol]_. The following protocol numbers are reserved :

 - ``TCP`` uses `Next Header` number ``6``
 - ``UDP`` uses `Next Header` number ``17``
 - ``SCTP`` uses `Next Header` number ``132``

For example, an IPv6 packet that contains an TCP segment would appear as shown in the figure below.

.. figure:: /pkt/ipv6-tcp.png
   :scale: 120

   An IPv6 packet containing an TCP segment

.. _IPv6Options:

However, the `Next header` has broader usages than simply indicating the transport protocol which is responsible for the packet payload. An IPv6 packet can contain a chain of headers and the last one indicates the transport protocol that is responsible for the packet payload. Supporting a chain of headers is a clever design from an extensibility viewpoint. As we will see, this chain of headers has several usages.

:rfc:`2460` defines several types of IPv6 extension headers that could be added to an IPv6 packet :

  - `Hop-by-Hop Options` header. This option is processed by routers and hosts.
  - `Destination Options` header. This option is processed only by hosts.
  - `Routing` header. This option is processed by some nodes.
  - `Fragment` header. This option is processed only by hosts.
  - `Authentication` header. This option is processed only by hosts.
  - `Encapsulating Security Payload`. This option is processed only by hosts.

The last two headers are used to add security above IPv6 and implement IPSec. They are described in :rfc:`2402` and :rfc:`2406` and are outside the scope of this document.

The `Hop-by-Hop Options` header was designed to make IPv6 easily extensible. In theory, this option could be used to define new fields that were not foreseen when IPv6 was designed. It is intended to be processed by both routers and hosts.  Deploying an extension to a network protocol can be difficult in practice since some nodes already support the extensions while others still use the old version and do not understand the extension. To deal with this issue, the IPv6 designers opted for a Type-Length-Value encoding of these IPv6 options. The `Hop-by-Hop Options` header is encoded as shown below.

.. figure:: /pkt/ipv6-hbh.png
   :scale: 120

   The IPv6 `Hop-by-Hop Options` header

In this optional header, the `Next Header` field is used to support the chain of headers. It indicates the type of the next header in the chain. IPv6 headers have different lengths. The `Hdr Ext Len` field indicates the total length of the option header in bytes. The `Opt. Type` field indicates the type of option. These types are encoded such that their high order bits specify how the header needs to be handled by nodes that do not recognize it. The following values are defined for the two high order bits :

 - ``00`` : if a node does not recognize this header, it  can be safely skipped and the processing continues with the subsequent header
 - ``01`` : if a node does not recognize this header, the packet must be discarded
 - ``10`` (resp. ``11``) : if a node does not recognize this header, it must return a control packet (ICMP, see later) back to the source (resp. except if the destination was a multicast address)

This encoding allows the designers of protocol extensions to specify whether the option must be supported by all nodes on a path or not. Still, deploying such an extension can be difficult in practice.

.. index:: jumbogram

Two `hop-by-hop` options have been defined. :rfc:`2675` specifies the jumbogram that enables IPv6 to support packets containing a payload larger than 65535 bytes. These jumbo packets have their `payload length` set to `0` and the jumbogram option contains the packet length as a 32 bits field. Such packets can only be sent from a source to a destination if all the routers on the path support this option. However, as of this writing it does not seem that the jumbogram option has been implemented. The router alert option defined in :rfc:`2711` is the second example of a `hop-by-hop` option. The packets that contain this option should be processed in a special way by intermediate routers. This option is used for IP packets that carry Resource Reservation Protocol (RSVP) messages, but this is outside the scope of this book.


The `Destinations Option` header uses the same format as the `Hop-by-Hop Options` header. It has some usages, e.g. to support mobile nodes :rfc:`6275`, but these are outside the scope of this document.

.. index:: IPv6 fragmentation

The `Fragment Options` header is more important. An important problem in the network layer is the ability to handle heterogeneous datalink layers. Most datalink layer technologies can only transmit and receive frames that are shorter than a given maximum frame size. Unfortunately, all datalink layer technologies use different maximum frames sizes.

.. index:: Maximum Transmission Unit, MTU

Each datalink layer has its own characteristics and as indicated earlier, each datalink layer is characterized by a maximum frame size. From IP's point of view, a datalink layer interface is characterized by its `Maximum Transmission Unit (MTU)`. The MTU of an interface is the largest packet (including header) that it can send. The table below provides some common MTU sizes.

==============      ==================
Datalink layer      MTU
--------------      ------------------
Ethernet	           1500 bytes
WiFi		           2272 bytes
ATM (AAL5)	        9180 bytes
802.15.4	           102 or 81 bytes
Token Ring	        4464 bytes
FDDI  		        4352 bytes
==============      ==================

Although IPv6 can send 64 KBytes long packets, few datalink layer technologies that are used today are able to send a 64 KBytes packet inside a frame. Furthermore, as illustrated in the figure below, another problem is that a host may send a packet that would be too large for one of the datalink layers used by the intermediate routers.

.. figure:: /protocols/figures/ipv6-frag.png
   :align: center
   :scale: 70

   The need for fragmentation and reassembly

.. Index:: IPv4 fragmentation and reassembly

To solve these problems, IPv6 includes a packet fragmentation and reassembly mechanism. In IPv4, fragmentation was performed by both the hosts and the intermediate routers. However, experience with IPv4 has shown that fragmenting packets in routers was costly [KM1995]_.  For this reason, the developers of IPv6 have decided that routers would not fragment packets anymore. In IPv6, fragmentation is only performed by the source host. If a source has to send a packet which is larger than the MTU of the outgoing interface, the packet needs to be fragmented before being transmitted. In IPv6, each packet fragment is an IPv6 packet that includes the `Fragmentation` header. This header is included by the source in each packet fragment. The receiver uses them to reassemble the received fragments.

.. figure:: /pkt/ipv6-fragment.png
   :scale: 120

   IPv6 fragmentation header

If a router receives a packet that is too long to be forwarded, the packet is dropped and the router returns an ICMPv6 message to inform the sender of the problem. The sender can then either fragment the packet or perform Path MTU discovery. In IPv6, packet fragmentation is performed only by the source by using IPv6 options.

.. The basic operation of the IPv6 fragmentation is as follows. A large packet is fragmented into two or more fragments. The size of all fragments, except the last one, is equal to the Maximum Transmission Unit of the link used to forward the packet. Each IPv6 `Fragmentation header` contains a 32 bits `Identification` field. When a packet is fragmented, the `Identification` of the large packet is copied in all fragments to allow the destination to reassemble the received fragments together. In each fragment, the `Fragment Offset` indicates, in units of 8 bytes, the position of the payload of the fragment in the payload of the original packet. The `Length` field in each fragment indicates the length of the payload of the fragment as in a normal IPv6 packet. Finally, the `M` flag is set only in the last fragment of a large packet.

In IPv6, fragmentation is performed exclusively by the source host and relies on the fragmentation header. This 64 bits header is composed of six fields :

 - a `Next Header` field that indicates the type of the header that follows the fragmentation header
 - two `Reserved` fields set to `0`.
 - the `Fragment Offset` is a 13-bit unsigned integer that contains the offset, in 8 bytes units, of the data following this header, relative to the start of the original packet.
 - the `More` flag, which is set to `0` in the last fragment of a packet and to `1` in all other fragments.
 - the 32-bit `Identification` field indicates to which original packet a fragment belongs. When a host sends fragmented packets, it should ensure that it does not reuse the same `identification` field for packets sent to the same destination during a period of `MSL` seconds. This is easier with the 32 bits `identification` used in the IPv6 fragmentation header, than with the 16 bits `identification` field of the IPv4 header.

.. spelling::

   priori

Some IPv6 implementations send the fragments of a packet in increasing fragment offset order, starting from the first fragment. Others send the fragments in reverse order, starting from the last fragment. The latter solution can be advantageous for the host that needs to reassemble the fragments, as it can easily allocate the buffer required to reassemble all fragments of the packet upon reception of the last fragment. When a host receives the first fragment of an IPv6 packet, it cannot know a priori the length of the entire IPv6 packet.

The figure below provides an example of a fragmented IPv6 packet containing a UDP segment. The `Next Header` type reserved for the IPv6 fragmentation option is 44.

.. figure:: /protocols/figures/ipv6-frag-example.png
   :align: center
   :scale: 70

   IPv6 fragmentation example

The following pseudo-code details the IPv6 fragmentation, assuming that the packet does not contain options.

.. code-block:: python

    # mtu : maximum size of the packet (including header) of outgoing link
    # In Scapy-like notation (see https://github.com/secdev/scapy)
    if p.len < mtu:
        send(p)
    else:
        # packet is too large
        # 40 refers to the size of the IPv6 header
        maxpayload = 8 * int((mtu - 40) / 8)  # must be n times 8 bytes
        # packet must be fragmented
        payload = p[IPv6].payload
        pos = 0
        id = globalCounter
        globalCounter += 1
        while len(payload) > 0:
            if len(payload) > maxpayload:
                toSend = IPv6(dst=p.dst, src=p.src, plen=mtu,
                              hlim=p.hlim, nh=44)/IPv6ExtHdrFrament(
                                  id=id, offset=p.offset + (pos/8), m=True,
                                  nh=p.nh)/payload[0:maxpayload]
                pos = pos + maxpayload
                payload = payload[maxpayload+1:]
            else:
                # The last fragment
                toSend = IPv6(dst=p.dst, src=p.src, plen=len(payload),
                              hlim=p.hlim, nh=44)/IPv6ExtHdrFrament(
                                  id=id, offset=p.offset + (pos/8), m=False,
                                  nh=p.nh)/payload
                payload = []

            forward(toSend)

In the above pseudocode, we maintain a single 32 bits counter that is incremented for each packet that needs to be fragmented. Other implementations to compute the packet identification are possible. :rfc:`2460` only requires that two fragmented packets that are sent within the MSL between the same pair of hosts have different identifications.

The fragments of an IPv6 packet may arrive at the destination in any order, as each fragment is forwarded independently in the network and may follow different paths. Furthermore, some fragments may be lost and never reach the destination.

The reassembly algorithm used by the destination host is roughly as follows. First, the destination can verify whether a received IPv6 packet is a fragment or not by checking whether it contains a fragment header. If so, all fragments with the some identification must be reassembled together. The reassembly algorithm relies on the `Identification` field of the received fragments to associate a fragment with the corresponding packet being reassembled. Furthermore, the `Fragment Offset` field indicates the position of the fragment payload in the original non-fragmented packet. Finally, the packet with the `M` flag reset allows the destination to determine the total length of the original non-fragmented packet.

Note that the reassembly algorithm must deal with the unreliability of the IP network. This implies that a fragment may be duplicated or a fragment may never reach the destination. The destination can easily detect fragment duplication thanks to the `Fragment Offset`. To deal with fragment losses, the reassembly algorithm must bind the time during which the fragments of a packet are stored in its buffer while the packet is being reassembled. This can be implemented by starting a timer when the first fragment of a packet is received. If the packet has not been reassembled upon expiration of the timer, all fragments are discarded and the packet is considered to be lost.


.. note:: Header compression on low bandwidth links

 Given the size of the IPv6 header, it can cause huge overhead on low bandwidth links, especially when small packets are exchanged such as for Voice over IP applications. In such environments, several techniques can be used to reduce the overhead. A first solution is to use data compression in the datalink layer to compress all the information exchanged [Thomborson1992]_. These techniques are similar to the data compression algorithms used in tools such as :manpage:`compress(1)` or :manpage:`gzip(1)` :rfc:`1951`. They compress streams of bits without taking advantage of the fact that these streams contain IP packets with a known structure. A second solution is to compress the IP and TCP header. These header compression techniques, such as the one defined in :rfc:`5795` take advantage of the redundancy found in successive packets from the same flow to significantly reduce the size of the protocol headers. Another solution is to define a compressed encoding of the IPv6 header that matches the capabilities of the underlying datalink layer :rfc:`4944`.

The last type of `IPv6 header extension` is the `Routing` header. The ``type 0`` routing header defined in :rfc:`2460` is an example of an IPv6 option that must be processed by some routers. This option is encoded as shown below.

.. figure:: /pkt/ipv6-routing-0.png
   :align: center
   :scale: 100

   The Type 0 routing header (:rfc:`2460`)


The type 0 routing option was intended to allow a host to indicate a loose source route that should be followed by a packet by specifying the addresses of some of the routers that must forward this packet. Unfortunately, further work with this routing header, including an entertaining demonstration with scapy_ [BE2007]_ , revealed severe security problems with this routing header. For this reason, loose source routing with the type 0 routing header has been removed from the IPv6 specification :rfc:`5095`.


.. do Segment Routing

.. _ICMPv6:

ICMP version 6
==============

It is sometimes necessary for intermediate routers or the destination host to inform the sender of the packet of a problem that occurred while processing a packet. In the TCP/IP protocol suite, this reporting is done by the Internet Control Message Protocol (ICMP). ICMPv6 is defined in :rfc:`4443`. It is used both to report problems that occurred while processing an IPv6 packet, but also to distribute addresses.

ICMPv6 messages are carried inside IPv6 packets (the `Next Header` field for ICMPv6 is ``58``). Each ICMP message contains a 32 bits header with an 8 bits `type` field, a `code` field and a 16 bits checksum computed over the entire ICMPv6 message. The message body contains a copy of the IPv6 packet in error.

.. figure:: /pkt/icmpv6.png
   :align: center
   :scale: 120

   ICMP version 6 packet format


ICMPv6 specifies two classes of messages : error messages that indicate a problem in handling a packet and informational messages. Four types of error messages are defined in :rfc:`4443` :

 - ``1`` : `Destination Unreachable`. Such an ICMPv6 message is sent when the destination address of a packet is unreachable. The `code` field of the ICMP header contains additional information about the type of unreachability. The following codes are specified in :rfc:`4443`
     - ``0`` : No route to destination. This indicates that the router that sent the ICMPv6 message did not have a route towards the packet's destination
     - ``1`` : Communication with destination administratively prohibited. This indicates that a firewall has refused to forward the packet towards its final destination.
     - ``2`` : Beyond scope of source address. This message can be sent if the source is using link-local addresses to reach a global unicast address outside its subnet.
     - ``3`` : Address unreachable. This message indicates that the packet reached the subnet of the destination, but the host that owns this destination address cannot be reached.
     - ``4`` : Port unreachable. This message indicates that the IPv6 packet was received by the destination, but there was no application listening to the specified port.
 - ``2`` : Packet Too Big. The router that was to send the ICMPv6 message received an IPv6 packet that is larger than the MTU of the outgoing link. The ICMPv6 message contains the MTU of this link in bytes. This allows the sending host to implement Path MTU discovery :rfc:`1981`
 - ``3`` : Time Exceeded. This error message can be sent either by a router or by a host. A router would set `code` to `0` to report the reception of a packet whose `Hop Limit` reached `0`. A host would set `code` to `1` to report that it was unable to reassemble received IPv6 fragments.
 - ``4`` : Parameter Problem. This ICMPv6 message is used to report either the reception of an IPv6 packet with an erroneous header field (code `0`) or an unknown `Next Header` or IP option (codes `1` and `2`). In this case, the message body contains the erroneous IPv6 packet and the first 32 bits of the message body contain a pointer to the error.


The `Destination Unreachable` ICMP error message is returned when a packet cannot be forwarded to its final destination. The first four ICMPv6 error messages (type ``1``, codes ``0-3``)  are generated by routers while hosts may return code ``4`` when there is no application bound to the corresponding port number.

The `Packet Too Big` ICMP messages enable the source host to discover the MTU size that it can safely use to reach a given destination. To understand its operation, consider the (academic) scenario shown in the figure below. In this figure, the labels on each link represent the maximum packet size supported by this link.



    .. tikz::
       :libs: positioning, matrix, shapes

       \tikzstyle{arrow} = [thick,->,>=stealth]
       \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \node[host] (A) {A};
       \node[router, right=of A] (R1) {R1};
       \node[router, right=of R1] (R2) {R2};
       \node[router, below=of R2] (R3) {R3};
       \node[host, left=of R3] (B) {B};
       \draw[black] (A) -- (R1) node [midway, below] { {\tiny 1500}};
       \draw[black] (R1) -- (R2) node [midway, below] { {\tiny 1400}};
       \draw[black] (R3) -- (B) node [midway, below] {  {\tiny 1500}};
       \draw[black] (R2) -- (R3) node [midway, right] {  {\tiny 1200}};



If ``A`` sends a 1500 bytes packet, ``R1`` will return an ICMPv6 error message indicating a maximum packet length of 1400 bytes. ``A`` would then fragment the packet before retransmitting it. The small fragment would go through, but the large fragment will be refused by ``R2`` that would return an ICMPv6 error message. ``A`` can fragment again the packet and send it to the final destination as two fragments.

In practice, an IPv6 implementation does not store the transmitted packets to be able to retransmit them if needed. However, since TCP (and SCTP) buffer the segments that they transmit, a similar approach can be used in transport protocols to detect the largest MTU on a path towards a given destination. This technique is called PathMTU Discovery :rfc:`1981`.

.. index:: Path MTU discovery

When a TCP segment is transported in an IP packet that is fragmented in the network, the loss of a single fragment forces TCP to retransmit the entire segment (and thus all the fragments). If TCP was able to send only packets that do not require fragmentation in the network, it could retransmit only the information that was lost in the network. In addition, IP reassembly causes several challenges at high speed as discussed in :rfc:`4963`. Using IP fragmentation to allow UDP applications to exchange large messages raises several security issues [KPS2003]_.

ICMPv6 is used by TCP implementations to discover the largest MTU size that is allowed to reach a destination host without causing network fragmentation. A TCP implementation parses the `Packets Too Big` ICMP messages that it receives. These ICMP messages contain the MTU of the router's outgoing link in their `Data` field. Upon reception of such an ICMP message, the source TCP implementation adjusts its Maximum Segment Size (MSS) so that the packets containing the segments that it sends can be forwarded by this router without requiring fragmentation.


.. index:: ping6

Two types of informational ICMPv6 messages are defined in :rfc:`4443` : `echo request` and `echo reply`, which are used to test the reachability of a destination by using :manpage:`ping6(8)`. Each host is supposed [#fpingproblems]_ to reply with an ICMP `Echo reply` message when it receives an  ICMP `Echo request` message. A sample usage of :manpage:`ping6(8)` is shown below.

.. code-block:: console

   #ping6 www.ietf.org
   PING6(56=40+8+8 bytes) 2001:6a8:3080:2:3403:bbf4:edae:afc3 --> 2001:1890:123a::1:1e
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=0 hlim=49 time=156.905 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=1 hlim=49 time=155.618 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=2 hlim=49 time=155.808 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=3 hlim=49 time=155.325 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=4 hlim=49 time=155.493 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=5 hlim=49 time=155.801 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=6 hlim=49 time=155.660 ms
   16 bytes from 2001:1890:123a::1:1e, icmp_seq=7 hlim=49 time=155.869 ms
   ^C
   --- www.ietf.org ping6 statistics ---
   8 packets transmitted, 8 packets received, 0.0% packet loss
   round-trip min/avg/max/std-dev = 155.325/155.810/156.905/0.447 ms


.. index:: traceroute6

Another very useful debugging tool is :manpage:`traceroute6(8)`. The traceroute man page describes this tool as `"print the route packets take to network host"`. traceroute uses the `Time exceeded` ICMP messages to discover the intermediate routers on the path towards a destination. The principle behind traceroute is very simple. When a router receives an IP packet whose `Hop Limit` is set to ``1`` it is forced to return to the sending host a `Time exceeded` ICMP message containing the header and the first bytes of the discarded packet. To discover all routers on a network path, a simple solution is to first send a packet whose `Hop Limit` is set to `1`, then a packet whose `Hop Limit` is set to `2`, etc. A sample traceroute6 output is shown below.


.. code-block:: console

 #traceroute6 www.ietf.org
 traceroute6 to www.ietf.org (2001:1890:1112:1::20) from 2001:6a8:3080:2:217:f2ff:fed6:65c0, 30 hops max, 12 byte packets
  1  2001:6a8:3080:2::1  13.821 ms  0.301 ms  0.324 ms
  2  2001:6a8:3000:8000::1  0.651 ms  0.51 ms  0.495 ms
  3  10ge.cr2.bruvil.belnet.net  3.402 ms  3.34 ms  3.33 ms
  4  10ge.cr2.brueve.belnet.net  3.668 ms 10ge.cr2.brueve.belnet.net  3.988 ms 10ge.cr2.brueve.belnet.net  3.699 ms
  5  belnet.rt1.ams.nl.geant2.net  10.598 ms  7.214 ms  10.082 ms
  6  so-7-0-0.rt2.cop.dk.geant2.net  20.19 ms  20.002 ms  20.064 ms
  7  kbn-ipv6-b1.ipv6.telia.net  21.078 ms  20.868 ms  20.864 ms
  8  s-ipv6-b1-link.ipv6.telia.net  31.312 ms  31.113 ms  31.411 ms
  9  s-ipv6-b1-link.ipv6.telia.net  61.986 ms  61.988 ms  61.994 ms
  10  2001:1890:61:8909::1  121.716 ms  121.779 ms  121.177 ms
  11  2001:1890:61:9117::2  203.709 ms  203.305 ms  203.07 ms
  12  mail.ietf.org  204.172 ms  203.755 ms  203.748 ms



.. note:: Rate limitation of ICMP messages

 High-end hardware based routers use special purpose chips on their interfaces to forward IPv6 packets at line rate. These chips are optimized to process `correct` IP packets. They are not able to create ICMP messages at line rate. When such a chip receives an IP packet that triggers an ICMP message, it interrupts the main CPU of the router and the software running on this CPU processes the packet. This CPU is much slower than the hardware acceleration found on the interfaces [Gill2004]_. It would be overloaded if it had to process IP packets at line rate and generate one ICMP message for each received packet. To protect this CPU, high-end routers limit the rate at which the hardware can interrupt the main CPU and thus the rate at which ICMP messages can be generated. This implies that not all erroneous IP packets cause the transmission of an ICMP message. The risk of overloading the main CPU of the router is also the reason why using hop-by-hop IPv6 options, including the router alert option is discouraged [#falert]_.


The IPv6 subnet
===============

Until now, we have focused our discussion on the utilization of IPv6 on point-to-point links. Although there are point-to-point links in the Internet, mainly between routers and sometimes hosts, most of the hosts are attached to datalink layer networks such as Ethernet LANs or WiFi networks. These datalink layer networks play an important role in today's Internet and have heavily influenced the design of the operation of IPv6. To understand IPv6 and ICMPv6 completely, we first need to correctly understand the key principles behind these datalink layer technologies.

As explained earlier, devices attached to a Local Area Network can directly exchange frames among themselves. For this, each datalink layer interface on a device (host, router, ...) attached to such a network is identified by a MAC address. Each datalink layer interface includes a unique hardwired MAC address. MAC addresses are allocated to manufacturers in blocks and interface is numbered with a unique address. Thanks to the global unicity of the MAC addresses, the datalink layer service can assume that two hosts attached to a LAN have different addresses. Most LANs provide an unreliable connectionless service and a datalink layer frame has a header containing :

 - the source MAC address
 - the destination MAC address
 - some multiplexing information to indicate the network layer protocol that is responsible for the payload of the frame

LANs also provide a broadcast and a multicast service. The broadcast service enables a device to send a single frame to all the devices attached to the same LAN. This is done by reserving a special broadcast  MAC address (typically all bits of the address are set to one). To broadcast a frame, a device simply needs to send a frame whose destination is the broadcast address. All devices attached to the datalink network will receive the frame.

The broadcast service allows easily reaching all devices attached to a datalink layer network. It has been widely used to support IP version 4. A drawback of using the broadcast service to support a network layer protocol is that a broadcast frame that contains a network layer packet is always delivered to all devices attached to the datalink network, even if some of these devices do not support the network layer protocol. The multicast service is a useful alternative to the broadcast service. To understand its operation, it is important to understand how a datalink layer interface operates. In shared media LANs, all devices are attached to the same physical medium and all frames are delivered to all devices. When such a frame is received by a datalink layer interface, it compares the destination address with the MAC address of the device. If the two addresses match, or the destination address is the broadcast address, the frame is destined to the device and its payload is delivered to the network layer protocol. The multicast service exploits this principle. A multicast address is a logical address. To receive frames destined to a multicast address in a shared media LAN, a device captures all frames having this multicast address as their destination. All IPv6 nodes are capable of capturing datalink layer frames destined to different multicast addresses.


Interactions between IPv6 and the datalink layer
------------------------------------------------

.. index:: Neighbour Discovery Protocol

IPv6 hosts and routers frequently interact with the datalink layer service. To understand the main interactions, it is useful to analyze all the packets that are exchanged when a simple network containing a few hosts and routers is built. Let us first start with a LAN containing two hosts [#fMAC]_.

  .. tikz::
     :libs: positioning, matrix, arrows.meta, shapes

     \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
     \tikzset{lan/.style = {ellipse, draw, text centered} }
     \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
     \node[host, align=center] (A) {A \\ \tiny{MAC : 00:23:45:67:89:ab} };
     \node[lan, below right=of A] (lan) {LAN};
     \node[host, above right=of lan, align=center] (B) {B \\ \tiny{MAC : 00:34:56:78:9a:bc} };
     \draw[black] (A) -- (lan);
     \draw[black] (B) -- (lan);



.. index:: link-local IPv6 address

Hosts ``A`` and ``B`` are attached to the same datalink layer network. They can thus exchange frames by using the MAC addresses shown in the figure above. To be able to use IPv6 to exchange packets, they need to have an IPv6 address. One possibility would be to manually configure an IPv6 address on each host. However, IPv6 provides a better solution thanks to the `link-local` IPv6 addresses. A `link-local` IPv6 address is an address that is composed by concatenating the ``fe80:://64`` prefix with the MAC address of the device. In the example above, host A would use IPv6 `link-local` address ``fe80::0223:45FF:FE67:89ab`` and host B ``fe80::0234:56FF:FE78:9abc``. With these two IPv6 addresses, the hosts can exchange IPv6 packets.

.. note:: Converting MAC addresses in host identifiers

 Appendix A of :rfc:`4291` provides the algorithm used to convert a 48 bits MAC address into a 64 bits host identifier. This algorithm builds upon the structure of the MAC addresses. A MAC address is represented as shown in the figure below.

  .. figure:: /pkt/macaddr.png
     :align: center

     A MAC address

 MAC addresses are allocated in blocks of :math:`2^{20}`. When a company registers for a block of MAC addresses, it receives an identifier. company identifier is then used to populated the `c` bits of the MAC addresses. The company can allocate all addresses in starting with this prefix and manages the `m` bits as it wishes.

  .. figure:: /pkt/macaddr-eui64.png
     :align: center

     A MAC address converted into a 64 bits host identifier

 Inside a MAC address, the two bits indicated as `0` and `g` in the figure above play a special role. The first bit indicates whether the address is universal or local. The `g` bit indicates whether this is a multicast address or a unicast address. The MAC address can be converted into a 64 bits host identifier by flipping the value of the `0` bit and inserting ``FFFE``, i.e. ``1111111111111110`` in binary, in the middle of the address as shown in the figure below. The `c`, `m` and `g` bits of the MAC address are not modified.


The next step is to connect the LAN to the Internet. For this, a router is attached to the LAN.


   .. tikz:: A simple IPv6 network with one router
      :libs: positioning, matrix, arrows.meta, shapes

      [align=center,node distance=2.5cm]
      \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
      \tikzset{lan/.style = {ellipse, draw, text centered} }
      \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
      \node[host, align=center] (A) {A \\ \tiny{MAC : 00:23:45:67:89:ab} };
      \node[host, right=of A, align=center] (B) {B \\ \tiny{MAC : 00:34:56:78:9a:bc} };
      \node[router, right=of B, align=center] (router) {router \\ \tiny{MAC : 00:45:67:89:ab:cd} };
      \node[lan, below right=of A] (lan) {LAN};
      \draw[black] (A) -- (lan);
      \draw[black] (router) -- (lan);
      \draw[black] (B) -- (lan);


Assume that the LAN containing the two hosts and the router is assigned prefix ``2001:db8:1234:5678/64``. A first solution to configure the IPv6 addresses in this network is to assign them manually. A possible assignment is :

 - ``2001:db8:1234:5678::1`` is assigned to ``router``
 - ``2001:db8:1234:5678::AA`` is assigned to ``hostA``
 - ``2001:db8:1234:5678::BB`` is assigned to ``hostB``

.. index:: Address resolution problem, Neighbor Discovery Protocol, NDP

To be able to exchange IPv6 packets with ``hostB``, ``hostA`` needs to know the MAC address of the interface of ``hostB`` on the LAN. This is the `address resolution` problem. In IPv6, this problem is solved by using the Neighbor Discovery Protocol (NDP). NDP is specified in :rfc:`4861`. This protocol is part of ICMPv6 and uses the multicast datalink layer service.

.. spelling::

   querier

.. index:: Neighbor Solicitation message

NDP allows a host to discover the MAC address used by any other host attached to the same LAN. NDP operates in two steps. First, the querier sends a multicast ICMPv6 Neighbor Solicitation message that contains as parameter the queried IPv6 address. This multicast ICMPv6 NS is placed inside a multicast frame [#fndpmulti]_. The queried node receives the frame, parses it and replies with a unicast ICMPv6 Neighbor Advertisement that provides its own IPv6 and MAC addresses. Upon reception of the Neighbor Advertisement message, the querier stores the mapping between the IPv6 and the MAC address inside its NDP table. This table is a data structure that maintains a cache of the recently received Neighbor Advertisement. Thanks to this cache, a host only needs to send a Neighbor Solicitation message for the first packet that it sends to a given host. After this initial packet, the NDP table can provide the mapping between the destination IPv6 address and the corresponding MAC address.

 .. msc::
      router [label="router", linecolour=black],
      hostA [label="hostA", linecolour=black],
      hostB [label="hostB", linecolour=black];

      hostA->* [ label = "NS : Who has 2001:db8:1234:5678::BB" ];
      hostB->hostA [ label = "NA : 00:34:56:78:9a:bc"];
      |||;

The NS message can also be used to verify the reachability of a host in the local subnet. For this usage, NS messages can be sent in unicast since other nodes on the subnet do not need to process the message.

When an entry in the NDP table times out on a host, it may either be deleted or the host may try to validate it by sending the NS message again.

.. In practice, there are some technical subtleties with these ICMPv6 messages. First, the NS and NA  messages always sent with a `HopLimit` of ``255``. No device should ever accept such an ICMPv6 message that includes a different `HopLimit`. This is to prevent attacks where remote attackers could try to send fake ICMPv6 messages from outside the LAN. Since the `HopLimit` of all IPv6 packets is always decremented by one by each intermediate router, it is impossible for a remote attacker to send an ICMPv6 message that would have a `HopLimit` of ``255`` when it reaches the LAN. Second, the NA message is sent in unicast. of the NS message used to query an address is always an IPv6 multicast address. The IPv6 addressing architecture defines several well-know IPv6 multicast addresses :


.. index:: Duplicate Address Detection

This is not the only usage of the Neighbor Solicitation and Neighbor Advertisement messages. They are also used to detect the utilization of duplicate addresses. In the network above, consider what happens when a new host is connected to the LAN. If this host is configured by mistake with the same address as ``hostA`` (i.e. ``2001:db8:1234:5678::AA``), problems could occur. Indeed, if two hosts have the same IPv6 address on the LAN, but different MAC addresses, it will be difficult to correctly reach them. IPv6 anticipated this problem and includes a `Duplicate Address Detection` Algorithm (DAD). When an IPv6 address [#flinklocal]_ is configured on a host, by any means, the host must verify the uniqueness of this address on the LAN. For this, it multicasts an ICMPv6 Neighbor Solicitation that queries the network for its newly configured address. The IPv6 source address of this NS is set to ``::`` (i.e. the reserved unassigned address) if the host does not already have an IPv6 address on this subnet). If the NS does not receive any answer, the new address is considered to be unique and can safely be used. Otherwise, the new address is refused and an error message should be returned to the system administrator or a new IPv6 address should be generated. The `Duplicate Address Detection` Algorithm can prevent various operational problems that are often difficult to debug.



.. There are several differences between IPv6 and IPv4 when considering their interactions with the datalink layer. In IPv6, the interactions between the network and the datalink layer is performed using ICMPv6.

Few users manually configure the IPv6 addresses on their hosts. They prefer to rely on protocols that can automatically configure their IPv6 addresses. IPv6 supports two such protocols : DHCPv6 and the Stateless Address Autoconfiguration (SLAAC).

.. spelling::

   autoconfiguration
   Autoconfiguration


.. index:: DHCPv6, SLAC, Stateless Address Autoconfiguration


The Stateless Address Autoconfiguration (SLAAC) mechanism defined in :rfc:`4862` enables hosts to automatically configure their addresses without maintaining any state. When a host boots, it derives its identifier from its datalink layer address [#fprivacy]_ as explained earlier and concatenates this 64 bits identifier to the `FE80::/64` prefix to obtain its link-local IPv6 address. It then multicasts a Neighbor Solicitation with its link-local address as a target to verify whether another host is using the same link-local address on this subnet. If it receives a Neighbor Advertisement indicating that the link-local address is used by another host, it generates another 64 bits identifier and sends again a Neighbor Solicitation. If there is no answer, the host considers its link-local address to be valid. This address will be used as the source address for all NDP messages sent on the subnet.

To automatically configure its global IPv6 address, the host must know the globally routable IPv6 prefix that is used on the local subnet. IPv6 routers regularly multicast ICMPv6 Router Advertisement messages that indicate the IPv6 prefix assigned to the subnet. The Router Advertisement message contains several interesting fields.

.. figure:: /pkt/router-adv.png
   :align: center
   :scale: 120

   Format of the ICMPv6 Router Advertisement message

This message is sent from the link-local address of the router on the subnet. Its destination is the IPv6 multicast address that targets all IPv6 enabled hosts (i.e. ``ff02::1``). The `Cur Hop Limit` field, if different from zero, allows specifying the default `Hop Limit` that hosts should use when sending IPv6 packets from this subnet. ``64`` is a frequently used value. The `M` and `O` bits are used to indicate that some information can be obtained from DHCPv6. The `Router Lifetime` parameter provides the expected lifetime (in seconds) of the sending router acting as a default router. This lifetime enables planning the replacement of a router by another one in the same subnet. The `Reachable Time` and the `Retrans Timer` parameter are used to configure the utilization of the NDP protocol on the hosts attached to the subnet.

Several options can be included in the Router Advertisement message. The simplest one is the MTU option that indicates the MTU to be used within the subnet. Thanks to this option, it is possible to ensure that all devices attached to the same subnet use the same MTU. Otherwise, operational problems could occur. The `Prefix` option is more important. It provides information about the prefix(es) that is (are) advertised by the router on the subnet.

.. figure:: /pkt/router-prefix.png
   :align: center
   :scale: 120

   The Prefix information option

.. index:: IPv6 Renumbering


The key information placed in this option are the prefix and its length. This allows the hosts attached to the subnet to automatically configure their own IPv6 address. The `Valid` and `Preferred` `Lifetimes` provide information about the expected lifetime of the prefixes. Associating some time validity to prefixes is a good practice from an operational viewpoint. There are some situations where the prefix assigned to a subnet needs to change without impacting the hosts attached to the subnet. This is often called the IPv6 renumbering problem in the literature :rfc:`7010`. A very simple scenario is the following. An SME subscribes to one ISP. Its router is attached to another router of this ISP and advertises a prefix assigned by the ISP. The SME is composed of a single subnet and all its hosts rely on stateless address configuration. After a few years, the SME decides to change of network provider. It connects its router to the second ISP and receives a different prefix from this ISP. At this point, two prefixes are advertised on the SME's subnet. The old prefix can be advertised with a short lifetime to ensure that hosts will stop using it while the new one is advertised with a longer lifetime. After sometime, the router stops advertising the old prefix and the hosts stop using it. The old prefix can now be returned back to the first ISP. In larger networks, renumbering an IPv6 remains a difficult operational problem [LeB2009]_.

Upon reception of this message, the host can derive its global IPv6 address by concatenating its 64 bits identifier with the received prefix. It concludes the SLAAC by sending a Neighbor Solicitation message targeted at its global IPv6 address to ensure that no other host is using the same IPv6 address.

.. note:: Router Advertisements and Hop Limits

  ICMPv6 Router Advertisements messages are regularly sent by routers. They are destined to all devices attached to the local subnet and no router should ever forward them to another subnet. Still, these messages are sent inside IPv6 packets whose `Hop Limit` is always set to ``255``. Given that the packet should not be forwarded outside of the local subnet, the reader could expect instead a `Hop Limit` set to ``1``. Using a `Hop Limit` set to ``255`` provides one important benefit from a security viewpoint and this hack has been adapted in several Internet protocols. When a host receives a `Router Advertisement` message, it expects that this message has been generated by a router attached to the same subnet. Using a `Hop Limit` of ``255`` provides a simple check for this. If the message was generated by an attacker outside the subnet, it would reach the subnet with a decremented `Hop Limit`. Checking that the `Hop Limit` is set to ``255`` is a simple [#fsend]_ verification that the packet was generated on this particular subnet. :rfc:`5082` provides other examples of protocols that use this hack and discuss its limitations.


Routers regularly send Router Advertisement messages. These messages are triggered by a timer that is often set at approximately 30 seconds. Usually, hosts wait for the arrival of a Router Advertisement message to configure their address. This implies that hosts could sometimes need to wait 30 seconds before being able to configure their address. If this delay is too long, a host can also send a `Router Solicitation` message. This message is sent towards the multicast address that corresponds to all IPv6 routers (i.e. ``FF01::2``) and the default router will reply.

The last point that needs to be explained about ICMPv6 is the `Redirect` message. This message is used when there is more than one router on a subnet as shown in the figure below.

   .. tikz:: A simple IPv6 network with two routers
      :libs: positioning, matrix, shapes


      \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
      \tikzset{lan/.style = {ellipse, draw, text centered} }
      \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
      \node[host] (A) {\begin{tabular}{c} A \\ \tiny{MAC: 00:23:45:67:89:ab} \end{tabular}};
      \node[host, right =of A] (B) {\begin{tabular}{c} B \\ \tiny{MAC: 00:34:56:78:9a:bc} \end{tabular}};
      \node[router, right =of B] (router1) {\begin{tabular}{c} router1 \\ \tiny{MAC: 00:45:67:89:ab:cd} \end{tabular}};
      \node[router, right =of router1] (router2) {\begin{tabular}{c} router2 \\ \tiny{MAC: 00:12:34:56:78:78} \end{tabular}};
      \node[lan, below right=of A] (lan) {LAN};

      \draw[black] (A) -- (lan);
      \draw[black] (router1) -- (lan);
      \draw[black] (router2) -- (lan);
      \draw[black] (B) -- (lan);


In this network, ``router1`` is the default router for all hosts. The second router, ``router2`` provides connectivity to a specific IPv6 subnet, e.g. ``2001:db8:abcd::/48``. These two routers attached to the same subnet can be used in different ways. First, it is possible to manually configure the routing tables on all hosts to add a route towards ``2001:db8:abcd::/48`` via ``router2``. Unfortunately, forcing such manual configuration boils down all the benefits of using address auto-configuration in IPv6. The second approach is to automatically configure a default route via ``router1`` on all hosts. With such route, when a host needs to send a packet to any address within ``2001:db8:abcd::/48``, it will send it to ``router1``. ``router1`` would consult its routing table and find that the packet needs to be sent again on the subnet to reach ``router2``. This is a waste of time. A better approach would be to enable the hosts to automatically learn the new route. This is possible thanks to the ICMPv6 `Redirect` message. When ``router1`` receives a packet that needs to be forwarded back on the same interface, it replies with a `Redirect` message that indicates that the packet should have been sent via ``router2``. Upon reception of a `Redirect`  message, the host updates it forwarding table to include a new transient entry for the destination reported in the message. A timeout is usually associated with  this transient entry to automatically delete it after some time.


.. index:: DHCPv6



An alternative is the Dynamic Host Configuration Protocol (DHCP) defined in :rfc:`2131` and :rfc:`3315`. DHCP allows a host to automatically retrieve its assigned IPv6 address, but relies on  server. A DHCP server is associated to each subnet [#fdhcpserver]_. Each DHCP server manages a pool of IPv6 addresses assigned to the subnet. When a host is first attached to the subnet, it sends a DHCP request message in a UDP segment (the DHCP server listens on port 67). As the host knows neither its IPv6 address nor the IPv6 address of the DHCP server, this UDP segment is sent inside a multicast packet target at the DHCP servers. The DHCP request may contain various options such as the name of the host, its datalink layer address, etc. The server captures the DHCP request and selects an unassigned address in its address pool. It then sends the assigned IPv6 address in a DHCP reply message which contains the datalink layer address of the host and additional information such as the subnet mask, the address of the default router or the address of the DNS resolver. The DHCP reply also specifies the lifetime of the address allocation. This forces the host to renew its address allocation once it expires. Thanks to the limited lease time, IP addresses are automatically returned to the pool of addresses when  hosts are powered off.

Both SLAAC and DHCPv6 can be extended to provide additional information beyond the IPv6 prefix/address. For example, :rfc:`6106` defines options for the ICMPv6 ND message that can carry the IPv6 address of the recursive DNS resolver and a list of default domain search suffixes. It is also possible to combine SLAAC with DHCPv6. :rfc:`3736` defines a stateless variant of DHCPv6 that can be used to distribute DNS information while SLAAC is used to distribute the prefixes.


.. rubric:: Footnotes



.. [#fmultiiana] The full list of allocated IPv6 multicast addresses is available at http://www.iana.org/assignments/ipv6-multicast-addresses

.. [#fianaprotocol] The IANA_ maintains the list of all allocated Next Header types at http://www.iana.org/assignments/protocol-numbers/

.. [#fipv4checksum] When IPv4 was designed, the situation was different. The IPv4 header includes a checksum that only covers the network header. This checksum is computed by the source and updated by all intermediate routers that decrement the TTL, which is the IPv4 equivalent of the `HopLimit` used by IPv6.

.. [#fpingproblems] Until a few years ago, all hosts replied to `Echo request` ICMP messages. However, due to the security problems that have affected TCP/IP implementations, many of these implementations can now be configured to disable answering `Echo request` ICMP messages.

.. [#falert] For a discussion of the issues with the router alert IP option, see http://tools.ietf.org/html/draft-rahman-rtg-router-alert-dangerous-00 or
 http://tools.ietf.org/html/draft-rahman-rtg-router-alert-considerations-03

.. [#fMAC] For simplicity, you assume that each datalink layer interface is assigned a 64 bits MAC address. As we will see later, today's datalink layer technologies mainly use 48 bits MAC addresses, but the smaller addresses can easily be converted into 64 bits addresses.

.. [#fndpmulti] :rfc:`4291` and :rfc:`4861` explain in more details how the IPv6 multicast address is determined from the target IPv6 unicast address. These details are outside the scope of this book, but may matter if you try to understand a packet trace.

.. [#flinklocal] The DAD algorithm is also used with `link-local` addresses.

.. [#fprivacy] Using a datalink layer address to derive a 64 bits identifier for each host raises privacy concerns as the host will always use the same identifier. Attackers could use this to track hosts on the Internet. An extension to the Stateless Address Configuration mechanism that does not raise privacy concerns is defined in :rfc:`4941`. These privacy extensions allow a host to generate its 64 bits identifier randomly every time it attaches to a subnet. It then becomes impossible for an attacker to use the 64-bits identifier to track a host.




.. [#fsend] Using a `Hop Limit` of ``255`` prevents one family of attacks against ICMPv6, but other attacks still remain possible. A detailed discussion of the security issues with IPv6 is outside the scope of this book. It is possible to secure NDP by using the `Cryptographically Generated IPv6 Addresses` (CGA) defined in :rfc:`3972`. The Secure Neighbor Discovery Protocol is defined in :rfc:`3971`. A detailed discussion of the security of IPv6 may be found in [HV2008]_.

.. [#fdhcpserver] In practice, there is usually one DHCP server per group of subnets and the routers capture on each subnet the DHCP messages and forward them to the DHCP server.



.. include:: /links.rst
