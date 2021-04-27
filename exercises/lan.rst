.. Copyright |copy| 2013,2019 by Justin Vellemans, Florentin Rochet, David Lebrun, Juan Antonio Cordero, Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_

Local Area Networks: The Spanning Tree Protocol and Virtual LANs
=================================================================


.. inginious:: stp-bpdu


.. inginious:: stp-ports-state

.. inginious:: stp-ports-state-qcm

.. inginious:: q-stp-1

Exercises
---------

1. Consider the switched network shown in Fig. 1. What is the spanning tree that will be computed by 802.1d in this network assuming that all links have a unit cost ? Indicate the state of each port.

  .. figure:: /exercises/figures/ex-stp-switches.png
     :align: center
     :scale: 100

     Fig. 1. A small network composed of Ethernet switches

2. Consider the switched network shown in Fig. 1. In this network, assume that the LAN between switches S3 and S12 fails. How should the switches update their port/address tables after the link failure ?


3. Consider the switched network shown in the figure below. Compute the Spanning Tree of this network.

    .. tikz::
       :libs: shapes, positioning, matrix, arrows

       \tikzstyle{arrow} = [thick,->,>=stealth]
       \tikzset{switch/.style = {diamond, draw, text centered, minimum height=2em, node distance= 2cm}, }
       \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \tikzset{ftable/.style={rectangle, dashed, draw} }
       \node[switch] (S3) {S5};
       \node[switch, left of=S3] (S6) {S9};
       \node[switch, right of=S3] (S7) {S10};
       \node[switch, above of=S3] (S4) {S2};
       \node[switch, below of=S3] (S9) {S4};

       \path[draw,thick]
       (S3) edge (S6)
       (S3) edge (S7)
       (S6) edge (S4)
       (S4) edge (S7)
       (S3) edge (S9)
       (S9) edge (S7)
       (S3) edge (S7);

4. Many enterprise networks are organized with a set of backbone devices interconnected by using a full mesh of links as shown in Fig.2. In this network, what are the benefits and drawbacks of using Ethernet switches and IP routers running OSPF ?

  .. figure:: /exercises/figures/ex-stp-backbone.png
     :align: center
     :scale: 100

     Fig. 2. A typical enterprise backbone network

5. In the network depicted in Fig. 3, the host `H0` performs a traceroute toward its peer `H1` (designated by its name) through a network composed of switches and routers. Explain precisely the frames, packets, and segments exchanged since the network was turned on. You may assign addresses if you need to.

  .. figure:: /exercises/figures/ex-stp-switches_vs_routers.png
     :align: center
     :scale: 100

     Fig. 3. Host `H0` performs a traceroute towards its peer `H1` through a network composed of switches and routers

     .. spelling::

	versa


6. In the network represented in Fig. 4, can the host `H0` communicate with `H1` and vice-versa? Explain. Add whatever you need in the network to allow them to communicate.

  .. figure:: /exercises/figures/ex-stp-routing_across_VLANs.png
     :align: center
     :scale: 100

     Fig. 4. Can `H0` and `H1` communicate ?

7. Consider the network depicted in Fig. 5. Both of the hosts `H0` and `H1` have two interfaces: one connected to the switch `S0` and the other one to the switch `S1`. Will the link between `S0` and `S1` ever be used? If so, under which assumptions? Provide a comprehensive answer.

  .. figure:: /exercises/figures/ex-stp-switches_wo_STP.png
     :align: center
     :scale: 100

     Fig. 5. Will the link between `S0` and `S1` ever be used?

8. Most commercial Ethernet switches are able to run the Spanning tree protocol independently on each VLAN. What are the benefits of using per-VLAN spanning trees ?

..
  9. Consider the network shown below and assume that all routers use a link-state routing protocol.
  .. figure:: ../../book/network/svg/ex-five-routers-redundant.png
    :align: center
    :scale: 100

    Simple network with redundant links

    a. Show the messages used by the routers to discover their neighbors and establish adjacencies.

    b. Show the messages that propagate the adjacencies of A during the flooding phase.

    c. For each router compute its routing table once the flooding is over.

    d. Consider that link `B-C` fails and that router `B` is the first to detect the failure. Router `B` will flood its updated link state packet through the entire network and all routers will recompute their forwarding table. Compute the successive updates to the routers RIB, assuming that router `C` receives the updated link-state packet from router B before detecting the failure himself.

    e. What would change if routers had used a distance-vector protocol instead.


Testing the Spanning Tree with IPMininet
----------------------------------------

IPMininet_ can also be used to configure the Spanning Tree protocol on Linux hosts that act as Ethernet switches. Let us consider the simple Ethernet network shown in the figure below.

 .. tikz:: A simple Ethernet network
    :libs: shapes, positioning, matrix, arrows

    \tikzset{switch/.style = {diamond, draw, text centered, minimum height=2em, node distance= 2cm}, }

    \node[switch] (S9) {S9};
    \node[switch, left of=S9] (S6) {S6};
    \node[switch, right of=S9] (S7) {S7};
    \node[switch, above of=S9] (S4) {S4};
    \node[switch, below of=S9] (S3) {S3};

    \path[draw,thick]
    (S3) edge (S6)
    (S3) edge (S7)
    (S6) edge (S4)
    (S4) edge (S7)
    (S3) edge (S9)
    (S9) edge (S7)
    (S3) edge (S7);


This network can be launched with the IPMininet_ script shown below. The entire script is available from :download:`/exercises/ipmininet_scripts/stp.py`.

.. code-block:: python

   import shlex
   from ipmininet.iptopo import IPTopo

   from ipmininet.ipnet import IPNet
   from ipmininet.cli import IPCLI


   class MyTopology(IPTopo):

       def build(self, *args, **kwargs):

           # Switches with manually set STP priority
           s3 = self.addSwitch("s3", prio=3, lo_addresses=["2001:1::4/64"])
           s4 = self.addSwitch("s4", prio=4, lo_addresses=["2001:1::4/64"])
           s6 = self.addSwitch("s6", prio=6, lo_addresses=["2001:1::6/64"])
           s7 = self.addSwitch("s7", prio=7, lo_addresses=["2001:1::7/64"])
           s9 = self.addSwitch("s9", prio=9, lo_addresses=["2001:1::9/64"])

           # Hub
           # hub1 = self.addHub("hub1")

           # Links
           self.addLink(s3, s9, stp_cost=1)  # Cost changed for both interfaces
           l37 = self.addLink(s3, s7)
           l37[s3].addParams(stp_cost=1) # cost changed for s3->s7
           l37[s7].addParams(stp_cost=1) # cost changed for s7->s3
           self.addLink(s9, s7) # default cost of 1
           self.addLink(s6, s9)
           self.addLink(s6, s4)
           self.addLink(s7, s4)

           super(MyTopology, self).build(*args, **kwargs)

       def post_build(self, net):
           for s in self.switches():
               command="/usr/sbin/tcpdump -i any --immediate-mode -c 50 -w ./stp-"+s+"-trace.pcap stp"
               p = net[s].popen(shlex.split(command))

           super(MyTopology, self).post_build(net)


    net = IPNet(topo=MyTopology())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()


The ``addSwitch`` method creates an Ethernet switch. It assigns a random MAC address to each switch and we can configure it with a priority that is used in the high order bits of the switch identifier. We add one IP address to each switch so that we can connect to them on mininet_. In practice, IPMininet_ configures the :manpage:`brtcl(8)` software that implements the Spanning Tree protocol on Linux. We can then create the links, configure their cost if required and launch tcpdump_ to capture the Ethernet frames that contain the messages of the Spanning Tree protocol.

The network contains five nodes and six links.

.. code-block:: python

   mininet> nodes
   available nodes are:
   s3 s4 s6 s7 s9
   mininet> links
   s3-eth2<->s7-eth1 (OK OK)
   s3-eth1<->s9-eth1 (OK OK)
   s6-eth2<->s4-eth1 (OK OK)
   s6-eth1<->s9-eth3 (OK OK)
   s7-eth3<->s4-eth2 (OK OK)
   s9-eth2<->s7-eth2 (OK OK)


By using :manpage:`brtcl(8)`, we can easily observe the state of the Spanning Tree protocol on the different switches. Let us start with ``s3``, i.e. the root of the Spanning Tree.

.. code-block:: console


   mininet> s3 brctl showstp s3
   s3
     bridge id		0003.f63545ab5f79
     designated root	0003.f63545ab5f79
     root port		   0			path cost		   0
     max age		  20.00			bridge max age		  20.00
     hello time		   2.00			bridge hello time	   2.00
     forward delay		  15.00			bridge forward delay	  15.00
     ageing time		 300.00
     hello timer		   1.03			tcn timer		   0.00
     topology change timer	   0.00			gc timer		  77.90
     flags


   s3-eth1 (1)
     port id		8001			state		     forwarding
     designated root	0003.f63545ab5f79	path cost		   1
     designated bridge	0003.f63545ab5f79	message age timer	   0.00
     designated port	8001			forward delay timer	   0.00
     designated cost	   0			hold timer		   0.02
     flags

   s3-eth2 (2)
     port id		8002			state		     forwarding
     designated root	0003.f63545ab5f79	path cost		   1
     designated bridge	0003.f63545ab5f79	message age timer	   0.00
     designated port	8002			forward delay timer	   0.00
     designated cost	   0			hold timer		   0.02
     flags

The first part of the output of the :manpage:`brctl(8)` command shows the state of the Spanning Tree software on the switch. The identifier of this switch is ``0003.f63545ab5f79`` and the root switch is itself. There is no root port on this switch since it is the root. The path cost is the cost of the path to reach the root switch, i.e. 0 on the root. Then the switch reports the different timers.

The second part of the output provides the state of each switch port. Port ``s3-eth1`` is active and forwards data frames (state is set to `forwarding`). This port is a `designated` port. The cost of ``1`` is the cost associated to this interface. The same information is found for port ``s3-eth2``.

The state of switch ``s9`` is different. The output of :manpage:`brctl(8)` indicates that the root identifier is ``0003.f63545ab5f79`` which is at a distance of ``1`` from switch ``s9``. The root port on ``s9`` is port `1`, i.e. ``s9-eth1``. Two of the ports of this switch forward data packets, the root port and the ``s9-eth3`` which is a designated port. The ``s9-eth2`` port is a blocked port.

.. code-block:: console

   mininet> s9 brctl showstp s9
   s9
     bridge id		0009.7ecc45e18e5b
     designated root	0003.f63545ab5f79
     root port		   1			path cost		   1
     max age		  20.00			bridge max age		  20.00
     hello time		   2.00			bridge hello time	   2.00
     forward delay		  15.00			bridge forward delay	  15.00
     ageing time		 300.00
     hello timer		   0.00			tcn timer		   0.00
     topology change timer	   0.00			gc timer		 167.22
     flags


   s9-eth1 (1)
     port id		8001			state		     forwarding
     designated root	0003.f63545ab5f79	path cost		   1
     designated bridge	0003.f63545ab5f79	message age timer	  20.00
     designated port	8001			forward delay timer	   0.00
     designated cost	   0			hold timer		   0.00
     flags

   s9-eth2 (2)
     port id		8002			state		       blocking
     designated root	0003.f63545ab5f79	path cost		   1
     designated bridge	0007.2a6f5ef34984	message age timer	  19.98
     designated port	8002			forward delay timer	   0.00
     designated cost	   1			hold timer		   0.00
     flags

   s9-eth3 (3)
     port id		8003			state		     forwarding
     designated root	0003.f63545ab5f79	path cost		   1
     designated bridge	0009.7ecc45e18e5b	message age timer	   0.00
     designated port	8003			forward delay timer	   0.00
     designated cost	   1			hold timer		   0.97
     flags


:manpage:`brctl(8)` also maintains a MAC address table that contains the Ethernet addresses that have been learned on each switch port.

.. code-block:: console

   mininet> s9 brctl showmacs s9
   port no	mac addr		is local?	ageing timer
   1	2a:6f:5e:f3:49:84	no		 257.92
   1	62:60:d3:46:2f:12	no		 257.92
   3	7e:cc:45:e1:8e:5b	yes		   0.00
   3	7e:cc:45:e1:8e:5b	yes		   0.00
   2	a2:07:cb:02:90:4a	yes		   0.00
   2	a2:07:cb:02:90:4a	yes		   0.00
   1	d6:a1:b4:c8:de:72	yes		   0.00
   1	d6:a1:b4:c8:de:72	yes		   0.00
   1	f6:35:45:ab:5f:79	no		   0.45


Thanks to the traces collected by tcpdump_, we can easily analyze the messages exchanged by the switches. Here is the fist message sent by switch ``s3``.

.. figure:: /exercises/figures/stp-packet1.png




.. include:: /links.rst
