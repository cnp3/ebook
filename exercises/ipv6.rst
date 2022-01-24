.. Copyright |copy| 2014, 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


IPv6 Networks
=============

Basic questions on IPv6 Networks
--------------------------------

Before starting to determine the paths that packets will follow in an IPv6 network, it is important to remember how to convert IPv6 addresses in binary numbers.

.. inginious:: q-ipv6-binary

An IPv6 forwarding table contains a list of IPv6 prefixes with their associated nexthop or outgoing interface. When an IPv6 router receives a packet, it forwards it according to its forwarding table. Note that IPv6 routers forward packets along the *longest match* between the destination address of the packet and the routes in the forwarding table.

.. inginious:: q-ipv6-forwarding


Now that you master the basics, you can determine the paths followed by IPv6 packets in simple networks.


.. inginious:: q-ipv6-static-1

.. inginious:: q-ipv6-static-2

.. inginious:: q-ipv6-static-3


Design questions
----------------

1. Consider the network shown in the figure below. In this network, the following addresses are used.

  - host ``A`` : ``2001:db8:1341:1::A`` and its default route points to ``2001:db8:1341:1::1``
  - host ``B`` : ``2001:db8:1341:4::B`` and its default route points to ``2001:db8:1341:4::4``

The routers have one address inside each network :

 - router ``R1`` uses address ``2001:db8:1341:1::1`` on its West interface, address ``2001:db8:1341:12::1`` on its East interface and address ``2001:db8:1341:13::1`` on its South interface
 - router ``R2`` uses address ``2001:db8:1341:12::2`` on its West interface, address ``2001:db8:1341:23::2`` on its South-West interface and address ``2001:db8:1341:24::2`` on its South interface.
 - router ``R3`` uses address ``2001:db8:1341:34::3`` on its East interface, address ``2001:db8:1341:23::3`` on its North-East interface and address ``2001:db8:1341:13::3`` on its North interface
 - router ``R4`` uses address ``2001:db8:1341:34::4`` on its West interface, address ``2001:db8:1341:24::4`` on its North interface and address ``2001:db8:1341:4::4`` on its East interface

The forwarding paths used in a network depend on the forwarding tables installed in the network nodes. Sometimes, these forwarding tables must be configured manually.

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[ftable, above=of R1] (FR1) { \begin{tabular}{l|l}
        Dest. & Nexthop \\
        \hline
        2001:db8:1341:4/64  & 2001:db8:1341:12::2 \\
        2001:db8:1341:23/64 & 2001:db8:1341:13::3 \\
        2001:db8:1341:34/64 & 2001:db8:1341:13::3 \\
        2001:db8:1341:24/64 & 2001:db8:1341:12::2 \\
        \end{tabular}};
        \node[router,right=of R1] (R2) {R2};

        \node[router,below=of R1] (R3) {R3};

        \node[router,below=of R2] (R4) {R4};
        \node[ftable,below=of R4] (FR4) { \begin{tabular}{l|l}
        Dest. & Nexthop \\
        \hline
        2001:db8:1341:1/64  & 2001:db8:1341:34::3 \\
        2001:db8:1341:23/64 & 2001:db8:1341:24::2 \\
        2001:db8:1341:13/64 & 2001:db8:1341:34::3 \\
        2001:db8:1341:12/64 & 2001:db8:1341:24::2 \\
        \end{tabular}};
        \node[host, right=of R4] (B) {B};

        \path[draw,thick]
        (A) edge (R1)
        (R1) edge (R2)
        (R2) edge (R3)
        (R1) edge (R3)
        (R4) edge (R3)
        (R2) edge (R4)
        (R4) edge (B);

        \draw[arrow, dashed] (FR1) -- (R1);
        \draw[arrow, dashed] (FR4) -- (R4);

In this network, propose the forwarding tables of ``R2`` and ``R3`` that ensure that hosts ``A`` and ``B`` can exchange packets in both directions.


2. Consider the same network as in the previous question, but now the forwarding tables of ``R2`` and ``R3`` are configured as shown below :

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[router,right=of R1] (R2) {R2};
        \node[ftable, above=of R2] (FR2) { \begin{tabular}{l|l}
        Dest. & Nexthop \\
        \hline
        2001:db8:1341:1/64  & 2001:db8:1341:12::1 \\
        2001:db8:1341:4/64  & 2001:db8:1341:23::3 \\
        2001:db8:1341:13/64 & 2001:db8:1341:23::3 \\
        2001:db8:1341:34/64 & 2001:db8:1341:23::3 \\
        \end{tabular}};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[ftable,below=of R3] (FR3) { \begin{tabular}{l|l}
        Dest. & Nexthop \\
        \hline
        2001:db8:1341:1/64  & 2001:db8:1341:23::2 \\
        2001:db8:1341:4/64  & 2001:db8:1341:34::4 \\
        2001:db8:1341:12/64 & 2001:db8:1341:23::2 \\
        2001:db8:1341:24/64 & 2001:db8:1341:23::2 \\
        \end{tabular}};
        \node[host, right=of R4] (B) {B};

        \path[draw,thick]
        (A) edge (R1)
        (R1) edge (R2)
        (R2) edge (R3)
        (R1) edge (R3)
        (R4) edge (R3)
        (R2) edge (R4)
        (R4) edge (B);

        \draw[arrow, dashed] (FR2) -- (R2);
        \draw[arrow, dashed] (FR3) -- (R3);


   In this network, select `all` the rules in the shown forwarding tables that ensure that the packets sent from ``A`` to ``B`` follow the reverse path of the packets sent by ``B`` to ``A``.


3. Consider the network shown in the figure below. In this network, the following addresses are used.

  - host ``A`` : ``2001:db8:1341:1::A`` and its default route points to ``2001:db8:1341:1::1``
  - host ``B`` : ``2001:db8:1341:4::B`` and its default route points to ``2001:db8:1341:4::4``

The routers have one address inside each network :

 - router ``R1`` uses address ``2001:db8:1341:1::1`` on its West interface, address ``2001:db8:1341:12::1`` on its East interface and address ``2001:db8:1341:13::1`` on its South interface
 - router ``R2`` uses address ``2001:db8:1341:12::2`` on its West interface, and address ``2001:db8:1341:24::2`` on its South interface
 - router ``R3`` uses address ``2001:db8:1341:34::3`` on its East interface and address ``2001:db8:1341:13::3`` on its North interface
 - router ``R4`` uses address ``2001:db8:1341:34::4`` on its West interface, address ``2001:db8:1341:24::4`` on its North interface and address ``2001:db8:1341:4::4`` on its East interface

Routers ``R2`` and ``R3`` are buggy in this network. Besides the routes for their local interfaces (not shown in the figure), they only have a default route which is shown in the figure below.

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[ftable, above=of R1] (FR2) { \begin{tabular}{l|l}
        Dest. & Nexthop \\
        \hline
        ::/0  & 2001:db8:1341:12::1 \\
        \end{tabular}};
        \node[router,right=of R1] (R2) {R2};

        \node[router,below=of R1] (R3) {R3};

        \node[router,below=of R2] (R4) {R4};
        \node[ftable,below=of R4] (FR3) { \begin{tabular}{l|l}
        Dest. & Nexthop \\
        \hline
        ::/0  & 2001:db8:1341:34::4 \\
        \end{tabular}};
        \node[host, right=of R4] (B) {B};

        \path[draw,thick]
        (A) edge (R1)
        (R1) edge (R2)
        (R1) edge (R3)
        (R4) edge (R3)
        (R2) edge (R4)
        (R4) edge (B);

        \draw[arrow, dashed] (FR2) -- (R2);
        \draw[arrow, dashed] (FR3) -- (R3);

How do you configure the forwarding tables on ``R1`` and ``R4`` so that ``A`` can reach ``B`` and the reverse ?

4. Consider a slightly different network than in the previous question.

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[router,right=of R1] (R2) {R2};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[host, right=of R4] (B) {B};

        \path[draw,thick]
        (A) edge (R1)
        (R1) edge (R2)
        (R1) edge (R3)
        (R1) edge (R4)
        (R4) edge (R3)
        (R2) edge (R4)
        (R4) edge (B);

 Assuming that the following IPv6 addresses are used :

  - host ``A`` : ``2001:db8:1341:1::A`` and its default route points to ``2001:db8:1341:1::1``
  - host ``B`` : ``2001:db8:1341:4::B`` and its default route points to ``2001:db8:1341:4::4``

The routers have one address inside each network :

 - router ``R1`` uses address ``2001:db8:1341:1::1`` on its West interface, address ``2001:db8:1341:12::1`` on its East interface, address ``2001:db8:1341:14::1`` on its South-East interface and address ``2001:db8:1341:13::1`` on its South interface
 - router ``R2`` uses address ``2001:db8:1341:12::2`` on its West interface, and address ``2001:db8:1341:24::2`` on its South interface
 - router ``R3`` uses address ``2001:db8:1341:34::3`` on its East interface and address ``2001:db8:1341:13::3`` on its North interface
 - router ``R4`` uses address ``2001:db8:1341:34::4`` on its West interface, address ``2001:db8:1341:24::4`` on its North interface, address ``2001:db8:1341:14::4`` on its North-West interface and address ``2001:db8:1341:4::4`` on its East interface

 Can you configure the forwarding tables so that the following paths are used by packets sent by host ``A`` to reach one of the four addresses of router ``R4``?

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[router,right=of R1] (R2) {R2};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[host, right=of R4] (B) {B};

        \path[draw,arrow, color=red, thick]
        (A) edge (R1)
        (R1) edge (R2)
        (R2) edge (R4);

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[router,right=of R1] (R2) {R2};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[host, right=of R4] (B) {B};

        \path[draw,arrow, color=blue, thick]
        (A) edge (R1)
        (R1) edge (R4);

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A) {A};
        \node[router, right=of A] (R1) { R1 };
        \node[router,right=of R1] (R2) {R2};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[host, right=of R4] (B) {B};

        \path[draw,arrow, color=green, thick]
        (A) edge (R1)
        (R1) edge (R3)
        (R3) edge (R4);

 Do your forwarding tables impose the path used to reach host ``B`` which is attached to router ``R4`` or do you need to configure an additional entry in these tables ?

5. Consider the network below that contains only routers. This network has been configured by a group of students and you must verify whether the configuration is correct. All the IPv6 addresses are part of the same ``/48`` prefix that we name ``p``. The following subnets are defined in this ``/48`` prefix.

 - ``p:12/64`` for the link between ``R1`` and ``R2``. On this subnet, ``R1`` uses address ``p:12::1`` while router ``R2`` uses address ``p:12::2``
 - ``p:13/64`` for the link between ``R1`` and ``R3``. On this subnet, ``R1`` uses address ``p:13::1`` while router ``R3`` uses address ``p:13::3``
 - ``p:24/64`` for the link between ``R2`` and ``R4``. On this subnet, ``R2`` uses address ``p:24::2`` while router ``R4`` uses address ``p:24::4``
 - ...

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[router] (R1) {R1};
        \node[router,right=of R1] (R2) {R2};
        \node[router,right=of R2] (R5) {R5};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[router,below=of R5] (R6) {R6};

        \path[draw,thick]
        (R1) edge (R2)
        (R1) edge (R3)
        (R4) edge (R3)
        (R2) edge (R4)
        (R2) edge (R5)
        (R4) edge (R6)
        (R5) edge (R6);

.. note 12 via R2
.. note 13 via R3 mais boucle R2 R4 R5 R6
.. note 34 via R4 mais blackhole en R2 et R5 pas de route
.. note 24 via R2 ou R4 pas de probleme
.. note 25 via le plus proche sauf boucle R4-R6
.. note 46 pas de route sauf defaut
.. note 56 tout vers R4 mais pas de route en R4

The students have configured the following forwarding tables on these six routers.

 - on router ``R1``

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[ftable] (FR1) { \begin{tabular}{l|l}
        Dest. & Nexthop/Interface \\
        \hline
        ::/0  & p:12::2 \\
        p:12::/64  & East \\
        p:13::/64  & South\\
        p:25::/64  & p:12::2\\
        p:34::/64 & p:12::2\\
        \end{tabular}};



 - on router ``R2``

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[ftable] (FR2) { \begin{tabular}{l|l}
        Dest. & Nexthop/Interface \\
        \hline
        ::/0  & p:12::1 \\
        p:12::/64  & West \\
        p:13::/64 & p:24::4\\
        p:24::/64  & South\\
        p:25::/64  & East\\
        p:56::/64 & p:24::4\\
        \end{tabular}};


 - on router ``R3``

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[ftable] (FR3) { \begin{tabular}{l|l}
        Dest. & Nexthop/Interface \\
        \hline
        ::/0 & p:13::1\\
        p:13::/64  & North \\
        p:34::/64  & East\\
        p:56::/64 & p:34::4\\
        \end{tabular}};


 - on router ``R5``

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[ftable] (FR5) { \begin{tabular}{l|l}
        Dest. & Nexthop/Interface \\
        \hline
        ::/0 & p:56::6 \\
        p:12::/64 & p:25::2\\
        p:25::/64  & West \\
        p:56::/64  & South\\
        \end{tabular}};

 - on router ``R4``

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzset{ftable/.style={rectangle, dashed, draw} }

        \node[ftable] (FR4) { \begin{tabular}{l|l}
        Dest. & Nexthop/Interface \\
        \hline
        p:12::/63 & p:24::2\\
        p:24::/64  & North\\
        p:25::/64  & p:46::6\\
        p:34::/64  & West\\
        p:46::/64  & East\\
        \end{tabular}};

 - on router ``R6``

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[ftable] (FR6) { \begin{tabular}{l|l}
        Dest. & Nexthop/Interface \\
        \hline
        ::/0 & p:56::5 \\
        p:13::/64 & p:46::4\\
        p:24::/63 & p:46::4\\
        p:34::/64 & p:46::4\\
        p:46::/64  & West\\
        p:56::/64  & North\\
        \end{tabular}};

What do you think about the proposed configuration?


6. Sometimes, static routes must be configured on networks to enforce certain paths. Consider the six routers network shown in the figure below.

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A1) {A1};
        \node[router, right=of A1] (R1) {R1};
        \node[host, below=of A1] (A2) {A2};
        \node[router,right=of R1] (R2) {R2};
        \node[router,right=of R2] (R5) {R5};
        \node[router,below=of R1] (R3) {R3};
        \node[router,below=of R2] (R4) {R4};
        \node[router,below=of R5] (R6) {R6};
        \node[host, right=of R5] (B1) {B1};
        \node[host, right=of R6] (B2) {B2};


        \path[draw,thick]
        (A1) edge (R1)
        (A2) edge (R3)
        (R1) edge (R2)
        (R1) edge (R3)
        (R4) edge (R3)
        (R2) edge (R4)
        (R2) edge (R5)
        (R4) edge (R6)
        (R5) edge (R6)
        (R5) edge (B1)
        (R6) edge (B2);


   In this network, we will focus on four IPv6 prefixes :

     - ``p:0000::/64`` used on the link ``A1-R1``. ``A1`` uses address ``p:0000::A1/64``
     - ``p:0001::/64`` used on the link ``A2-R3``. ``A2`` uses address ``p:0001::A2/64``
     - ``p:0002::/64`` used on the link ``B1-R5``. ``B1`` uses address ``p:0002::B1/64``
     - ``p:0003::/64`` used on the link ``B2-R6``. ``B2`` uses address ``p:0003::B2/64``

   Can you configure the forwarding tables of the six routers to achieve the following network objectives :

    a. All packets sent by ``B1`` and ``B2`` to ``A1`` and ``A2`` are always forwarded via ``R2`` while all packets from ``A1`` and ``A2`` are always forwarded via ``R4``
    b. The packets whose destinations are ``A1``,  ``A2``, ``B1`` or ``B2`` are never forwarded via router ``R4``
    c. The packets sent by ``A1`` or ``A2`` towards ``B1`` are always forwarded via ``R2`` while the packets towards ``B2`` are always forwarded via ``R4``.

   When creating these forwarding tables, try to minimize the number of entries that you install on each router.

7. When a network is designed, an important element of the design is the IP address allocation plan. A good allocation plan can provide flexibility and help to reduce the size of the forwarding tables.

     .. tikz::
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
        \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
        \tikzset{ftable/.style={rectangle, dashed, draw} }
        \node[host] (A1) {A1};
        \node[router, right=of A1] (R1) {R1};
        \node[host, below=of A1] (A2) {A2};
        \node[router,right=of R1] (R2) {R2};
        \node[router,right=of R2] (R5) {R5};
        \node[router,below=of R1] (R3) {R3};
         \node[router,below=of R5] (R6) {R6};
        \node[host, right=of R5] (B1) {B1};
        \node[host, right=of R6] (B2) {B2};


        \path[draw,thick]
        (A1) edge (R1)
        (A2) edge (R3)
        (R1) edge (R3)
        (R2) edge (R3)
        (R2) edge (R5)
        (R2) edge (R6)
        (R5) edge (R6)
        (R5) edge (B1)
        (R6) edge (B2);

  Assign IP subnets to all links in this network so that you can reduce the number of entries in the forwarding tables of all routers. Assume that you have received a ``/56`` prefix that you can use as you want. Each subnet containing a host must be allocated a ``/64`` subnet.

.. spelling::

   namespace
   namespaces



Configuring IPv6 Networks
-------------------------

With the previous exercises, you have learned how to reason about IPv6 networks "on paper". Given the availability of IPv6 implementations, it is also possible to carry out experiments in real and virtual labs. Several virtual environments are possible. In this section, we focus on mininet_. mininet_ is an emulation framework developed at Stanford University that leverages the namespaces features of recent Linux kernels. With those namespaces, a single Linux kernel can support a variety of routers and hosts interconnected by virtual links. mininet_ has been used by several universities as an educational tool, but unfortunately it was designed without IPv6 support.

During the last years, `Olivier Tilmans <https://inl.info.ucl.ac.be/otilmans.html>`_ and `Mathieu Jadin <https://inl.info.ucl.ac.be/mjadin.html>`_ have developed the missing piece to enable students to use mininet_ to experiment with IPv6: ipmininet_.  ipmininet_ is a python module that provides the classes that are required to automatically configure IPv6 networks with different routing protocols. It is available from PyPi from https://pypi.org/project/ipmininet/

The syntax of IPMininet_ is relatively simple and can be learned by looking at a few examples.

Let us start our exploration of IPv6 routing with a simple network topology that contains two hosts and three routers and uses static routes.

.. tikz:: A simple network
   :libs: positioning,matrix,arrows

   \tikzstyle{arrow} = [thick,->,>=stealth]
   \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
   \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
   \tikzset{ftable/.style={rectangle, dashed, draw} }
   \node[host] (A) {A};
   \node[router, right=of A] (R1) { R1 };
   \node[ftable, above=of R1] (FR1) { \begin{tabular}{l|l}
   Dest. & Nexthop \\
   \hline
   2001:db8:1341:3/64 & 2001:db8:1341:12::2 \\
   2001:db8:1341:23/64 & 2001:db8:1341:13::3 \\
   \end{tabular}};
   \node[router,right=of R1] (R2) {R2};
   \node[ftable, right=of R2] (FR2) { \begin{tabular}{l|l}
   Dest. & Nexthop \\
   \hline
   2001:db8:1341:3/64 & 2001:db8:1341:23::3 \\
   2001:db8:1341:1/64 & 2001:db8:1341:12::1 \\
   2001:db8:1341:13/64 & 2001:db8:1341:23::3 \\
   \end{tabular}};
   \node[router,below=of R1] (R3) {R3};
   \node[ftable, below=of R3] (FR3) { \begin{tabular}{l|l}
   Dest. & Nexthop \\
   \hline
   2001:db8:1341:1/64 & 2001:db8:1341:13::1 \\
   2001:db8:1341:12/64 & 2001:db8:1341:23::2 \\
   \end{tabular}};
   \node[host, right=of R3] (B) {B};

   \path[draw,thick]
   (A) edge (R1)
   (R1) edge (R2)
   (R2) edge (R3)
   (R1) edge (R3)
   (R3) edge (B);

   \draw[arrow, dashed] (FR1) -- (R1);
   \draw[arrow, dashed] (FR2) -- (R2);
   \draw[arrow, dashed] (FR3) -- (R3);

IPMininet_ simplifies the creation of the network topology by providing a simple API. For this, you simply need to declare a class that extends the ``IPTopo`` class.

.. code-block:: python

   from ipmininet.iptopo import IPTopo
   from ipmininet.router.config import RouterConfig, STATIC, StaticRoute
   from ipmininet.ipnet import IPNet
   from ipmininet.cli import IPCLI

   class MyTopology(IPTopo):
       pass

Then, you need to extend the build method that creates routers and hosts.

.. code-block:: python


   def build(self, *args, **kwargs):

      # The routers using static routes
      r1 = self.addRouter("r1", config=RouterConfig)
      r2 = self.addRouter("r2", config=RouterConfig)
      r3 = self.addRouter("r3", config=RouterConfig)
      # The hosts
      a = self.addHost("a")
      b = self.addHost("b")

Although IPMininet_ can assign prefixes and addresses automatically, we use manually assigned addresses in this example.

We use five /64 IPv6 prefixes in this network topology:

 - ``2001:db8:1341:1::/64`` on the link between ``a`` and ``r1``
 - ``2001:db8:1341:12::/64`` on the link between ``r1`` and ``r2``
 - ``2001:db8:1341:13::/64`` on the link between ``r1`` and ``r3``
 - ``2001:db8:1341:23::/64`` on the link between ``r2`` and ``r3``
 - ``2001:db8:1341:1::/64`` on the link between ``b`` and ``r3``

We can then manually configure the IPv6 addresses of each host/router on each link. Let us start with the links attached to the two hosts.

.. code-block:: python

   # link between r1 and a
   lr1a = self.addLink(r1, a)
   lr1a[r1].addParams(ip=("2001:db8:1341:1::1/64"))
   lr1a[a].addParams(ip=("2001:db8:1341:1::A/64"))
   # link between r3 and b
   lr3b = self.addLink(r3, b)
   lr3b[r3].addParams(ip=("2001:db8:1341:3::3/64"))
   lr3b[b].addParams(ip=("2001:db8:1341:3::B/64"))


The same can be done for the three links between the different routers.

.. code-block:: python

   lr1r2 = self.addLink(r1, r2)
   lr1r2[r1].addParams(ip=("2001:db8:1341:12::1/64"))
   lr1r2[r2].addParams(ip=("2001:db8:1341:12::2/64"))

   lr1r3 = self.addLink(r1, r3)
   lr1r3[r1].addParams(ip=("2001:db8:1341:13::1/64"))
   lr1r3[r3].addParams(ip=("2001:db8:1341:13::3/64"))

   lr2r3 = self.addLink(r2, r3)
   lr2r3[r2].addParams(ip=("2001:db8:1341:23::2/64"))
   lr2r3[r3].addParams(ip=("2001:db8:1341:23::3/64"))


With these IP prefixes and the network topology, we can now use IPMininet_ to create the topology and assign the addresses.

.. spelling::

   addDaemon
   StaticRoute
   mininet

We start by creating the objects that correspond to the static routes on the three routers. The second argument of the ``addDaemon`` method is a list of ``StaticRoute`` objects. Each of these objects is created by specifying an IP prefix and a nexthop.

.. code-block:: python

   # Add static routes
   r1.addDaemon(STATIC,
		static_routes=[StaticRoute("2001:db8:1341:3::/64","2001:db8:1341:12::2"),
                               StaticRoute("2001:db8:1341:23::/64","2001:db8:1341:13::3")])

   r2.addDaemon(STATIC,
		static_routes=[StaticRoute("2001:db8:1341:3::/64", "2001:db8:1341:23::3"),
                               StaticRoute("2001:db8:1341:1::/64", "2001:db8:1341:12::1"),
                               StaticRoute("2001:db8:1341:13::/64", "2001:db8:1341:23::3")])

   r3.addDaemon(STATIC,
		static_routes=[StaticRoute("2001:db8:1341:1::/64", "2001:db8:1341:13::1"),
                               StaticRoute("2001:db8:1341:12::/64","2001:db8:1341:23::2")])


We can now create the hosts and the routers

.. code-block:: python

   super(MyTopology, self).build(*args, **kwargs)


With this ``build`` method, we can now launch the network by using the python code below.

.. code-block:: python

   net = IPNet(topo=MyTopology(), allocate_IPs=False)  # Disable IP auto-allocation
   try:
      net.start()
      IPCLI(net)
   finally:
      net.stop()


The entire script is available from :download:`/exercises/ipmininet_scripts/static-1.py`.

To help students to start using IPMininet, `Mathieu Jadin <https://inl.info.ucl.ac.be/mjadin.html>`_ has created a Vagrant box that launches a Ubuntu virtual machine with all the required software. See https://ipmininet.readthedocs.io/en/latest/install.html for additional information.

Here is a simple example of the utilization of this Vagrant box.

We start the network topology shown above with the ``sudo python script.py`` command. It launches the mininet_ interactive shell that provides several useful commands:

.. code-block:: console

   mininet> help

   Documented commands (type help <topic>):
   ========================================
   EOF    gterm  iperf     links   pingall       ports  route   time
   dpctl  help   iperfudp  net     pingallfull   px     sh      x
   dump   intfs  ips       nodes   pingpair      py     source  xterm
   exit   ip     link      noecho  pingpairfull  quit   switch

   You may also send a command to a node using:
      <node> command {args}
   For example:
      mininet> h1 ifconfig

   The interpreter automatically substitutes IP addresses
   for node names when a node is the first arg, so commands
   like
       mininet> h2 ping h3
   should work.

   Some character-oriented interactive commands require
   noecho:
      mininet> noecho h2 vi foo.py
   However, starting up an xterm/gterm is generally better:
      mininet> xterm h2

   mininet>

Some of the standard mininet commands assume the utilization of IPv4 and do not have a direct IPv6 equivalent. Here are some useful commands.

The ``nodes`` command lists the routers and hosts that have been created in the mininet topology.

.. code-block:: console

   mininet> nodes
   available nodes are:
   a b r1 r2 r3


The ``links`` command lists the links that have been instantiated and shows that mapping between the named interfaces on each node.

.. code-block:: console

   mininet> links
   r1-eth2<->a-eth0 (OK OK)
   r1-eth0<->r2-eth0 (OK OK)
   r1-eth1<->r3-eth0 (OK OK)
   r2-eth1<->r3-eth1 (OK OK)
   r3-eth2<->b-eth0 (OK OK)
   mininet>

.. spelling::

   inet
   inet6

It is possible to execute any of the standard Linux commands to configure the network stack on any of the hosts by prefixing the command with the corresponding host. Remember to always specify ``inet6`` as the address family to retrieve the IPv6 information.

.. code-block:: console

   mininet> a ip -f inet6 link
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
   2: a-eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen
    link/ether c6:4e:26:d9:de:6d brd ff:ff:ff:ff:ff:ff link-netnsid 0

Host ``a`` has two interfaces: the standard loopback interface and a network interface named ``a-eth0`` that is attached to router ``r1``. We can also verify how the IPv6 addresses have been configured:

.. code-block:: console

   mininet> a ip -f inet6 address
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN qlen 1
      inet6 ::1/128 scope host
        valid_lft forever preferred_lft forever
   2: a-eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP qlen 1000
      inet6 2001:db8:1341:1::a/64 scope global
        valid_lft forever preferred_lft forever
      inet6 fe80::c44e:26ff:fed9:de6d/64 scope link
        valid_lft forever preferred_lft forever

On its ``a-eth0`` interface, host ``a`` uses IPv6 address ``2001:db8:1341:1::a/64``. The link local address (``fe80::c44e:26ff:fed9:de6d/64``) will be described in another chapter. Finally, we can check the forwarding table of host ``a``.

.. code-block:: console

   mininet> a ip -f inet6 route
   2001:db8:1341:1::/64 dev a-eth0  proto kernel  metric 256  pref medium
   fe80::/64 dev a-eth0  proto kernel  metric 256  pref medium
   default via 2001:db8:1341:1::1 dev a-eth0  metric 1024  pref medium


There are three routes in this table. The first two correspond to the two prefixes that are used over the ``a-eth0`` interface. These routes are automatically created when an IPv6 address is configured on an interface. The last route is the default route (``::/0``) which points towards ``2001:db8:1341:1::1``, i.e. router ``r1``.

Another useful command is ``xterm`` 'node' that allows to launch a terminal on the specified node. This gives you a interactive shell on any node. You can use it to capture packets with tcpdump_. As an example, let us use :manpage:`traceroute6(8)` to trace the path followed by packets from host ``a`` towards the IPv6 address of host ``b`` i.e. ``2001:db8:1341:3::b``. The output of this command shows that the path passes through routers ``r1``, ``r2`` and ``r3``.

.. code-block:: console

   mininet> a traceroute6 -q 1 2001:7ab:3::c
   traceroute to 2001:7ab:3::c (2001:7ab:3::c) from 2001:7ab:1::a, 30 hops max, 16 byte packets
   1  2001:7ab:1::1 (2001:7ab:1::1)  0.105 ms
   2  2001:89ab:12::2 (2001:89ab:12::2)  1.131 ms
   3  2001:89ab:23::2 (2001:89ab:23::2)  0.845 ms
   4  2001:7ab:3::c (2001:7ab:3::c)  0.254 ms


Another interesting mininet_ command is ``pingall`` it allows to check that any host can reach any other host inside the network. It executes a ping from any host to any other host inside the network topology.

.. code-block:: console

   mininet> pingall
   *** Ping: testing reachability over IPv4 and IPv6
   a --IPv6--> b
   b --IPv6--> a
   *** Results: 0% dropped (2/2 received)


When debugging a network, it can be interesting to capture packets using tcpdump_ on specific links to check that they follow the expect. If you use tcpdump_ without any filter, you will capture the packets generated by xterm. To capture packets, you need to specify precise filters that will match the packets of interest. For traceroute6, you need to match the IPv6 packets that contain UDP segments and some ICMPv6 packets. The script below provides a simple filter that you can reuse. It takes one argument: the name of the interface on which tcpdump_ needs to run.

.. code-block:: bash

   #!/bin/bash

   tcpdump -v -i $1 -n '(ip6 && udp) || (icmp6  && (ip6[40] == 1 || ip6[40]==3))'

Starting from the :download:`/exercises/ipmininet_scripts/static-1.py` IPMininet_ script, we can explore classical problems when networks are configured with static routes. A first problem is when a router has an incomplete forwarding table. We configure the static routes as shown below. The entire script is available from :download:`/exercises/ipmininet_scripts/static-1-hole.py`.

.. code-block:: console

   # Add static routes
   r1.addDaemon(STATIC, static_routes=[StaticRoute("2001:db8:1341:3::/64",
 "2001:db8:1341:12::2")])

   r2.addDaemon(STATIC, static_routes=[StaticRoute("2001:db8:1341:1::/64",
 "2001:db8:1341:12::1")])

   r3.addDaemon(STATIC, static_routes=[StaticRoute("2001:db8:1341:1::/64",
 "2001:db8:1341:13::1")])

We first check with ``pingall`` whether the network works correctly.

.. code-block:: console

   mininet> pingall
   *** Ping: testing reachability over IPv4 and IPv6
   a --IPv6--> X
   b --IPv6--> X
   *** Results: 100% dropped (0/2 received)

The problem can be detected by using :manpage:`traceroute6(8)`.

.. code-block:: console


   mininet> a traceroute6 -q 1 -n 2001:db8:1341:3::b
   traceroute to 2001:db8:1341:3::b (2001:db8:1341:3::b) from 2001:db8:1341:1::a, 30 hops max, 24 byte packets
   1  2001:db8:1341:1::1  0.074 ms
   2  2001:db8:1341:12::2  0.042 ms !N

In the output of :manpage:`traceroute6(8)`, a ``!N`` indicates that host ``a`` received from ``2001:db8:1341:12::2``, i.e. router ``r2``, a Network unreachable ICMPv6 message. The forwarding table of ``r2`` confirms the root cause of this problem.

.. code-block:: console

   mininet> r2 ip -f inet6 route show
   2001:db8:1341:1::/64 via 2001:db8:1341:12::1 dev r2-eth0  proto 196  metric 20  pref medium
   2001:db8:1341:12::/64 dev r2-eth0  proto kernel  metric 256  pref medium
   2001:db8:1341:23::/64 dev r2-eth1  proto kernel  metric 256  pref medium
   fe80::/64 dev r2-eth0  proto kernel  metric 256  pref medium
   fe80::/64 dev r2-eth1  proto kernel  metric 256  pref medium


A second problem is when there is a forwarding loop inside the network, i.e. packets sent to a specific destination loop through several routers. With the static routes shown below, router ``r2`` forwards the packets towards ``2001:db8:1341:3::b`` via router ``r1``. The entire script is available from :download:`/exercises/ipmininet_scripts/static-1-loop.py`.

.. code-block:: console

   # Add static routes
   r1.addDaemon(STATIC,
		static_routes=[StaticRoute("2001:db8:1341:3::/64","2001:db8:1341:12::2")])

   r2.addDaemon(STATIC,
		static_routes=[StaticRoute("2001:db8:1341::/60", "2001:db8:1341:12::1"),
                               StaticRoute("2001:db8:1341:1::/64","2001:db8:1341:12::1")])

   r3.addDaemon(STATIC,
		static_routes=[StaticRoute("2001:db8:1341:1::/64", "2001:db8:1341:13::1")])

The ``pingall`` command reveals that there is a problem in this network.

.. code-block:: console

    mininet>pingall
    *** Ping: testing reachability over IPv4 and IPv6
    a --IPv6--> X
    b --IPv6--> X
    *** Results: 100% dropped (0/2 received)

We can analyze this configuration problem in more details by using ``traceroute6``. The loop appears clearly.

.. code-block:: console

   mininet>a traceroute6 -q 1 -n 2001:db8:1341:3::b
   traceroute to 2001:db8:1341:3::b (2001:db8:1341:3::b) from 2001:db8:1341:1::a, 30 hops max, 24 byte packets
   1  2001:db8:1341:1::1  0.102 ms
   2  2001:db8:1341:12::2  0.225 ms
   3  2001:db8:1341:1::1  0.201 ms
   4  2001:db8:1341:12::2  0.075 ms
   5  2001:db8:1341:1::1  0.057 ms
   6  2001:db8:1341:12::2  0.041 ms
   7  2001:db8:1341:1::1  0.051 ms
   8  2001:db8:1341:12::2  0.043 ms
   9  2001:db8:1341:1::1  0.122 ms
   10  2001:db8:1341:12::2  0.058 ms
   11  2001:db8:1341:1::1  0.033 ms
   12  2001:db8:1341:12::2  0.043 ms
   ^C
   mininet>

On host ``b``, the problem is different. The packets that it sends towards host ``a`` do not seem to go beyond router ``r3``.

.. code-block:: console


   mininet> b traceroute6 -q 1 -n 2001:db8:1341:1::a
   traceroute to 2001:db8:1341:1::a (2001:db8:1341:1::a) from 2001:db8:1341:3::b, 30 hops max, 24 byte packets
   1  2001:db8:1341:3::3  0.091 ms
   2  *
   3  *
   4  *
   ^C
   mininet>

To debug this problem, let us look at the forwarding table of ``r3``. This router forwards the packets sent to host ``a`` to router ``r1`` that is directly connected to host ``a``.

.. code-block:: console

   mininet> r3 ip -f inet6 route show
   2001:db8:1341:1::/64 via 2001:db8:1341:13::1 dev r3-eth0  proto 196  metric 20  pref medium
   2001:db8:1341:3::/64 dev r3-eth2  proto kernel  metric 256  pref medium
   2001:db8:1341:13::/64 dev r3-eth0  proto kernel  metric 256  pref medium
   2001:db8:1341:23::/64 dev r3-eth1  proto kernel  metric 256  pref medium
   fe80::/64 dev r3-eth0  proto kernel  metric 256  pref medium
   fe80::/64 dev r3-eth1  proto kernel  metric 256  pref medium
   fe80::/64 dev r3-eth2  proto kernel  metric 256  pref medium

Unfortunately, when router ``r1`` sends its ICMP HopLimit exceeded message, the destination of this IP packet is ``2001:db8:1341:3::b``. This packet is forward to router ``r2`` that returns the packet back to router ``r1``. The packet loops between the two routers until their HopLimit reaches zero.


.. code-block:: console

   mininet> r1 ip -f inet6 route show
   2001:db8:1341:1::/64 dev r1-eth2  proto kernel  metric 256  pref medium
   2001:db8:1341:3::/64 via 2001:db8:1341:12::2 dev r1-eth0  proto 196  metric 20  pref medium
   2001:db8:1341:12::/64 dev r1-eth0  proto kernel  metric 256  pref medium
   2001:db8:1341:13::/64 dev r1-eth1  proto kernel  metric 256  pref medium
   fe80::/64 dev r1-eth2  proto kernel  metric 256  pref medium
   fe80::/64 dev r1-eth0  proto kernel  metric 256  pref medium
   fe80::/64 dev r1-eth1  proto kernel  metric 256  pref medium
   mininet>




IPv6 packets
------------

To correctly understand the operation of IPv6, it is sometimes important to remember the packet format and how the different fields are used.

.. inginious:: ip6-hop

The `Next Header` of the IPv6 packet indicates the type of the header that follows the IPv6 packet. IANA_ maintains a list of all the assigned values of this header at https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

.. inginious:: ip6-tcp

.. inginious:: ip6-udp

.. inginious:: ip6-icmpv6


When an IPv6 router receives a packet that is larger than the Maximum Transmission Unit (MTU) on its outgoing interface, it drops the packet and returns an ICMPv6 message back to the source. Upon reception of this ICMPv6 message, the source will either adjust the size of the packets that it transmits or use IPv6 packet fragmentation. The exercises below show a few examples of the utilization of IPv6 fragmentation.


.. inginious:: ip6-frag-icmp6

.. .. inginious:: ip6-ping6-frag2

Network engineers often rely on :manpage:`ping6(8)` to verify the reachability of a remote host or router. :manpage:`ping6(8)` sends ICMPv6 echo request messages and analyzes the received ICMPv6 echo responses.  Each echo request message contains an identifier and a sequence number that is returned in the response.

.. inginious:: ip6-ping6

When the :manpage:`ping6(8)` is executed, it sends ICMPv6 echo request messages with increasing sequence numbers.

.. inginious:: ip6-ping6-reorder

The :manpage:`traceroute6(8)` software is very useful to debug network problems. It sends a series of UDP segments encapsulated inside IP packets with increasing values of the HopLimit. The first packet has a HotLimit and the first router on the path returns an ICMPv6 HopLimit exceeded message.

.. inginious:: ip6-traceroute6-hop

When :manpage:`traceroute6(8)` sends UDP segments, it uses the UDP source port as a way to remember the target hop for this specific UDP segment.

.. inginious:: ip6-traceroute6-reorder


.. include:: /links.rst
