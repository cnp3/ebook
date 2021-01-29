.. Copyright |copy| 2010, 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_

.. index:: link-state routing

.. _linkstate:

Link state routing
------------------

Link state routing is the second family of routing protocols. While distance vector routers use a distributed algorithm to compute their routing tables, link-state routers exchange messages to allow each router to learn the entire network topology. Based on this learned topology, each router is then able to compute its routing table by using a shortest path computation such as Dijkstra's algorithm [Dijkstra1959]_. A detailed description of this shortest path algorithm may be found in [Wikipedia:Dijkstra]_.

For link-state routing, a network is modeled as a `directed weighted graph`. Each router is a node, and the links between routers are the edges in the graph. A positive weight is associated to each directed edge and routers use the shortest path to reach each destination. In practice, different types of weights can be associated to each directed edge :

 - unit weight. If all links have a unit weight, shortest path routing prefers the paths with the least number of intermediate routers.
 - weight proportional to the propagation delay on the link. If all link weights are configured this way, shortest path routing uses the paths with the smallest propagation delay.
 - :math:`weight=\frac{C}{bandwidth}` where `C` is a constant larger than the highest link bandwidth in the network. If all link weights are configured this way, shortest path routing prefers higher bandwidth paths over lower bandwidth paths.

Usually, the same weight is associated to the two directed edges that correspond to a physical link (i.e. :math:`R1 \rightarrow R2` and :math:`R2 \rightarrow R1`). However, nothing in the link state protocols requires this. For example, if the weight is set in function of the link bandwidth, then an asymmetric ADSL link could have a different weight for the upstream and downstream directions. Other variants are possible. Some networks use optimization algorithms to find the best set of weights to minimize congestion inside the network for a given traffic demand [FRT2002]_.


.. index:: Hello message

When a link-state router boots, it first needs to discover to which routers it is directly connected. For this, each router sends a HELLO message every `N` seconds on all its interfaces. This message contains the router's address. Each router has a unique address. As its neighboring routers also send HELLO messages, the router automatically discovers to which neighbors it is connected. These HELLO messages are only sent to neighbors that are directly connected to a router, and a router never forwards the HELLO messages that it receives. HELLO messages are also used to detect link and router failures. A link is considered to have failed if no HELLO message has been received from a neighboring router for a period of :math:`k \times N` seconds.

    .. tikz::
        :libs: positioning, matrix, arrows, shapes

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em, minimum width=2em, font=\large, node distance=7em}}
        \node[router] (A) {A};
        \node[router, right=of A] (B) { B };
        \node[router, below=of B] (C) {C};

        \path[draw,thick]
        (A) edge (B)
        (B) edge (C);

        \draw[orange, arrow] ([yshift=1em, xshift=1em] A.east) -- ([yshift=1em, xshift=-1em] B.west) node [midway] (msg1) {};
        \draw ([yshift=1em]msg1) -- ([yshift=1em]msg1) node [rectangle, draw, font=\tiny] {A: HELLO};

        \draw[orange, arrow] ([yshift=-1em, xshift=-1em] B.west) -- ([yshift=-1em, xshift=1em] A.east) node [midway] (msg2) {};
        \draw ([yshift=-1em]msg2) -- ([yshift=-1em]msg2) node [rectangle, draw, font=\tiny] {B: HELLO};

        \draw[orange, arrow] ([xshift=-1em, yshift=-1em] B.south) -- ([xshift=-1em, , yshift=1em] C.north) node [midway] (msg3) {};
        \draw ([xshift=-1em]msg3) -- ([xshift=-1em]msg3) node [rotate=-90,rectangle, draw, font=\tiny] {B: HELLO};

        \draw[orange, arrow] ([xshift=1em, , yshift=1em] C.north) -- ([xshift=1em, yshift=-1em] B.south) node [midway] (msg3) {};
        \draw ([xshift=1em]msg3) -- ([xshift=1em]msg3) node [rotate=90,rectangle, draw, font=\tiny] {C: HELLO};

   The exchange of HELLO messages


Once a router has discovered its neighbors, it must reliably distribute all its outgoing edges to all routers in the network to allow them to compute their local view of the network topology. For this, each router builds a `link-state packet` (LSP) containing the following information:

 - LSP.Router: identification (address) of the sender of the LSP
 - LSP.age: age or remaining lifetime of the LSP
 - LSP.seq: sequence number of the LSP
 - LSP.Links[]: links advertised in the LSP. Each directed link is represented with the following information:

   - LSP.Links[i].Id: identification of the neighbor
   - LSP.Links[i].cost: cost of the link

These LSPs must be reliably distributed inside the network without using the router's routing table since these tables can only be computed once the LSPs have been received. The `Flooding` algorithm is used to efficiently distribute the LSPs of all routers. Each router that implements `flooding` maintains a `link state database` (LSDB) containing the most recent LSP sent by each router. When a router receives a LSP, it first verifies whether this LSP is already stored inside its LSDB. If so, the router has already distributed the LSP earlier and it does not need to forward it. Otherwise, the router forwards the LSP on all its links except the link over which the LSP was received. Flooding can be implemented by using the following pseudo-code.

.. code-block:: python

    # links is the set of all links on the router
    # Router R's LSP arrival on link l
    if newer(LSP, LSDB(LSP.Router)) :
        LSDB.add(LSP)  # implicitly removes older LSP from same router
        for i in links:
            if i!=l:
      	       send(LSP,i)
    # else, LSP has already been flooded


In this pseudo-code, `LSDB(r)` returns the most recent `LSP` originating from router `r` that is stored in the `LSDB`. `newer(lsp1, lsp2)` returns true if `lsp1` is more recent than `lsp2`. See the note below for a discussion on how `newer` can be implemented.

.. note:: Which is the most recent LSP ?

 A router that implements flooding must be able to detect whether a received LSP is newer than the stored LSP. This requires a comparison between the sequence number of the received LSP and the sequence number of the LSP stored in the link state database. The ARPANET routing protocol [MRR1979]_ used a 6 bits sequence number and implemented the comparison as follows :rfc:`789`

 .. code-block:: python

    def newer( lsp1, lsp2 ):
        return ( ((lsp1.seq > lsp2.seq) and ((lsp1.seq - lsp2.seq) <= 32)) or
     	       ( (lsp1.seq < lsp2.seq) and ((lsp2.seq - lsp1.seq) > 32)) )

 This comparison takes into account the modulo :math:`2^{6}` arithmetic used to increment the sequence numbers. Intuitively, the comparison divides the circle of all sequence numbers into two halves. Usually, the sequence number of the received LSP is equal to the sequence number of the stored LSP incremented by one, but sometimes the sequence numbers of two successive LSPs may differ, e.g. if one router has been disconnected for some time. The comparison above worked well until October 27, 1980. On this day, the ARPANET crashed completely. The crash was complex and involved several routers. At one point, LSP `40` and LSP `44` from one of the routers were stored in the LSDB of some routers in the ARPANET. As LSP `44` was the newest, it should have replaced LSP `40` on all routers. Unfortunately, one of the ARPANET routers suffered from a memory problem and sequence number `40` (`101000` in binary) was replaced by `8` (`001000` in binary) in the buggy router and flooded. Three LSPs were present in the network and `44` was newer than `40` which is newer than `8`, but unfortunately `8` was considered to be newer than `44`... All routers started to exchange these three link state packets forever and the only solution to recover from this problem was to shutdown the entire network :rfc:`789`.

 Current link state routing protocols usually use 32 bits sequence numbers and include a special mechanism in the unlikely case that a sequence number reaches the maximum value (with a 32 bits sequence number space, it takes 136 years to cycle the sequence numbers if a link state packet is generated every second).

 To deal with the memory corruption problem, link state packets contain a checksum or CRC. This checksum is computed by the router that generates the LSP. Each router must verify the checksum when it receives or floods an LSP. Furthermore, each router must periodically verify the checksums of the LSPs stored in its LSDB. This enables them to cope with memory errors that could corrupt the LSDB as the one that occurred in the ARPANET.

Flooding is illustrated in the figure below. By exchanging HELLO messages, each router learns its direct neighbors. For example, router `E` learns that it is directly connected to routers `D`, `B` and `C`. Its first LSP has sequence number `0` and contains the directed links `E->D`, `E->B` and `E->C`. Router `E` sends its LSP on all its links and routers `D`, `B` and `C` insert the LSP in their LSDB and forward it over their other links.


    .. tikz::
       :libs: positioning, matrix, arrows

       \tikzstyle{arrow} = [thick,->,>=stealth]
       \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em, minimum width=2em, font=\large, node distance=8em}}
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \tikzset{rtable/.style={rectangle, dashed, draw, font=\small, node distance=3em} }
       \node[router] (A) {A};
       \node[rtable, above left=of A] (RTA) { \begin{tabular}{l}
       Links \\
       \hline
       A $\rightarrow$ B: 1 \\
       A $\rightarrow$ D: 1 \\
       \end{tabular}};
       \node[router, right=of A] (B) { B };
       \node[rtable, above=of B] (RTB) { \begin{tabular}{l}
       Links \\
       \hline
       B $\rightarrow$ A: 1 \\
       B $\rightarrow$ C: 1 \\
       B $\rightarrow$ E: 1 \\
       \end{tabular}};
       \node[router,right=of B] (C) {C};
       \node[rtable, above right=of C] (RTC) { \begin{tabular}{l}
       Links \\
       \hline
       C $\rightarrow$ B: 1 \\
       C $\rightarrow$ E: 1 \\
       \end{tabular}};
       \node[router,below=of A] (D) {D};
       \node[rtable, left=of D] (RTD) { \begin{tabular}{l}
       Links \\
       \hline
       D $\rightarrow$ A: 1 \\
       D $\rightarrow$ E: 1 \\
       \end{tabular}};
       \node[router, right=of D] (E) {E};
       \node[rtable, right=of E] (RTE) { \begin{tabular}{l}
       Links \\
       \hline
       E $\rightarrow$ B: 1 \\
       E $\rightarrow$ C: 1 \\
       E $\rightarrow$ D: 1 \\
       \end{tabular}};

       \path[draw,thick]
       (A) edge (B)
       (A) edge (D)
       (B) edge (C)
       (B) edge (E)
       (C) edge (E)
       (D) edge (E);

       \draw[dashed] (RTA) -- (A);
       \draw[dashed] (RTB) -- (B);
       \draw[dashed] (RTC) -- (C);
       \draw[dashed] (RTD) -- (D);
       \draw[dashed] (RTE) -- (E);

   Flooding : example


Flooding allows LSPs to be distributed to all routers inside the network without relying on routing tables. In the example above, the LSP sent by router `E` is likely to be sent twice on some links in the network. For example, routers `B` and `C` receive `E`'s LSP at almost the same time and forward it over the `B-C` link. To avoid sending the same LSP twice on each link, a possible solution is to slightly change the pseudo-code above so that a router waits for some random time before forwarding a LSP on each link. The drawback of this solution is that the delay to flood an LSP to all routers in the network increases. In practice, routers immediately flood the LSPs that contain new information (e.g. addition or removal of a link) and delay the flooding of refresh LSPs (i.e. LSPs that contain exactly the same information as the previous LSP originating from this router) [FFEB2005]_.

To ensure that all routers receive all LSPs, even when there are transmissions errors, link state routing protocols use `reliable flooding`. With `reliable flooding`, routers use acknowledgments and if necessary retransmissions to ensure that all link state packets are successfully transferred to each neighboring router. Thanks to reliable flooding, all routers store in their LSDB the most recent LSP sent by each router in the network. By combining the received LSPs with its own LSP, each router can build a graph that represents the entire network topology.

    .. tikz::
       :libs: positioning, matrix, arrows

       \tikzstyle{arrow} = [thick,->,>=stealth]
       \tikzset{router/.style = {rectangle, draw, text centered, thick, minimum height=2em, minimum width=2em, font=\large, node distance=8em}}
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \tikzset{rtable/.style={rectangle, dashed, draw, font=\small, node distance=4em} }
       \node[router] (A) {A};
       \node[rtable, above left=of A] (RTA) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router, right=of A] (B) { B };
       \node[rtable, above=of B] (RTB) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router,right=of B] (C) {C};
       \node[rtable, above right=of C] (RTC) {\begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router,below=of A] (D) {D};
       \node[rtable, left=of D] (RTD) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router, right=of D] (E) {E};
       \node[rtable, right=of E] (RTE) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};

       \path[draw,thick]
       (A) edge (B)
       (A) edge (D)
       (B) edge (C)
       (B) edge (E)
       (C) edge (E)
       (D) edge (E);

       \draw[dashed] (RTA) -- (A);
       \draw[dashed] (RTB) -- (B);
       \draw[dashed] (RTC) -- (C);
       \draw[dashed] (RTD) -- (D);
       \draw[dashed] (RTE) -- (E);

   Link state databases received by all routers


.. note:: Static or dynamic link metrics ?

 As link state packets are flooded regularly, routers are able to measure the quality (e.g. delay or load) of their links and adjust the metric of each link according to its current quality. Such dynamic adjustments were included in the ARPANET routing protocol [MRR1979]_ . However, experience showed that it was difficult to tune the dynamic adjustments and ensure that no forwarding loops occur in the network [KZ1989]_. Today's link state routing protocols use metrics that are manually configured on the routers and are only changed by the network operators or network management tools [FRT2002]_.

.. index:: two-way connectivity

When a link fails, the two routers attached to the link detect the failure by the absence of HELLO messages received during the last :math:`k \times N` seconds. Once a router has detected the failure of one of its local links, it generates and floods a new LSP that no longer contains the failed link. This new LSP replaces the previous LSP in the network. In practice, the two routers attached to a link do not detect this failure exactly at the same time. During this period, some links may be announced in only one direction. This is illustrated in the figure below. Router `E` has detected the failure of link `E-B` and flooded a new LSP, but router `B` has not yet detected this failure.


    .. tikz::
       :libs: positioning, matrix, arrows

       \tikzstyle{arrow} = [thick,->,>=stealth]
       \tikzset{router/.style = {rectangle, draw, text centered, thick, minimum height=2em, minimum width=2em, font=\large, node distance=7em}}
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \tikzset{rtable/.style={rectangle, dashed, draw, font=\small, node distance=4em} }
       \node[router] (A) {A};
       \node[rtable, above left=of A] (RTA) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router, right=of A] (B) { B };
       \node[rtable, above=of B] (RTB) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router,right=of B] (C) {C};
       \node[rtable, above right=of C] (RTC) {\begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router,below=of A] (D) {D};
       \node[rtable, left=of D] (RTD) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E, E $\rightarrow$ B: 1 & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & E-0 [B:1];[C:1];[D:1] \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};
       \node[router, right=of D] (E) {E};
       \node[rtable, below right=of E] (RTE) { \begin{tabular}{l|l}
       Links & LSPs \\
       \hline
       A $\rightarrow$ B, B $\rightarrow$ A: 1 & A-0 [B:1];[D:1] \\
       A $\rightarrow$ D, D $\rightarrow$ A: 1 & B-0 [A:1];[C:1];[E:1] \\
       B $\rightarrow$ C, C $\rightarrow$ B: 1 & C-0 [B:1];[E:1] \\
       B $\rightarrow$ E: 1, {\color{red}\sout{E $\rightarrow$ B: 1}} & D-0 [A:1];[E:1] \\
       C $\rightarrow$ E, E $\rightarrow$ C: 1 & {\color{red} E-1 [C:1];[D:1]} \\
       D $\rightarrow$ E, E $\rightarrow$ D: 1 & \\
       \end{tabular}};

       \path[draw,thick]
       (A) edge (B)
       (A) edge (D)
       (B) edge (C)
       (B) edge (E)
       (C) edge (E)
       (D) edge (E);

       \draw (B) -- (E) node [red, midway, very thick] {\Large \sffamily\textbf{X}};

       \draw[orange, arrow] ([xshift=-1em, yshift=-1.5em] E.west) -- ([xshift=1em, yshift=-1.5em] D.east) node [midway] (msg1) {};
       \draw ([yshift=-1.5em]msg1) -- ([yshift=-1.5em]msg1) node [rectangle, draw, thick, font=\small] {\textbf{LSP: E-1 [C:1];[D:1]}};

       \draw[orange, arrow] ([xshift=1em, yshift=0.75em] E.east) -- ([xshift=1em, yshift=-1.75em] C.west) node [midway] (msg2) {};
       \draw ([xshift=1em]msg2) -- ([xshift=1em, yshift=-1em]msg2) node [rotate=45, rectangle, draw, thick, font=\small] {\textbf{LSP: E-1 [C:1];[D:1]}};

       \draw[dashed] (RTA) -- (A);
       \draw[dashed] (RTB) -- (B);
       \draw[dashed] (RTC) -- (C);
       \draw[dashed] (RTD) -- (D);
       \draw[dashed] (RTE) -- (E);

   The two-way connectivity check


When a link is reported in the LSP of only one of the attached routers, routers consider the link as having failed and they remove it from the directed graph that they compute from their LSDB. This is called the `two-way connectivity check`. This check allows link failures to be quickly flooded as a single LSP is sufficient to announce such bad news. However, when a link comes up, it can only be used once the two attached routers have sent their LSPs. The `two-way connectivity check` also allows for dealing with router failures. When a router fails, all its links fail by definition. These failures are reported in the LSPs sent by the neighbors of the failed router. The failed router does not, of course, send a new LSP to announce its failure. However, in the graph that represents the network, this failed router appears as a node that only has outgoing edges. Thanks to the `two-way connectivity check`, this failed router cannot be considered as a transit router to reach any destination since no outgoing edge is attached to it.

When a router has failed, its LSP must be removed from the LSDB of all routers [#foverload]_. This can be done by using the `age` field that is included in each LSP. The `age` field is used to bound the maximum lifetime of a link state packet in the network. When a router generates a LSP, it sets its lifetime (usually measured in seconds) in the `age` field. All routers regularly decrement the `age` of the LSPs in their LSDB and a LSP is discarded once its `age` reaches `0`. Thanks to the `age` field, the LSP from a failed router does not remain in the LSDBs forever.

To compute its forwarding table, each router computes the spanning tree rooted at itself by using Dijkstra's shortest path algorithm [Dijkstra1959]_. The forwarding table can be derived automatically from the spanning as shown in the figure below.

    .. tikz::
       :libs: positioning, matrix, arrows

       \tikzstyle{arrow} = [thick,->,>=stealth]
       \tikzset{router/.style = {rectangle, draw, text centered, thick, minimum height=2em, minimum width=2em, font=\large, node distance=4em}}
       \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
       \tikzset{rtable/.style={rectangle, dashed, draw, font=\small, node distance=6em} }
       \node[router] (R1) {R1};
       \node[router, above right=of R1] (R2) { R2 };
       \node[router,below right=of R1] (R3) {R3};
       \node[rtable, left=of R3] (FT) {\begin{tabular}{l}
       Forwarding table \\
       \hline
       R1: West \\
       R2: North \\
       R4: East \\
       R5: East \\
       R6: East \\
       \end{tabular}};
       \node[router,right=of R2] (R5) {R5};
       \node[router,right=of R3] (R4) {R4};
       \node[router,below right=of R5] (R6) {R6};

       \draw[thick] (R1) -- (R2) node [midway, above, rotate=45] {D = 3};
       \draw[thick, red] (R1) -- (R3) node [midway, below, rotate=-45] {D = 5};
       \draw[thick, red] (R2) -- (R3) node [midway, rotate=90, above] {D = 3};
       \draw[thick] (R2) -- (R5) node [midway, above] {D = 2};
       \draw[thick, red] (R3) -- (R4) node [midway, above] {D = 1};
       \draw[thick, red] (R5) -- (R4) node [midway, rotate=90, below] {D = 3};
       \draw[thick] (R5) -- (R6) node [midway, above, rotate=-45] {D = 10};
       \draw[thick, red] (R4) -- (R6) node [midway, below, rotate=45] {D = 6};

       \draw[dashed] (FT) -- (R3);

   Computation of the forwarding table, the paths used by packets sent by R3 are shown in red


.. inginious:: q-net-ls


.. rubric:: Footnotes

.. [#foverload] It should be noted that link state routing assumes that all routers in the network have enough memory to store the entire LSDB. The routers that do not have enough memory to store the entire LSDB cannot participate in link state routing. Some link state routing protocols allow routers to report that they do not have enough memory and must be removed from the graph by the other routers in the network, but this is outside the scope of this e-book.
