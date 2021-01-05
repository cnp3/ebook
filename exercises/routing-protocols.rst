.. Copyright |copy| 2019 by Olivier Bonaventure 
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_



Exploring routing protocols
===========================

Routing protocols play a key role in the Internet since they ensure that all the routers have valid routing tables. In this section, we use IPMininet_ to explore how intradomain and interdomain routing protocols work in practice. IPMininet_ adds an abstraction layer above the actual configuration of the FRRouting daemons that implement these routing protocols.


Exploring OSPF
--------------

We first use IPMininet_ to explore the operation of OSPFv3, the version of OSPF that supports IPv6. We create a simple network with three routers and two hosts as shown in the figure below.

     .. tikz:: A simple network
        :libs: shapes, positioning, matrix, arrows, shapes 

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
	\tikzset{as/.style={cloud, draw,cloud puffs=10,cloud puff arc=120, aspect=2, minimum height=1em, minimum width=1em} }

        \node[host] (a) {a};
        \node[router, right=of a] (r1) {r1};
        \node[router, right=of r1] (r2) {r2};
	\node[router, below right=of r1] (r3) {r3};
	\node[host, right=of r3] (b) {b};

	\path[draw, color=black]
	(a) edge (r1)
	(b) edge (r3)    
	(r1) edge node [sloped, midway, above, color=black] {1} (r2)
	(r1) edge node [sloped, midway, above, color=black] {5} (r3)
	(r2) edge node [sloped, midway, above, color=black] {3} (r3);

.. code-block:: python

   import shlex
   from ipmininet.iptopo import IPTopo
   from ipmininet.ipnet import IPNet
   from ipmininet.cli import IPCLI

   class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        # Add routers (OSPF daemon is added by default with the default config)

        r1 = self.addRouter("r1")
        r2 = self.addRouter("r2")
        r3 = self.addRouter("r3")
        a = self.addHost("a")
        b = self.addHost("b")

        lr1r2 = self.addLink(r1, r2, igp_cost=1)
        lr1r2[r1].addParams(ip=("2001:db8:1341:12::1/64"))
        lr1r2[r2].addParams(ip=("2001:db8:1341:12::2/64"))

        lr1r3 = self.addLink(r1, r3, igp_cost=5)
        lr1r3[r1].addParams(ip=("2001:db8:1341:13::1/64"))
        lr1r3[r3].addParams(ip=("2001:db8:1341:13::3/64"))

        lr2r3 = self.addLink(r2, r3, igp_cost=3)
        lr2r3[r2].addParams(ip=("2001:db8:1341:23::2/64"))
        lr2r3[r3].addParams(ip=("2001:db8:1341:23::3/64"))
        
        lr1a = self.addLink(r1, a, igp_passive=True)
        lr1a[r1].addParams(ip=("2001:db8:1341:1::1/64"))
        lr1a[a].addParams(ip=("2001:db8:1341:1::A/64"))

        lr3b = self.addLink(r3, b, igp_passive=True)
        lr3b[r3].addParams(ip=("2001:db8:1341:3::3/64"))
        lr3b[b].addParams(ip=("2001:db8:1341:3::B/64"))

        super(MyTopology, self).build(*args, **kwargs)


The code is very simple as by default IPMininet_ enables OSPF on routers. We introduce two specific parameters. First, the interface that connects a router to a host is flagged as a passive interface (``igp_passive=True``). This indicates to the router that there are no other routers attached to this interface and that it should not send or accept OSPF Hello messages on this interface. The second configuration parameter is that we set the IGP cost on each link.


We use this mininet_ topology to collect packet traces that show the packets that OSPF routers exchange. For this, we add the following ``post_build`` method that IPMininet_ starts after having constructed the network and before launching the daemons. It simply starts tcpdump_ on each router to collect the first 100 OSPF packets that they send/receive.

.. code-block:: python

    def post_build(self, net):
        for r in self.routers():
            command="/usr/sbin/tcpdump --immediate-mode -c 100 -w ./"+r+"-trace.pcap proto ospf"
            p = net[r].popen(shlex.split(command))
	    
        super(MyTopology, self).post_build(net)

Finally, we can start the IPMininet_ topology and launch the daemons. The entire script is available from :download:`/exercises/ipmininet_scripts/ospf6.py`.
	
.. code-block:: python

   net = IPNet(topo=MyTopology(), allocate_IPs=False)  # Disable IP auto-allocation
   try:
     net.start()
     IPCLI(net)
   finally:
     net.stop()
		

The script starts the routers and hosts.

.. code-block:: console

   mininet> nodes
   available nodes are: 
   a b r1 r2 r3
   mininet> links
   r1-eth2<->a-eth0 (OK OK) 
   r1-eth0<->r2-eth0 (OK OK) 
   r1-eth1<->r3-eth0 (OK OK) 
   r2-eth1<->r3-eth1 (OK OK) 
   r3-eth2<->b-eth0 (OK OK) 

We can easily verify that the paths used to forward packets are the expected ones according to the configured IGP weights.

.. code-block:: console

   mininet> a traceroute6 2001:db8:1341:3::B
   traceroute to 2001:db8:1341:3::B (2001:db8:1341:3::b) from 2001:db8:1341:1::a, 30 hops max, 24 byte packets
   1  2001:db8:1341:1::1 (2001:db8:1341:1::1)  0.203 ms  0.061 ms  0.045 ms
   2  2001:db8:1341:13::3 (2001:db8:1341:13::3)  0.064 ms  0.055 ms  0.049 ms
   3  2001:db8:1341:3::b (2001:db8:1341:3::b)  0.231 ms  0.057 ms  0.05 ms
   mininet> b traceroute6 2001:db8:1341:1::A
   traceroute to 2001:db8:1341:1::A (2001:db8:1341:1::a) from 2001:db8:1341:3::b, 30 hops max, 24 byte packets
   1  2001:db8:1341:3::3 (2001:db8:1341:3::3)  0.088 ms  0.19 ms  0.053 ms
   2  2001:db8:1341:13::1 (2001:db8:1341:13::1)  0.066 ms  0.059 ms  0.047 ms
   3  2001:db8:1341:1::a (2001:db8:1341:1::a)  0.054 ms  0.059 ms  0.047 ms

We can also connect to the OSPFv3 daemon running on the routers to observe its state. For this, we use the ``noecho r1 telnet localhost ospf6d`` command.

.. code-block:: console

   mininet> noecho r1 telnet localhost ospf6d
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.

   Hello, this is FRRouting (version 7.1).
   Copyright 1996-2005 Kunihiro Ishiguro, et al.


   User Access Verification

   Password:

The password to access this daemon is `zebra`. It supports various commands that are described in the `FRRouting documentation <http://docs.frrouting.org/en/latest/ospf6d.html#showing-ospf6-information>`_ We briefly illustrate some of them below.

.. code-block:: console

   r1> show ipv6 ospf6 
   OSPFv3 Routing Process (0) with Router-ID 0.0.0.2
   Running 14:26:45
   LSA minimum arrival 1000 msecs
   Initial SPF scheduling delay 0 millisec(s)
   Minimum hold time between consecutive SPFs 50 millsecond(s)
   Maximum hold time between consecutive SPFs 5000 millsecond(s)
   Hold time multiplier is currently 1
   SPF algorithm last executed 14:26:26 ago, reason R+, R-
   Last SPF duration 0 sec 239 usec
   SPF timer is inactive
   Number of AS scoped LSAs is 0
   Number of areas in this router is 1
   
   Area 0.0.0.0
	Number of Area scoped LSAs is 11
		Interface attached to this area: lo r1-eth0 r1-eth1 r1-eth2
   SPF last executed 51986.405587s ago

The ``show ipv6 ospf6`` command reports the general state of the OSPFv3 daemon.
 The ``show ipv6 ospf6 neighbor`` command reports the state of the connected neighbors.

 .. code-block:: console

    r1> show ipv6 ospf6 neighbor 
    Neighbor ID     Pri    DeadTime    State/IfState         Duration I/F[State]
    0.0.0.3          10    00:00:02     Full/DR              14:44:44 r1-eth0[BDR]
    0.0.0.4          10    00:00:02     Full/DR              14:44:48 r1-eth1[BDR]


In its output, we see that ``r1`` is attached to two different routers. Finally, the ``show ipv6 ospf6 database`` returns the full OSPFv3 database with all the link state information that was distributed by OSPFv3.

.. code-block:: console
		
   r1> show ipv6 ospf6 database 

        Area Scoped Link State Database (Area 0.0.0.0)

   Type LSId           AdvRouter       Age   SeqNum                        Payload
   Rtr  0.0.0.0        0.0.0.2        1037 80000020                0.0.0.3/0.0.0.2
   Rtr  0.0.0.0        0.0.0.2        1037 80000020                0.0.0.4/0.0.0.2
   Rtr  0.0.0.0        0.0.0.3        1033 80000020                0.0.0.3/0.0.0.2
   Rtr  0.0.0.0        0.0.0.3        1033 80000020                0.0.0.4/0.0.0.3
   Rtr  0.0.0.0        0.0.0.4        1033 80000020                0.0.0.4/0.0.0.2
   Rtr  0.0.0.0        0.0.0.4        1033 80000020                0.0.0.4/0.0.0.3
   Net  0.0.0.2        0.0.0.3        1038 8000001e                        0.0.0.3
   Net  0.0.0.2        0.0.0.3        1038 8000001e                        0.0.0.2
   Net  0.0.0.2        0.0.0.4        1043 8000001e                        0.0.0.4
   Net  0.0.0.2        0.0.0.4        1043 8000001e                        0.0.0.2
   Net  0.0.0.3        0.0.0.4        1033 8000001e                        0.0.0.4
   Net  0.0.0.3        0.0.0.4        1033 8000001e                        0.0.0.3
   INP  0.0.0.0        0.0.0.2        1037 80000022           2001:db8:1341:1::/64
   INP  0.0.0.2        0.0.0.3        1038 8000001e          2001:db8:1341:12::/64
   INP  0.0.0.0        0.0.0.4        1033 80000022           2001:db8:1341:3::/64
   INP  0.0.0.2        0.0.0.4        1043 8000001e          2001:db8:1341:13::/64
   INP  0.0.0.3        0.0.0.4        1033 8000001e          2001:db8:1341:23::/64

        I/F Scoped Link State Database (I/F lo in Area 0.0.0.0)

   Type LSId           AdvRouter       Age   SeqNum                        Payload

        I/F Scoped Link State Database (I/F r1-eth0 in Area 0.0.0.0)

   Type LSId           AdvRouter       Age   SeqNum                        Payload
   Lnk  0.0.0.3        0.0.0.2        1044 8000001e      fe80::5825:b0ff:fe60:abaa
   Lnk  0.0.0.2        0.0.0.3        1045 8000001f      fe80::68bc:b4ff:fe19:42b7

        I/F Scoped Link State Database (I/F r1-eth1 in Area 0.0.0.0)

   Type LSId           AdvRouter       Age   SeqNum                        Payload
   Lnk  0.0.0.4        0.0.0.2        1044 8000001f      fe80::84eb:5dff:fe5b:dc9d
   Lnk  0.0.0.2        0.0.0.4        1046 8000001e      fe80::c088:51ff:fee7:1def

        I/F Scoped Link State Database (I/F r1-eth2 in Area 0.0.0.0)

   Type LSId           AdvRouter       Age   SeqNum                        Payload
   Lnk  0.0.0.2        0.0.0.2        1044 8000001e      fe80::40d0:61ff:fed9:bccf

        AS Scoped Link State Database

   Type LSId           AdvRouter       Age   SeqNum                        Payload


We can also use the packet traces that were collected by tcpdump_ to observe the packets that the OSPFv3 daemons exchange. OSPFv3 is a more complex protocol that the basic link state protocol that we have described in this book, but you should be able to understand some of these packets. The packet traces are available as :download:`/exercises/traces/ospf6-r1-trace.pcap`, :download:`/exercises/traces/ospf6-r2-trace.pcap` and :download:`/exercises/traces/ospf6-r3-trace.pcap`. Here are a few interesting packets collected on router ``r1``.

The first packet that this router received his a Hello packet that was sent by router ``r2``. There are several interesting points to note about this packet. First, its source address is the link-local address (``fe80::68bc:b4ff:fe19:42b7``) of router ``r2`` on this interface. The destination address of the packet is reserved IPv6 multicast address for OSPFv3, i.e. ``ff02::5``. The Hop Limit of the packet is set to 1 and OSFPv3 uses a next header of type 89.

.. figure:: /exercises/figures/ospf6-packet1.png

The Hello packet contains some parameters such as the `Hello interval` that is set to 1 second. This interval is the delay between the transmission of successive Hello packets. Since the `Router Dead Interval` is set to 3 seconds, the router will consider the link as down if it does not receive Hello packets during a period of 3 seconds. The second packet of the trace is sent by router ``r1``. 

.. figure:: /exercises/figures/ospf6-packet2.png

We can then observe the Database description packet that is sent by routers to announce the state of their OSPFv3 database. The details of this packet are beyond the scope of this simple exercise. 
	    
.. figure:: /exercises/figures/ospf6-packet3.png
	    
This packet is updated when new information is added in the router's OSPFv3 database. A few seconds router, this router sends another Database description packet that announces more information.

.. figure:: /exercises/figures/ospf6-packet4.png

Router ``r2`` reacts to this updated Database description packet by requesting the link state information that it does not already know. For this, it sends a `LS Request` packet.

.. figure:: /exercises/figures/ospf6-packet5.png
	    
The requested information is sent in a `LS Update` packet shortly after that.

.. figure:: /exercises/figures/ospf6-packet6.png

OSPFv3 also includes `LS Acknowledge` packets that acknowledge the correct reception of link state information.

.. figure:: /exercises/figures/ospf6-packet7.png
	    
A more detailed discussion of the packets that routing protocols exchange may be found in [Goralski2009]_. 

Exploring RIP
-------------

IPMininet_ can also be used to perform experiments with RIP. A simple script that uses RIPng is provided below.

.. code-block:: python

   import shlex
   from ipmininet.iptopo import IPTopo
   from ipmininet.router.config import RIPng, RouterConfig
   from ipmininet.ipnet import IPNet
   from ipmininet.cli import IPCLI

   class MyTopology(IPTopo):

     def build(self, *args, **kwargs):

        # RouterConfig ensures that OSPF is not automatically started
        r1 = self.addRouter("r1", config=RouterConfig) 
        r2 = self.addRouter("r2", config=RouterConfig)
        r3 = self.addRouter("r3", config=RouterConfig)
        a = self.addHost("a")
        b = self.addHost("b")

        lr1r2 = self.addLink(r1, r2, igp_cost=1)
        lr1r2[r1].addParams(ip=("2001:db8:1341:12::1/64"))
        lr1r2[r2].addParams(ip=("2001:db8:1341:12::2/64"))

        lr1r3 = self.addLink(r1, r3, igp_cost=5)
        lr1r3[r1].addParams(ip=("2001:db8:1341:13::1/64"))
        lr1r3[r3].addParams(ip=("2001:db8:1341:13::3/64"))

        lr2r3 = self.addLink(r2, r3, igp_cost=3)
        lr2r3[r2].addParams(ip=("2001:db8:1341:23::2/64"))
        lr2r3[r3].addParams(ip=("2001:db8:1341:23::3/64"))
        
        lr1a = self.addLink(r1, a)
        lr1a[r1].addParams(ip=("2001:db8:1341:1::1/64"))
        lr1a[a].addParams(ip=("2001:db8:1341:1::A/64"))

        lr3b = self.addLink(r3, b)
        lr3b[r3].addParams(ip=("2001:db8:1341:3::3/64"))
        lr3b[b].addParams(ip=("2001:db8:1341:3::B/64"))


        r1.addDaemon(RIPng)
        r2.addDaemon(RIPng)
        r3.addDaemon(RIPng)

        super(MyTopology, self).build(*args, **kwargs)
        
      def post_build(self, net):
        for r in self.routers():
            command="/usr/sbin/tcpdump --immediate-mode -c 10 -w ./ripng-"+r+"-trace.pcap udp port 521"
            p = net[r].popen(shlex.split(command))
            
        super(MyTopology, self).post_build(net)

   net = IPNet(topo=MyTopology(), allocate_IPs=False)  # Disable IP auto-allocation
   try:
      net.start()
      IPCLI(net)
   finally:
      net.stop()

As RIP messages are exchanged using UDP on port 521, we filter this port in the tcpdump_ trace. RIPng distributes the routes and our two hosts can exchange packets. The entire script is available from :download:`/exercises/ipmininet_scripts/ripng.py`.

.. code-block:: console

   mininet> ping6all
   *** Ping: testing reachability over IPv6
   a --IPv6--> b 
   b --IPv6--> a 
   *** Results: 0% dropped (2/2 received)
   mininet> a traceroute6 -n 2001:db8:1341:3::b
   traceroute to 2001:db8:1341:3::b (2001:db8:1341:3::b) from 2001:db8:1341:1::a, 30 hops max, 24 byte packets
   1  2001:db8:1341:1::1  0.078 ms  0.074 ms  0.051 ms
   2  2001:db8:1341:13::3  0.071 ms  0.072 ms  0.212 ms
   3  2001:db8:1341:3::b  0.199 ms  0.08 ms  0.835 ms
   mininet> b traceroute6 -n 2001:db8:1341:1::a
   traceroute to 2001:db8:1341:1::a (2001:db8:1341:1::a) from 2001:db8:1341:3::b, 30 hops max, 24 byte packets
   1  2001:db8:1341:3::3  0.06 ms  0.022 ms  0.018 ms
   2  2001:db8:1341:13::1  0.038 ms  0.024 ms  0.022 ms
   3  2001:db8:1341:1::a  0.03 ms  0.023 ms  0.022 ms
   mininet> 

We can observe the RIPng messages that are exchanged over the network. :rfc:`2080` defines two types of RIPng messages:

 - the requests
 - the responses that contain the router's routing table

When a router starts, it sends a request message. This is illustrated in the figure below with the first message sent by router ``r2``. This message is sent inside an IPv6 packet whose source address is the link-local address of the router and the destination address is ``ff02::9`` which is the reserved multicast address for RIPng.

.. figure:: /exercises/figures/ripng-packet1.png

Router ``r2`` receives a similar request from ``fe80::481a:48ff:fed7:292e`` and replies by sending its routing table in a response message. Note that this message is sent to the link-local address of the requesting router.

.. figure:: /exercises/figures/ripng-packet2.png

Later, router ``r2`` will regularly transmit its distance vector inside an unsolicited response message that is sent towards the IPv7 multicast address ``ff02::9``.

.. figure:: /exercises/figures/ripng-packet2.png

The packet traces collected on the three routers of this example are available from :download:`/exercises/traces/ripng-r1-trace.pcap`, :download:`/exercises/traces/ripng-r2-trace.pcap` and :download:`/exercises/traces/ripng-r3-trace.pcap`. 
	    
    
Exploring BGP
-------------

To explore the configuration of BGP, let us consider a network that contains three ASes: ``AS1``,  ``AS2`` and ``AS3``. To simplify the tests, we identify one host inside each of these ASes.

     .. tikz:: A simple Internet
        :libs: shapes, positioning, matrix, arrows, shapes 

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
	\tikzset{as/.style={cloud, draw,cloud puffs=10,cloud puff arc=120, aspect=2, minimum height=1em, minimum width=1em} }

        \node[host] (h1) {h1};
        \node[as, right=of h1] (AS1) {AS1};
        \node[as, right=of AS1] (AS2) {AS2};
	\node[host, right=of AS2] (h2) {h2};
        \node[as, below right=of AS1] (AS3) {AS3};
	\node[host, right=of AS3] (h3) {h3};


	% customer provider
	\draw[->, color=red, line width=1.5mm]
        (AS1) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS2) 
	(AS2) edge  node [pos=0.5, sloped, below, color=red] {\texttt{\$}} (AS3);
	%shared cost
	\path[draw, color=blue, line width= 1 mm]
	(AS1) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS3);

	% hosts
	\path[draw, color=black]
	(AS1) edge (h1)
	(AS2) edge (h2)
	(AS3) edge (h3);



.. code-block:: python
		
   import ipmininet.router.config.bgp as _bgp
   from ipmininet.iptopo import IPTopo
   from ipmininet.router.config import BGP, ebgp_session, AF_INET6, CLIENT_PROVIDER, SHARE

   from ipmininet.ipnet import IPNet
   from ipmininet.cli import IPCLI

   class MyTopology(IPTopo):
      """Creates a very simple interdomain topology"""
      def build(self, *args, **kwargs):
        """
        AS1 --$--> AS2 --$--> AS3
         |                     |
         +-----------=---------+ 
        """

As in the previous examples, we create the routers and associate one IPv6 prefix to each AS:

 - ``AS1`` is assigned ``2001:cafe:1::/48``
 - ``AS2`` is assigned ``2001:cafe:2::/48``
 - ``AS3`` is assigned ``2001:cafe:3::/48``   

.. code-block:: python

   # Add all routers
   as1 = self.addRouter('as1')
   as2 = self.addRouter('as2')
   as3 = self.addRouter('as3')
   
   routers=self.routers()
   prefix = {routers[i]: '2001:cafe:%04x::/48' % (i+1) for i in range(len(routers ))}		

   as1.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as1],)),))
   as2.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as2],)),))
   as3.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as3],)),))

The `addDaemon` method adds a BGP daemon on each router and configures it to advertise the IPv6 prefix allocated to this AS. We then create all the links and manually assign one IPv6 subnet to each link and one IPv6 address to each interface. For the interdomain links, we use an IPv6 prefix that belongs to one of the attached ASes.

.. code-block:: python

	# Add hosts

        h1= self.addHost("h1")
        h2= self.addHost("h2")
        h3= self.addHost("h3")
        

        # Add all links
        l12=self.addLink(as1, as2)
        l12[as1].addParams(ip="2001:cafe:1:12::1/64")
        l12[as2].addParams(ip="2001:cafe:1:12::2/64")
        
        l13=self.addLink(as1, as3)
        l13[as1].addParams(ip="2001:cafe:1:13::1/64")
        l13[as3].addParams(ip="2001:cafe:1:13::3/64")
        l23=self.addLink(as2, as3)
        l23[as2].addParams(ip="2001:cafe:2:23::2/64")
        l23[as3].addParams(ip="2001:cafe:2:23::3/64")

        # Links to the hosts
        las1h1 = self.addLink(as1, h1)
        las1h1[as1].addParams(ip=("2001:cafe:1:1::1/64"))
        las1h1[h1].addParams(ip=("2001:cafe:1:1::11/64"))

        las2h2 = self.addLink(as2, h2)
        las2h2[as2].addParams(ip=("2001:cafe:2:1::2/64"))
        las2h2[h2].addParams(ip=("2001:cafe:2:1::12/64"))

        las3h3 = self.addLink(as3, h3)
        las3h3[as3].addParams(ip=("2001:cafe:3:1::3/64"))
        las3h3[h3].addParams(ip=("2001:cafe:3:1::13/64"))


The last step is to specify to which AS each router belongs and to configure the eBGP sessions and their routing policies. IPMininet_ abstracts most of the complexity of the configuration of these policies by supporting two policies

.. code-block:: python
        
        # Set AS-ownerships
        self.addAS(1, (as1,))
        self.addAS(2, (as2,))
        self.addAS(3, (as3,))
        
        # Add eBGP sessions
	# AS1 is a client of AS2
        ebgp_session(self, as1, as2, link_type=CLIENT_PROVIDER)
	# AS2 is a client of AS3
        ebgp_session(self, as2, as3, link_type=CLIENT_PROVIDER)
	# AS1 and AS3 are shared cost peers
        ebgp_session(self, as1, as3, link_type=SHARE)
 
        super(MyTopology, self).build(*args, **kwargs)

The script ends by launching the full topology. The entire script is available from :download:`/exercises/ipmininet_scripts/ebgp-simple.py`.

We can now run this simple network.

.. code-block:: console

   sudo python3 ebgp-simple.py

If you launch the script and immediately type ``ping6all`` to check the connectivity, you might obtained the following result.

.. code-block:: console

   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> X X 
   h2 --IPv6--> X X  
   h3 --IPv6--> X X 
   *** Results: 100% dropped (0/6 received)

Remember that BGP is a distributed protocol and that it takes some time to launch the daemons and exchange the messages. After some time, the same command will confirm that everything works as expected.

.. code-block:: console

   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> h2 h3 
   h2 --IPv6--> h1 h3 
   h3 --IPv6--> h2 h1 
   *** Results: 0% dropped (6/6 received)

We can also use :manpage:`traceroute6(8)` to check the path followed by the packets. Before doing that, think about the configuration of the BGP routing policies and try to predict the output of :manpage:`traceroute6(8)`. This is a good exercise to check your understanding of BGP.

We have configured the following addresses on the hosts.

.. code-block:: console

   mininet> h1 ip -6 -o addr show 
   1: lo    inet6 ::1/128 scope host \       valid_lft forever preferred_lft forever
   2: h1-eth0    inet6 2001:cafe:1:1::11/64 scope global \       valid_lft forever preferred_lft forever
   2: h1-eth0    inet6 fe80::8ae:b0ff:fe9d:aefa/64 scope link \       valid_lft forever preferred_lft forever
   mininet> h2 ip -6 -o addr show 
   1: lo    inet6 ::1/128 scope host \       valid_lft forever preferred_lft forever
   2: h2-eth0    inet6 2001:cafe:2:1::12/64 scope global \       valid_lft forever preferred_lft forever
   2: h2-eth0    inet6 fe80::d8a3:cdff:fed6:14ad/64 scope link \       valid_lft forever preferred_lft forever
   mininet> h3 ip -6 -o addr show 
   1: lo    inet6 ::1/128 scope host \       valid_lft forever preferred_lft forever
   2: h3-eth0    inet6 2001:cafe:3:1::13/64 scope global \       valid_lft forever preferred_lft forever
   2: h3-eth0    inet6 fe80::101d:e1ff:fe4e:a3a9/64 scope link \       valid_lft forever preferred_lft forever

We can now explore the routes in this small Internet. Host ``h1`` can reach directly host ``h3``.

.. code-block:: console

   mininet> h1 traceroute6 -n 2001:cafe:3:1::13
   traceroute to 2001:cafe:3:1::13 (2001:cafe:3:1::13) from 2001:cafe:1:1::11, 30 hops max, 24 byte packets
   1  2001:cafe:1:1::1  0.099 ms  0.038 ms  0.056 ms
   2  2001:cafe:2:23::3  2.3 ms  0.135 ms  0.161 ms
   3  2001:cafe:3:1::13  0.216 ms  0.182 ms  0.187 ms
		
Note that the path preferred by ``AS3`` to reach ``AS1`` is different.

.. code-block:: console

   mininet> h3 traceroute6 -n 2001:cafe:1:1::11
   traceroute to 2001:cafe:1:1::11 (2001:cafe:1:1::11) from 2001:cafe:3:1::13, 30 hops max, 24 byte packets
   1  2001:cafe:3:1::3  0.133 ms  0.088 ms  0.078 ms
   2  2001:cafe:2:23::2  0.099 ms  0.085 ms  0.086 ms
   3  2001:cafe:1:13::1  0.103 ms  0.097 ms  0.083 ms
   4  2001:cafe:1:1::11  0.075 ms  0.037 ms  0.062 ms


The same applies for the paths between ``h1`` and ``h2``
   
.. code-block:: console

   mininet> h1 traceroute6 -n 2001:cafe:2:1::12
   traceroute to 2001:cafe:2:1::12 (2001:cafe:2:1::12) from 2001:cafe:1:1::11, 30 hops max, 24 byte packets
   1  2001:cafe:1:1::1  0.102 ms  0.03 ms  0.026 ms
   2  2001:cafe:2:23::3  0.051 ms  0.034 ms  0.033 ms
   3  2001:cafe:1:12::2  0.036 ms  0.034 ms  0.031 ms
   4  2001:cafe:2:1::12  0.043 ms  0.207 ms  0.17 ms
   mininet> h2 traceroute6 -n 2001:cafe:1:1::11
   traceroute to 2001:cafe:1:1::11 (2001:cafe:1:1::11) from 2001:cafe:2:1::12, 30 hops max, 24 byte packets
   1  2001:cafe:2:1::2  0.075 ms  0.088 ms  0.029 ms
   2  2001:cafe:1:13::1  0.059 ms  0.052 ms  0.034 ms
   3  2001:cafe:1:1::11  0.05 ms  0.036 ms  0.031 ms
	

Besides :manpage:`ping6(8)` and :manpage:`traceroute6(8)`, it is also useful to interact with the BGP daemon that runs on each of our routers. This is done by connecting on the Command Line Interface of the BGP router using telnet.

.. code-block:: console

   mininet> noecho as1 telnet localhost bgpd
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.

   Hello, this is FRRouting (version 7.1).
   Copyright 1996-2005 Kunihiro Ishiguro, et al.


   User Access Verification
		
   Password:

.. spelling::

   Quagga
   
The password for the BGP daemon is `zebra`. The `noecho` command indicates that mininet_ does not need to echo the characters that you type. You then enter the Quagga VTY that enables you to type commands. The `help` commands gives you some information about the available commands as well as `?`

.. code-block:: console

   as1> help
   Quagga VTY provides advanced help feature.  When you need help,
   anytime at the command line please press '?'.

   If nothing matches, the help list will be empty and you must backup
   until entering a '?' shows the available options.
   Two styles of help are provided:
   1. Full help is available when you are ready to enter a
      command argument (e.g. 'show ?') and describes each possible
      argument.
   2. Partial help is provided when an abbreviated argument is entered
      and you want to know what arguments match the input
      (e.g. 'show me?'.)

   as1> 
   enable    Turn on privileged mode command
   exit      Exit current mode and down to previous mode
   find      Find CLI command containing text
   help      Description of the interactive help system
   list      Print command list
   quit      Exit current mode and down to previous mode
   show      Show running system information
   terminal  Set terminal line parameters
   who       Display who is on vty
   as1> 

In these exercises, we mainly consider the ``show`` that extracts information from the BGP daemon. We type `show bgp` and press the `tabulation` key to see the available commands in the `show bgp`.

.. code-block:: console

   as1> show bgp 
   as-path-access-list attribute-info cidr-only  community  community-info community-list 
   dampening  detail     extcommunity-list filter-list import-check-table ipv4       
   ipv6       json       l2vpn      large-community large-community-list mac        
   martian    memory     multicast  neighbors  nexthop    paths      
   peer-group peerhash   prefix-list regexp     route-leak route-map  
   statistics summary    unicast    update-groups view       views      
   vpn        vrf        vrfs       


A useful command to start is `show bgp summary` which provides a summary of the state of the BGP daemon.

.. code-block:: console

   as1> show bgp summary 

   IPv6 Unicast Summary:
   BGP router identifier 192.168.8.2, local AS number 1 vrf-id 0
   BGP table version 10
   RIB entries 5, using 800 bytes of memory
   Peers 2, using 41 KiB of memory

   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::2 4          2      52      51        0    0    0 00:15:21            2
   2001:cafe:1:13::3 4          3      51      50        0    0    0 00:15:21            2

   Total number of neighbors 2

.. spelling::

   Keepalive

This router (`as1`) has two BGP neighbors: ``2001:cafe:1:12::2`` and ``2001:cafe:1:13::3``. Both BGP sessions are established using the current version of the protocol (version 4). About 50 messages were sent/received over each session. These messages are mainly the BGP Keepalive messages that are exchanged every 30 seconds. The last column indicates that two prefixes were received over each session. We can see more details about these two eBGP sessions with the `show bgp neighbors` command.

.. code-block:: console

   as1> show bgp ipv6 neighbors 

   BGP neighbor is 2001:cafe:1:12::2, remote AS 2, local AS 1, external link
     Description: as2 (eBGP)
   Hostname: as2
   BGP version 4, remote router ID 192.168.3.1, local router ID 192.168.8.2
   BGP state = Established, up for 00:41:48
   Last read 00:00:48, Last write 00:00:48
   Hold time is 180, keepalive interval is 60 seconds
   Neighbor capabilities:
    4 Byte AS: advertised and received
    AddPath:
      IPv6 Unicast: RX advertised IPv6 Unicast and received
    Route refresh: advertised and received(old & new)
    Address Family IPv6 Unicast: advertised and received
    Hostname Capability: advertised (name: as1,domain name: n/a) received (name: as2,domain name: n/a)
    Graceful Restart Capabilty: advertised and received
      Remote Restart timer is 120 seconds
      Address families by peer:
        none
   Graceful restart information:
    End-of-RIB send: IPv6 Unicast
    End-of-RIB received: IPv6 Unicast
   Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  2          2
    Notifications:          2          0
    Updates:                5          9
    Keepalives:            67         66
    Route Refresh:          1          1
    Capability:             0          0
    Total:                 77         78
   Minimum time between advertisement runs is 0 seconds

   For address family: IPv6 Unicast
    Update group 4, subgroup 4
    Packet Queue length 0
    NEXT_HOP is always this router
    Community attribute sent to this neighbor(all)
    Inbound path policy configured
    Outbound path policy configured
    Route map for incoming advertisements is *rm3-ipv6
    Route map for outgoing advertisements is *export-to-up-as2-ipv6
    2 accepted prefixes

    Connections established 2; dropped 1
    Last reset 00:41:49, due to NOTIFICATION sent (Hold Timer Expired)
    External BGP neighbor may be up to 255 hops away.
    Local host: 2001:cafe:1:12::1, Local port: 179
    Foreign host: 2001:cafe:1:12::2, Foreign port: 51406
    Nexthop: 192.168.0.1
    Nexthop global: 2001:cafe:1:12::1
    Nexthop local: fe80::fca2:adff:fe20:4cb1
    BGP connection: shared network
    BGP Connect Retry Timer in Seconds: 120
    Read thread: on  Write thread: on

    BGP neighbor is 2001:cafe:1:13::3, remote AS 3, local AS 1, external link
    Description: as3 (eBGP)
     Hostname: as3
     BGP version 4, remote router ID 192.168.6.1, local router ID 192.168.8.2
     BGP state = Established, up for 00:41:48
     Last read 00:00:48, Last write 00:00:48
     Hold time is 180, keepalive interval is 60 seconds
     Neighbor capabilities:
      4 Byte AS: advertised and received
     AddPath:
      IPv6 Unicast: RX advertised IPv6 Unicast and received
    Route refresh: advertised and received(old & new)
    Address Family IPv6 Unicast: advertised and received
    Hostname Capability: advertised (name: as1,domain name: n/a) received (name: as3,domain name: n/a)
    Graceful Restart Capabilty: advertised and received
      Remote Restart timer is 120 seconds
      Address families by peer:
        none
    Graceful restart information:
     End-of-RIB send: IPv6 Unicast
     End-of-RIB received: IPv6 Unicast
    Message statistics:
     Inq depth is 0
     Outq depth is 0
                         Sent       Rcvd
    Opens:                  2          2
    Notifications:          2          0
    Updates:                5          8
    Keepalives:            66         66
    Route Refresh:          1          1
    Capability:             0          0
    Total:                 76         77
    Minimum time between advertisement runs is 0 seconds

    For address family: IPv6 Unicast
     Update group 3, subgroup 3
     Packet Queue length 0
     NEXT_HOP is always this router
     Community attribute sent to this neighbor(all)
     Inbound path policy configured
     Outbound path policy configured
     Route map for incoming advertisements is *rm13-ipv6
     Route map for outgoing advertisements is *export-to-peer-as3-ipv6
     2 accepted prefixes

     Connections established 2; dropped 1
     Last reset 00:41:49, due to Peer closed the session
     External BGP neighbor may be up to 255 hops away.
     Local host: 2001:cafe:1:13::1, Local port: 179
     Foreign host: 2001:cafe:1:13::3, Foreign port: 41630
     Nexthop: 192.168.4.2
     Nexthop global: 2001:cafe:1:13::1
     Nexthop local: fe80::f823:70ff:fe80:37c4
     BGP connection: shared network
     BGP Connect Retry Timer in Seconds: 120
     Read thread: on  Write thread: on


.. spelling::

   BGP
   Loc
   RIB

We can now observe the BGP-Loc-RIB of the router with the ``show bgp ipv6 command`` command.

.. code-block:: console

   as1> show bgp ipv6    
   BGP table version is 10, local router ID is 192.168.8.2, vrf id 0
   Default local pref 100, local AS 1
   Status codes:  s suppressed, d damped, h history, * valid, > best, = multipath,
		  i internal, r RIB-failure, S Stale, R Removed
   Nexthop codes: @NNN nexthop's vrf id, < announce-nh-self
   Origin codes:  i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
   *> 2001:cafe:1::/48 ::                       0         32768 i
   *> 2001:cafe:2::/48 fe80::3c81:2eff:fe19:465d
                                                  150      0 3 2 i
   *                   fe80::c001:dcff:fe49:a512
                                             0    100      0 2 i
   *  2001:cafe:3::/48 fe80::c001:dcff:fe49:a512
                                                  100      0 2 3 i
   *>                  fe80::3c81:2eff:fe19:465d
                                             0    150      0 3 i

   Displayed  3 routes and 5 total paths


It is interesting to look at the output of this command in details. Router `as1` has routes for three different IPv6 prefixes. The first prefix is its own prefix, ``2001:cafe:1::/48``. It has no nexthop since this prefix is originated by the router. Then, `as1` has received two paths for ``2001:cafe:2::/48``. In the BGP Loc-RIB, the `>` character indicates the best route according to the BGP decision process.  ``2001:cafe:2::/48`` was learned over two different BGP sessions:

 - the eBGP session with ``fe80::3c81:2eff:fe19:465d`` with an AS-Path of ``AS3:AS2`` (see last column)
 - the eBGP session with ``fe80::c001:dcff:fe49:a512`` with an AS-Path of ``AS2`` (see last column)  

The first of these two routes is preferred as indicated by the `>` character because it has a higher ``local-preference` (150) than the second one (100). For prefix ``2001:cafe:3::/48``, the route learned via ``fe80::3c81:2eff:fe19:465d`` is also preferred for the same reason.
   
IPMininet_ also allows to explore the dynamics of BGP by looking at the packets that the routers exchange. For this, we slightly modify the example above and add delays to the interdomain links as follows.

.. code-block:: python

   l12=self.addLink(as1, as2, delay='10ms')
   l13=self.addLink(as1, as3, delay='10ms')
   l23=self.addLink(as2, as3, delay='200ms')


We also add a ``post_build`` method to launch tcpdump_ and capture the BGP packets exchanged by the routers. A BGP session runs over a TCP connection. Let us examine a few of the BGP messages exchanged on the BGP session between ``AS1`` and ``AS2``. The traces collected on the three routers are available from :download:`/exercises/traces/bgp-as1-trace.pcap`, :download:`/exercises/traces/bgp-as2-trace.pcap` and :download:`/exercises/traces/bgp-as2-trace.pcap`. 

The BGP session starts with a TCP three-way handshake.
Once the session has been established, both BGP daemons send an ``OPEN`` message describing their capabilities and the BGP extensions that it supports. The details of these extensions go beyond the scope of this book. However, it is important to note that the ``OPEN`` message contains the ``AS`` number of the router that sends the message and its identifier as a 32 bits IPv4 address. This router identifier uniquely identifies the router. The last mandatory parameter of the ``OPEN`` message is the `Hold Time`, i.e. the maximum delay between two successive messages over this BGP session. A BGP router should send ``KEEPALIVE`` messages every one third of the `Hold Time` to keep the session up. 	    

.. figure:: /exercises/figures/bgp-packet2.png

The ``UPDATE`` message can be used to withdraw and advertise routes. The packet below is sent by ``AS2`` to advertise its route towards `2001:cafe:2::/48` on the BGP session with ``AS1``. 
	    
.. figure:: /exercises/figures/bgp-packet2.png

	    
Another interesting utilization of IPMininet_ is to explore how routers react to link failures. We start from the same network as with the previous example and disable the link between ``AS2`` and ``AS3``. For this, we log on one of the two routers and issue the following commands.

.. code-block:: console
		
   mininet> noecho as2 telnet localhost bgpd
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.

   Hello, this is FRRouting (version 7.1).
   Copyright 1996-2005 Kunihiro Ishiguro, et al.


   User Access Verification

   Password: 
   as2> enable
   as2# show bgp summary

   IPv6 Unicast Summary:
   BGP router identifier 192.168.8.1, local AS number 2 vrf-id 0
   BGP table version 5
   RIB entries 5, using 800 bytes of memory
   Peers 2, using 41 KiB of memory

   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::1 4          1      13      17        0    0    0 00:07:28            1
   2001:cafe:2:23::3 4          3      20      20        0    0    0 00:00:55            1

   Total number of neighbors 2


We first connect to the BGP daemon on router `as2`. In addition to the `show` commands that have been described earlier, the router also supports privileged commands that can change its configuration. Before executing these commands, we must enter the privileged mode with the `enable` command. On production routers, this command requires a password to verify the credentials of the network administrator. The `#` prompt indicates that we are allowed to execute privileged commands. We first check the state of the BGP sessions with the `show bgp summary` commands. There are two BGP sessions configured on this router.

We can now disable one of the BGP sessions on router `as2` as follows.

.. code-block:: console

   as2# configure terminal
   as2(config)# router bgp 2
   as2(config-router)# neighbor 2001:cafe:2:23::3 shutdown
   as2(config-router)# exit
   as2(config)# exit


We start indicate that we will use the terminal to change the router configuration with `configure terminal`. We then enter the BGP part of the configuration with `router bgp 2` (`2` is the AS number of `as2`). Then we use the `neighbor 2001:cafe:2:23::3 shutdown` that takes as parameter the IP address of the peer of the session that we want to stop. We then leave the BGP part of the configuration (first `exit`) and the configuration menu (second `exit` command). At this point, the BGP session between ``AS2`` and ``AS3`` is down.

.. code-block:: console
   
   as2# show bgp summary

   IPv6 Unicast Summary:
   BGP router identifier 192.168.8.1, local AS number 2 vrf-id 0
   BGP table version 6
   RIB entries 3, using 480 bytes of memory
   Peers 2, using 41 KiB of memory

   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::1 4          1      14      19        0    0    0 00:08:02            1
   2001:cafe:2:23::3 4          3      21      23        0    0    0 00:00:10 Idle (Admin)

   Total number of neighbors 2
   as2# exit

Without a BGP session between ``AS2`` and ``AS3``, there are reachability problems in this simple Internet.

.. code-block:: console
		
   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> h2 h3 
   h2 --IPv6--> X h1 
   h3 --IPv6--> X h1 
   *** Results: 33% dropped (4/6 received)

We can fix them by enabling again the BGP session with the `no neighbor 2001:cafe:2:23::3 shutdown` command.

.. code-block:: console

   mininet> noecho as2 telnet localhost bgpd
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.
   
   Hello, this is FRRouting (version 7.1).
   Copyright 1996-2005 Kunihiro Ishiguro, et al.


   User Access Verification

   Password: 
   as2> enable
   as2# configure terminal
   as2(config)# router bgp 2
   as2(config-router)# no neighbor 2001:cafe:2:23::3 shutdown
   as2(config-router)# exi
   as2(config)# exit
   as2# show bgp summary

   IPv6 Unicast Summary:
   BGP router identifier 192.168.8.1, local AS number 2 vrf-id 0
   BGP table version 7
   RIB entries 5, using 800 bytes of memory
   Peers 2, using 41 KiB of memory
   
   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::1 4          1      15      21        0    0    0 00:09:30            1
   2001:cafe:2:23::3 4          3      28      28        0    0    0 00:00:07            1

   Total number of neighbors 2
   as2# exit
   Connection closed by foreign host.
   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> h2 h3 
   h2 --IPv6--> h3 h1 
   h3 --IPv6--> h2 h1 
   *** Results: 0% dropped (6/6 received)

   

   
Exercises
---------

We can use IPMininet_ to prepare some networks with problems that need to be analyzed and corrected.

1. Our first example is a small Internet with 5 ASes. A subset of the script that configures this network is shown below. There is one host attached to each AS and this host has the same number as its AS. The entire script is available from :download:`/exercises/ipmininet_scripts/ebgp-bug.py`.

   .. code-block:: python

        l12=self.addLink(as1, as2, delay='10ms')
        l13=self.addLink(as1, as3, delay='10ms')
        l23=self.addLink(as2, as3, delay='10ms')
        l15=self.addLink(as1, as5, delay='10ms')
        l24=self.addLink(as2, as4, delay='10ms')
        l34=self.addLink(as3, as4, delay='10ms')
        l45=self.addLink(as4, as5, delay='10ms')
        
        # Add eBGP sessions
        ebgp_session(self, as2, as1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as3, as1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as5, as1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as3, as4, link_type=CLIENT_PROVIDER)
       
        ebgp_session(self, as2, as3, link_type=SHARE)
        ebgp_session(self, as2, as4, link_type=SHARE)
        ebgp_session(self, as4, as5, link_type=SHARE)


 When this network is launched, `ping6all` reports connectivity problems. Hosts `h1` and `h4` cannot exchange packets. Can you fix the problem by changing the routing policy used on only one interdomain link ? Justify your answer

 .. code-block:: console
		 
    mininet> ping6all
    *** Ping: testing reachability over IPv6
    h1 --IPv6--> h2 h5 X h3 
    h2 --IPv6--> h3 h1 h4 h5 
    h3 --IPv6--> h2 h1 h4 h5 
    h4 --IPv6--> h2 X h5 h3 
    h5 --IPv6--> h2 h1 h4 h3 
    *** Results: 10% dropped (18/20 received)

2. Another interesting utilization IPMininet_ is to explore the impact of a link failure. We start from a small variant of the above topology.

 .. code-block:: python

    l12=self.addLink(as1, as2, delay='10ms')
    l13=self.addLink(as1, as3, delay='10ms')
    l23=self.addLink(as2, as3, delay='10ms')
    l15=self.addLink(as1, as5, delay='10ms')
    l24=self.addLink(as2, as4, delay='10ms')
    l34=self.addLink(as3, as4, delay='10ms')
    l45=self.addLink(as4, as5, delay='10ms')
    l25=self.addLink(as2, as5, delay='10ms')
    # Add eBGP sessions
    ebgp_session(self, as2, as1, link_type=CLIENT_PROVIDER)
    ebgp_session(self, as3, as1, link_type=CLIENT_PROVIDER)
    ebgp_session(self, as5, as1, link_type=CLIENT_PROVIDER)
    ebgp_session(self, as4, as3, link_type=CLIENT_PROVIDER)
    
    ebgp_session(self, as2, as3, link_type=SHARE)
    ebgp_session(self, as2, as4, link_type=SHARE)
    ebgp_session(self, as4, as5, link_type=SHARE)
    ebgp_session(self, as2, as5, link_type=SHARE)		 

When this network starts, all hosts can reach all other hosts.

.. code-block:: console

   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> h4 h3 h2 h5 
   h2 --IPv6--> h4 h1 h3 h5 
   h3 --IPv6--> h4 h1 h2 h5 
   h4 --IPv6--> h1 h3 h2 h5 
   h5 --IPv6--> h4 h1 h3 h2 
   *** Results: 0% dropped (20/20 received)


Draw the network and try to predict how it will react to a shutdown of any of the customer-provider links ?

a. What are the BGP messages that will be exchanged when the link between ``AS1`` and ``AS2`` fails ? How does this affect the reachability of the different hosts ?

..
   Failure of AS1-AS2
   
   as1# show bgp sum

   IPv6 Unicast Summary:
   BGP router identifier 192.168.16.1, local AS number 1 vrf-id 0
   BGP table version 6
   RIB entries 7, using 1120 bytes of memory
   Peers 3, using 62 KiB of memory

   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::2 4          2      10      19        0    0    0 00:00:09 Idle (Admin)
   2001:cafe:1:13::3 4          3      11      18        0    0    0 00:05:16            2
   2001:cafe:1:15::5 4          5      10      20        0    0    0 00:05:14            1

   Total number of neighbors 3
   as1# exit
   Connection closed by foreign host.
   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> h4 h3 X h5 
   h2 --IPv6--> h4 X h3 h5 
   h3 --IPv6--> h4 h1 h2 h5 
   h4 --IPv6--> h1 h3 h2 h5 
   h5 --IPv6--> h4 h1 h3 h2 
   *** Results: 10% dropped (18/20 received)

b. What are the BGP messages that will be exchanged when the link between ``AS1`` and ``AS3`` fails ? How does this affect the reachability of the different hosts ?

..
   Failure of AS1-AS3

   as1# sh bgp sum

   IPv6 Unicast Summary:
   BGP router identifier 192.168.16.1, local AS number 1 vrf-id 0
   BGP table version 9
   RIB entries 5, using 800 bytes of memory
   Peers 3, using 62 KiB of memory
   
   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::2 4          2      14      28        0    0    0 00:00:21            1
   2001:cafe:1:13::3 4          3      13      23        0    0    0 00:00:05 Idle (Admin)
   2001:cafe:1:15::5 4          5      12      24        0    0    0 00:07:12            1

   Total number of neighbors 3
   as1# exit
   Connection closed by foreign host.
   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> X X h2 h5 
   h2 --IPv6--> h4 h1 h3 h5 
   h3 --IPv6--> h4 X h2 X 
   h4 --IPv6--> X h3 h2 h5 
   h5 --IPv6--> h4 h1 X h2 
   *** Results: 30% dropped (14/20 received)

c. What are the BGP messages that will be exchanged when the link between ``AS1`` and ``AS5`` fails ? How does this affect the reachability of the different hosts ?

..
   Failure of AS1-AS5
   
   as1# sh bgp sum

   IPv6 Unicast Summary:
   BGP router identifier 192.168.16.1, local AS number 1 vrf-id 0
   BGP table version 12
   RIB entries 7, using 1120 bytes of memory
   Peers 3, using 62 KiB of memory
   
   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:12::2 4          2      15      32        0    0    0 00:02:00            1
   2001:cafe:1:13::3 4          3      18      32        0    0    0 00:00:16            2
   2001:cafe:1:15::5 4          5      13      29        0    0    0 00:00:05 Idle (Admin)

   Total number of neighbors 3
   as1# exit
   Connection closed by foreign host.
   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> h4 h3 h2 X 
   h2 --IPv6--> h4 h1 h3 h5 
   h3 --IPv6--> h4 h1 h2 X 
   h4 --IPv6--> h1 h3 h2 h5 
   h5 --IPv6--> h4 X X h2 
   *** Results: 20% dropped (16/20 received)

d. What are the BGP messages that will be exchanged when the link between ``AS3`` and ``AS4`` fails ? How does this affect the reachability of the different hosts ?

.. 
   Failure AS3-AS4

   as3# sh bgp summary 
   
   IPv6 Unicast Summary:
   BGP router identifier 192.168.17.1, local AS number 3 vrf-id 0
   BGP table version 12
   RIB entries 7, using 1120 bytes of memory
   Peers 3, using 62 KiB of memory

   Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
   2001:cafe:1:13::1 4          1      36      22        0    0    0 00:02:19            3
   2001:cafe:2:23::2 4          2      16      17        0    0    0 00:10:55            1
   2001:cafe:3:34::4 4          4      15      30        0    0    0 00:00:05 Idle (Admin)

   Total number of neighbors 3
   as3# exit
   Connection closed by foreign host.
   mininet> ping6all
   *** Ping: testing reachability over IPv6
   h1 --IPv6--> X h3 h2 h5 
   h2 --IPv6--> h4 h1 h3 h5 
   h3 --IPv6--> X h1 h2 h5 
   h4 --IPv6--> X X h2 h5 
   h5 --IPv6--> h4 h1 h3 h2 
   *** Results: 20% dropped (16/20 received)



3. Let us now consider another example. The network contains nine ASes with one host per AS. Assuming that ``AS9`` announces prefix `p9` and that ``AS2`` announces prefix `p2`.

     .. tikz:: A simple Internet
        :libs: shapes, positioning, matrix, arrows, shapes 

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
	\tikzset{as/.style={cloud, draw,cloud puffs=10,cloud puff arc=120, aspect=2, minimum height=1em, minimum width=1em} }

	
        \node[as] (AS2) {AS2};
        \node[as, right=of AS2] (AS3) {AS3};
	\node[as, above=of AS3] (AS4) {AS4};
        \node[as, right=of AS3] (AS6) {AS6};
	\node[as, right=of AS4] (AS5) {AS5};
	\node[as, right=of AS5] (AS7) {AS7};
	\node[as, right=of AS6] (AS8) {AS8};
	\node[as, right=of AS8] (AS1) {AS1};
	\node[as, right=of AS7] (AS9) {AS9};

	% customer provider
	\draw[->, color=red, line width=1.5mm]
        (AS2) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS3)
	(AS3) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS4)
	(AS4) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS5)
	(AS5) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS6)
	(AS5) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS7)
	(AS9) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS7) 
	(AS9) edge  node [pos=0.5, sloped, below, color=red] {\texttt{\$}} (AS1);
	(AS1) edge  node [pos=0.5, sloped, below, color=red] {\texttt{\$}} (AS8);	
	%shared cost
	\path[draw, color=blue, line width= 1 mm]
	(AS3) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS6)
	(AS6) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS8)
	(AS7) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS6);

   a. What is the Loc-RIB of ``AS6`` for prefix `p9` ? Indicate which is the best route towards this prefix.

   b. What is the Loc-RIB of ``AS9`` for prefix `p2` ? Indicate which is the best route towards this prefix.

4. The network below contains nine ASes with one host per AS. Assuming that ``AS1`` announces prefix `p1` and that ``AS2`` announces prefix `p2`.

     .. tikz:: A simple Internet
        :libs: shapes, positioning, matrix, arrows, shapes 

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
	\tikzset{as/.style={cloud, draw,cloud puffs=10,cloud puff arc=120, aspect=2, minimum height=1em, minimum width=1em} }

	\node[as] (AS2) {AS2};
	\node[as, right=of AS2] (AS3) {AS3};
	\node[as, above=of AS3] (AS4) {AS4};
	\node[as, right=of AS3] (AS6) {AS6}; 
	\node[as, above=of AS6] (AS5) {AS5};
	\node[as, right=of AS6] (AS8) {AS8}; 
	\node[as, right=of AS5] (AS7) {AS7};
	\node[as, right=of AS8] (AS1) {AS1};
	% customer provider
	\draw[->, line width=1.5mm]
	(AS2) edge node [pos=0.5, sloped, above] {\texttt{\$}} (AS3)
	(AS3) edge node [pos=0.5, sloped, above] {\texttt{\$}} (AS4)
	(AS4) edge node [pos=0.5, sloped, above] {\texttt{\$}} (AS5)
	(AS7) edge node [pos=0.5, sloped, above] {\texttt{\$}} (AS5)
	(AS5) edge node [pos=0.5, sloped, above] {\texttt{\$}} (AS6)
	(AS1) edge node [pos=0.5, sloped, above] {\texttt{\$}} (AS8);
	\path[draw, line width= 1 mm]
	(AS3) edge node [sloped, midway, above] {\textbf{=}} (AS6)
	(AS6) edge node [sloped, midway, above] {\textbf{=}} (AS8)
	(AS8) edge node [sloped, midway, above] {\textbf{=}}  (AS7);

     
   a. What is the Loc-RIB of ``AS6`` for prefix `p1` ? Indicate which is the best route towards this prefix.

   b. What is the Loc-RIB of ``AS8`` for prefix `p2` ? Indicate which is the best route towards this prefix.




5. Let us now consider another example, also implemented using an IPMininet_ script. The network contains eight ASes with one host per AS. This small Internet is shown below and the script is available from :download:`/exercises/ipmininet_scripts/ebgp-bug-3.py`.


     .. tikz:: A simple Internet
        :libs: shapes, positioning, matrix, arrows, shapes 

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
	\tikzset{as/.style={cloud, draw,cloud puffs=10,cloud puff arc=120, aspect=2, minimum height=1em, minimum width=1em} }
   
        \node[as] (AS1) {AS1};
        \node[as, right=of AS1] (AS2) {AS2};
	\node[as, above=of AS2] (AS3) {AS3};
        \node[as, right=of AS3] (AS4) {AS4};
	\node[as, right=of AS2] (AS5) {AS5};
	\node[as, right=of AS4] (AS7) {AS7};
	\node[as, right=of AS5] (AS6) {AS6};
	\node[as, right=of AS7] (AS8) {AS8};


	% customer provider
	\draw[->, color=red, line width=1.5mm]
        (AS2) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS1)
	(AS1) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS3)
	(AS3) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS4)
	(AS2) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS5)
	(AS4) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS7)
	(AS7) edge node [pos=0.5, sloped, above, color=red] {\texttt{\$}}(AS6) 
	(AS7) edge  node [pos=0.5, sloped, below, color=red] {\texttt{\$}} (AS8);
	%shared cost
	\path[draw, color=blue, line width= 1 mm]
	(AS2) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS3)
	(AS4) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS5)
	(AS5) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS6)
	(AS8) edge node [sloped, midway, above, color=blue] {\textbf{=}} (AS6);



a. The network does not provide a full connectivity. The hosts attached to ``AS5`` cannot ping the hosts attached to ``AS8``.    
   
  ..
     mininet> ping6all
     *** Ping: testing reachability over IPv6
     h1 --IPv6--> X h3 h5 h8 h4 h6 h2 
     h2 --IPv6--> h7 h3 h5 h1 h8 h4 h6 
     h3 --IPv6--> h7 h5 h1 h8 h4 h6 h2 
     h4 --IPv6--> h7 h3 h5 h1 h8 h6 h2 
     h5 --IPv6--> h7 h3 h1 X h4 h6 h2 
     h6 --IPv6--> h7 h3 h5 h1 h8 h4 h2 
     h7 --IPv6--> h3 h5 h1 h8 h4 h6 h2 
     h8 --IPv6--> h7 h3 X h1 h4 h6 h2 
     *** Results: 5% dropped (53/56 received)
     
b. What is the path that packets follow from a host attached to ``AS1`` to a host attached to ``AS8`` ?

   ..
      mininet> h1 traceroute6 -n 2001:cafe:8:1::18
      traceroute to 2001:cafe:8:1::18 (2001:cafe:8:1::18) from 2001:cafe:1:1::11, 30 hops max, 24 byte packets
      1  2001:cafe:1:1::1  0.29 ms  0.06 ms  0.044 ms
      2  2001:cafe:1:13::3  0.053 ms  0.045 ms  0.045 ms
      3  2001:cafe:3:34::4  0.06 ms  0.051 ms  0.047 ms
      4  2001:cafe:4:47::7  0.064 ms  0.053 ms  0.053 ms
      5  2001:cafe:7:78::8  0.207 ms  0.089 ms  0.083 ms
      6  2001:cafe:8:1::18  0.092 ms  0.086 ms  0.082 ms
      
c. What is the path that packets follow from a host attached to ``AS8`` to a host attached to ``AS1`` ?

      ..
         mininet> h8 traceroute6 -n 2001:cafe:1:1::11
	 traceroute to 2001:cafe:1:1::11 (2001:cafe:1:1::11) from 2001:cafe:8:1::18, 30 hops max, 24 byte packets
	 1  2001:cafe:8:1::8  0.103 ms  0.028 ms  0.03 ms
	 2  2001:cafe:7:78::7  0.042 ms  0.032 ms  0.028 ms
	 3  2001:cafe:4:47::4  0.044 ms  0.032 ms  0.03 ms
	 4  2001:cafe:3:34::3  0.047 ms  0.034 ms  0.034 ms
	 5  2001:cafe:1:13::1  0.042 ms  0.036 ms  0.035 ms
	 6  2001:cafe:1:1::11  0.039 ms  0.031 ms  0.029 ms

d. What is the path that packets follow from a host attached to ``AS8`` to a host attached to ``AS2`` ?

     ..
        mininet> h8 traceroute6 -n 2001:cafe:2:1::12
	traceroute to 2001:cafe:2:1::12 (2001:cafe:2:1::12) from 2001:cafe:8:1::18, 30 hops max, 24 byte packets
	1  2001:cafe:8:1::8  0.105 ms  0.076 ms  0.03 ms
	2  2001:cafe:7:78::7  0.047 ms  0.03 ms  0.028 ms
	3  2001:cafe:4:47::4  0.043 ms  0.031 ms  0.031 ms
	4  2001:cafe:3:34::3  0.044 ms  0.034 ms  0.034 ms
	5  2001:cafe:1:13::1  0.043 ms  0.035 ms  0.036 ms
	6  2001:cafe:1:12::2  0.134 ms  0.092 ms  0.093 ms
	7  2001:cafe:2:1::12  0.082 ms  0.075 ms  0.072 ms

e. What is the path that packets follow from a host attached to ``AS2`` to a host attached to ``AS7`` ?
	
    ..
      mininet> h2 traceroute6 -n 2001:cafe:7:1::17
      traceroute to 2001:cafe:7:1::17 (2001:cafe:7:1::17) from 2001:cafe:2:1::12, 30 hops max, 24 byte packets
      1  2001:cafe:2:1::2  0.131 ms  0.057 ms  0.047 ms
      2  2001:cafe:2:25::5  0.056 ms  0.043 ms  0.04 ms
      3  2001:cafe:6:67::6  0.083 ms  0.131 ms  0.099 ms
      4  2001:cafe:4:47::7  0.099 ms  0.094 ms  0.157 ms
      5  2001:cafe:7:1::17  0.305 ms  0.144 ms  0.133 ms

f. We now disable the interdomain link between ``AS3`` and ``AS4``. What are the hosts that ``AS1``, ``AS5`` and ``AS6`` are still able to ping ?

      ..
         as3> show bgp sum

	 IPv6 Unicast Summary:
	 BGP router identifier 192.168.26.1, local AS number 3 vrf-id 0
	 BGP table version 13
	 RIB entries 5, using 800 bytes of memory
	 Peers 3, using 62 KiB of memory
	 
	 Neighbor          V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
	 2001:cafe:1:13::1 4          1      23      29        0    0    0 00:15:35            2
	 2001:cafe:2:23::2 4          2      21      22        0    0    0 00:15:35            1
	 2001:cafe:3:34::4 4          4      28      27        0    0    0 00:00:18 Idle (Admin)

	 Total number of neighbors 3

	 mininet> ping6all
	 *** Ping: testing reachability over IPv6
	 h1 --IPv6--> X h3 X X X X h2 
	 h2 --IPv6--> h7 h3 h5 h1 X h4 h6 
	 h3 --IPv6--> X X h1 X X X h2 
	 h4 --IPv6--> h7 X h5 X h8 h6 h2 
	 h5 --IPv6--> h7 X X X h4 h6 h2 
	 h6 --IPv6--> h7 X h5 X h8 h4 h2 
	 h7 --IPv6--> X h5 X h8 h4 h6 h2 
	 h8 --IPv6--> h7 X X X h4 h6 X 
	 *** Results: 42% dropped (32/56 received)
      
       
4. Exam topology
   
.. include:: /links.rst	       
