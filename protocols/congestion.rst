.. Copyright |copy| 2013, 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_



.. _TCPCongestion:

Congestion control
------------------

In an internetwork, i.e. a network composed of different types of networks (such as the Internet), congestion control could be implemented either in the network layer or the transport layer. The congestion problem was clearly identified in the late 1980s and the Internet researchers who developed techniques to solve the problem opted for a solution in the transport layer. Adding congestion control to the transport layer makes sense since this layer provides a reliable data transfer and avoiding congestion is a factor in this reliable delivery. The transport layer already deals with heterogeneous networks thanks to its `self-clocking` property that we have already described. In this section, we explain different congestion control techniques that have been added to TCP and other transport protocols such as SCTP or QUIC.

The TCP congestion control scheme was initially proposed by `Van Jacobson`_ in [Jacobson1988]_. The current specification may be found in :rfc:`5681`. TCP relies on `Additive Increase and Multiplicative Decrease (AIMD)`. To implement :term:`AIMD`, a TCP host must be able to control its transmission rate. A first approach would be to use timers and adjust their expiration times in function of the rate imposed by :term:`AIMD`. Unfortunately, maintaining such timers for a large number of TCP connections can be difficult. Instead, `Van Jacobson`_ noted that the sending rate of a TCP connection can be artificially controlled by constraining its sending window. A TCP connection cannot send data faster than :math:`\frac{window}{rtt}` where :math:`window` is the minimum between the host's sending window and the receive window advertised by the receiver.

TCP's congestion control scheme is based on a `congestion window`. The current value of the congestion window (`cwnd`) is stored in the TCB of each TCP connection and the window that can be used by the sender is constrained by :math:`\min(cwnd,rwin,swin)` where :math:`swin` is the current sending window and :math:`rwin` the last received receive window. The `Additive Increase` part of the TCP congestion control increments the congestion window by :term:`MSS` bytes every round-trip-time. In the TCP literature, this phase is often called the `congestion avoidance` phase. The `Multiplicative Decrease` part of the TCP congestion control halves the current value of the congestion window once congestion has been detected.

When a TCP connection begins, the sending host does not know whether the part of the network that it uses to reach the destination is congested or not. To avoid causing too much congestion, it must start with a small congestion window. In 1998, [Jacobson1988]_ recommended an initial window of MSS bytes. As the additive increase part of the TCP congestion control scheme increments the congestion window by MSS bytes every round-trip-time, the TCP connection may have to wait many round-trip-times before being able to efficiently use the available bandwidth. This is especially important in environments where the :math:`bandwidth \times rtt` product is high. To avoid waiting too many round-trip-times before reaching a congestion window that is large enough to efficiently utilize the network, the TCP congestion control scheme includes the `slow-start` algorithm. The objective of the TCP `slow-start` phase is to quickly reach an acceptable value for the `cwnd`. During `slow-start`, the congestion window is doubled every round-trip-time. The `slow-start` algorithm uses an additional variable in the TCB : `ssthresh` (`slow-start threshold`). The `ssthresh` is an estimation of the last value of the `cwnd` that did not cause congestion. It is initialized at the sending window and is updated after each congestion event.


A key question that must be answered by any congestion control scheme is how congestion is detected. The first implementations of the TCP congestion control scheme opted for a simple and pragmatic approach : packet losses indicate congestion. If the network is congested, router buffers are full and packets are discarded. In wired networks, packet losses are mainly caused by congestion. In wireless networks, packets can be lost due to transmission errors and for other reasons that are independent of congestion. TCP already detects segment losses to ensure a reliable delivery. The TCP congestion control scheme distinguishes between two types of congestion :

 - `mild congestion`. TCP considers that the network is lightly congested if it receives three duplicate acknowledgments and performs a fast retransmit. If the fast retransmit is successful, this implies that only one segment has been lost. In this case, TCP performs multiplicative decrease and the congestion window is divided by `2`. The slow-start threshold is set to the new value of the congestion window.
 - `severe congestion`. TCP considers that the network is severely congested when its retransmission timer expires. In this case, TCP retransmits the first segment, sets the slow-start threshold to 50% of the congestion window. The congestion window is reset to its initial value and TCP performs a slow-start.

The figure below illustrates the evolution of the congestion window when there is severe congestion. At the beginning of the connection, the sender performs `slow-start` until the first segments are lost and the retransmission timer expires. At this time, the `ssthresh` is set to half of the current congestion window and the congestion window is reset at one segment. The lost segments are retransmitted as the sender again performs slow-start until the congestion window reaches the `sshtresh`. It then switches to congestion avoidance and the congestion window increases linearly until segments are lost and the retransmission timer expires.


.. tikz:: Evaluation of the TCP congestion window with severe congestion
   :libs: calc, math, arrows

   \draw[->] (-0.2,0) -- (12,0) node[below] {$t$};
   \draw[->] (0,-1.2) -- (0,3) node[above] {$cwnd$};
   \draw[color=red,domain=0:4,variable=\x]    plot (\x,{0.1*(1+2^(\x))})       node[left] {slow start};
   \draw[-,dashed] (4,1) -- (4,3) node [above] {timer};
   \draw[-,dashed,color=red] (4,0.8) -- (8,0.8) node[below] {threshold};
   \draw[color=red,domain=4:7,variable=\x]    plot (\x,{0.1*(1+2^(\x-4))}) ; 
   \draw[color=blue,domain=7:10]   plot (\x,{0.1*(1+8+(\x-7))})     node[above] {congestion avoidance};
   \draw[-,dashed] (10,0.5) -- (10,2.5) node [above] {timer};
   \draw[-,dashed,color=red] (9,0.65) -- (12,0.65) node[above] {threshold};  \draw[color=red,domain=10:12,variable=\x]    plot (\x,{0.1*(1+2^(\x-10))}) ; 

	  
The figure below illustrates the evolution of the congestion window when the network is lightly congested and all lost segments can be retransmitted using fast retransmit. The sender begins with a slow-start. A segment is lost but successfully retransmitted by a fast retransmit. The congestion window is divided by 2 and the sender immediately enters congestion avoidance as this was a mild congestion.


.. tikz:: Evaluation of the TCP congestion window when the network is lightly congested

     \draw[->] (-0.2,0) -- (12,0) node[below] {$t$};
  \draw[->] (0,-1.2) -- (0,3) node[above] {$cwnd$};
  \draw[color=red,domain=0:4,variable=\x]    plot (\x,{0.1*(1+2^(\x))})       node[left] {slow start};
  \draw[->,dashed] (4,3.5) -- (4,2.5) node [below] {fast retransmit};
  \draw[-,dashed,color=red] (4,0.8) -- (7,0.8) node[below] {threshold};
  \draw[color=blue,domain=4:9]   plot (\x,{0.8+0.1*(0.7+(\x-4))})     node[above] {congestion avoidance};
   \draw[->,dashed] (9,3.5) -- (9,2.5) node [below] {fast retransmit};
  \draw[-,dashed,color=red] (8,0.46) -- (11,0.46) node[below] {threshold};
  \draw[color=blue,domain=9:12]   plot (\x,{0.46+0.1*(0.7+(\x-9))})  node[right] {congestion avoidance};



Most TCP implementations update the congestion window when they receive an acknowledgment. If we assume that the receiver acknowledges each received segment and the sender only sends MSS sized segments, the TCP congestion control scheme can be implemented using the simplified pseudo-code [#fwrap]_ below. This pseudocode includes the optimization proposed in :rfc:`3042` that allows a sender to send new unsent data upon reception of the first or second duplicate acknowledgment. The reception of each of these acknowledgments indicates that one segment has left the network and thus additional data can be sent without causing more congestion. Note that the congestion window is *not* increased upon reception of these first duplicate acknowledgments.

.. code-block:: python

    # NewReno congestion control in TCP		
		
    # Initialization
    cwnd = MSS  # congestion window in bytes
    ssthresh= swin # in bytes

    # Ack arrival
    if tcp.ack > snd.una:  # new ack, no congestion
        if dupacks == 0:  # not currently recovering from loss
            if cwnd < ssthresh:
                # slow-start : quickly increase cwnd
                # double cwnd every rtt
                cwnd = cwnd + MSS
            else:
                # congestion avoidance : slowly increase cwnd
                # increase cwnd by one mss every rtt
                cwnd = cwnd + MSS * (MSS / cwnd)
        else:  # recovering from loss
            cwnd = ssthresh  # deflate cwnd RFC5681
            dupacks = 0
    else:  # duplicate or old ack
        if tcp.ack == snd.una:  # duplicate acknowledgment
            dupacks += 1
            if dupacks == 1 or dupacks == 2:
                send_next_unacked_segment  # RFC3042
            if dupacks == 3:
                retransmitsegment(snd.una)
                ssthresh = max(cwnd/2, 2*MSS)
                cwnd = ssthresh
            if dupacks > 3:  # RFC5681
                cwnd = cwnd + MSS  # inflate cwnd
        else:
            # ack for old segment, ignored
            pass

    Expiration of the retransmission timer:
        send(snd.una)  # retransmit first lost segment
        sshtresh = max(cwnd/2, 2*MSS)
        cwnd = MSS


Furthermore when a TCP connection has been idle for more than its current retransmission timer, it should reset its congestion window to the congestion window size that it uses when the connection begins, as it no longer knows the current congestion state of the network. This congestion control scheme is known as the :index:`NewReno` congestion control scheme.

.. note:: Initial congestion window

 The original TCP congestion control mechanism [Jacobson1988]_ recommended that each TCP connection should begin by setting :math:`cwnd=MSS`. However, in today's higher bandwidth networks, using such a small initial congestion window severely affects the performance for short TCP connections, such as those used by web servers. In 2002, :rfc:`3390` allowed an initial congestion window of about 4 KBytes, which corresponds to 3 segments in many environments. In 2010, researchers from Google proposed to further increase the initial window up to 15 KBytes [DRC+2010]_. The measurements that they collected show that this increase would not significantly increase congestion but would significantly reduce the latency of short HTTP responses. Unsurprisingly, the chosen initial window corresponds to the average size of an HTTP response from a search engine. This proposed modification has been adopted in :rfc:`6928` and TCP implementations support it.


Controlling congestion without losing data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In today's Internet, congestion is controlled by regularly sending packets at a higher rate than the network capacity. These packets fill the buffers of the routers and are eventually discarded. But shortly after, TCP senders retransmit packets containing exactly the same data. This is potentially a waste of resources since these successive retransmissions consume resources upstream of the router that discards the packets. Packet losses are not the only signal to detect congestion inside the network. An alternative is to allow routers to explicitly indicate their current level of congestion when forwarding packets. This approach was proposed in the late 1980s [RJ1995]_ and used in some networks. Unfortunately, it took almost a decade before the Internet community agreed to consider this approach. In the mean time, a large number of TCP implementations and routers were deployed on the Internet.

.. spelling:word-list::

   ECN

Explicit Congestion Notification :rfc:`3168` improves the detection of congestion by allowing routers to explicitly mark packets when they are lightly congested. In theory, a single bit in the packet header [RJ1995]_ is sufficient to support this congestion control scheme. When a host receives a marked packet, it returns the congestion information to the source that adapts its transmission rate accordingly. Although the idea is relatively simple, deploying it on the entire Internet has proven to be challenging [KNT2013]_. It is interesting to analyze the different factors that have hindered the deployment of this technique.

The first difficulty in adding Explicit Congestion Notification (ECN) in TCP/IP network was to modify the format of the network packet and transport segment headers to carry the required information. In the network layer, one bit was required to allow the routers to mark the packets they forward during congestion periods. In the IP network layer, this bit is called the `Congestion Experienced` (`CE`) bit and is part of the packet header. However, using a single bit to mark packets is not sufficient. Consider a simple scenario with two sources, one congested router and one destination. Assume that the first sender and the destination support ECN, but not the second sender. If the router is congested it will mark packets from both senders. The first sender will react to the packet markings by reducing its transmission rate. However since the second sender does not support ECN, it will not react to the markings. Furthermore, this sender could continue to increase its transmission rate, which would lead to more packets being marked and the first source would decrease again its transmission rate, ... In the end, the sources that implement ECN would be penalized compared to the sources that do not implement it. This unfairness is a major hurdle to widely deploy ECN on the public Internet [#fprivate]_. The solution proposed in :rfc:`3168` to deal with this problem is to use a second bit in the network packet header. This bit, called the `ECN-capable transport` (ECT) bit, indicates whether the packet contains a segment produced by a transport protocol that supports ECN or not. Transport protocols that support ECN set the ECT bit in all packets. When a router is congested, it first verifies whether the ECT bit is set. In this case, the CE bit of the packet is set to indicate congestion. Otherwise, the packet is discarded. This eases the deployment of ECN [#fecnnonce]_.

The second difficulty is how to allow the receiver to inform the sender of the reception of network packets marked with the `CE` bit. In reliable transport protocols like TCP and SCTP, the acknowledgments can be used to provide this feedback. For TCP, two options were possible : change some bits in the TCP segment header or define a new TCP option to carry this information. The designers of ECN opted for reusing spare bits in the TCP header. More precisely, two TCP flags have been added in the TCP header to support ECN. The `ECN-Echo` (ECE) is set in the TCP acknowledgments when the `CE` was set in packets received on the forward path.

.. figure:: /pkt/tcp-enc.*
   :scale: 120

   The TCP flags


The third difficulty is to allow an ECN-capable sender to detect whether the remote host also supports ECN. This is a classical negotiation of extensions to a transport protocol. In TCP, this could have been solved by defining a new TCP option used during the three-way handshake. To avoid wasting space in the TCP options, the designers of ECN opted in :rfc:`3168` for using the `ECN-Echo` and `CWR` bits in the TCP header to perform this negotiation. In the end, the result is the same with fewer bits exchanged and without wasting TCP option space.

.. SCTP defines in [STD2013]_ the `ECN Support parameter` which can be included in the ``INIT`` and ``INIT-ACK`` chunks to negotiate the utilization of ECN. The solution adopted for SCTP is cleaner than the solution adopted for TCP.

Thanks to the `ECT`, `CE` and `ECE`, routers can mark packets during congestion and receivers can return the congestion information back to the TCP senders. However, these three bits are not sufficient to allow a server to reliably send the `ECE` bit to a TCP sender. TCP acknowledgments are not sent reliably. A TCP acknowledgment always contains the next expected sequence number. Since TCP acknowledgments are cumulative, the loss of one acknowledgment is recovered by the correct reception of a subsequent acknowledgment.

If TCP acknowledgments are overloaded to carry the `ECE` bit, the situation is different. Consider the example shown in the figure below. A client sends packets to a server through a router. In the example below, the first packet is marked. The server returns an acknowledgment with the `ECE` bit set. Unfortunately, this acknowledgment is lost and never reaches the client. Shortly after, the server sends a data segment that also carries a cumulative acknowledgment. This acknowledgment confirms the reception of the data to the client, but it did not receive the congestion information through the `ECE` bit.


 .. msc::

      client [label="client", linecolour=black],
      router [label="router", linecolour=black],
      server [label="server", linecolour=black];

      client=>router [ label = "data[seq=1,ECT=1,CE=0]", arcskip="1" ];
      router=>server [ label = "data[seq=1,ECT=1,CE=1]", arcskip="1"];
      |||;
      server=>router [ label = "ack=2,ECE=1", arcskip="1" ];
      router -x client [label="ack=2,ECE=1", arcskip="1" ];
      |||;
      server=>router [ label = "data[seq=x,ack=2,ECE=0,ECT=1,CE=0]", arcskip="1" ];
      router=>client [ label = "data[seq=x,ack=2,ECE=0,ECT=1,CE=0]", arcskip="1"];
      |||;
      client->server [linecolour=white];



To solve this problem, :rfc:`3168` uses an additional bit in the TCP header : the `Congestion Window Reduced` (CWR) bit.

 .. msc::

      client [label="client", linecolour=black],
      router [label="router", linecolour=black],
      server [label="server", linecolour=black];
      client=>router [ label = "data[seq=1,ECT=1,CE=0]", arcskip="1" ];
      router=>server [ label = "data[seq=1,ECT=1,CE=1]", arcskip="1"];
      |||;
      server=>router [ label = "ack=2,ECE=1", arcskip="1" ];
      router -x client [label="ack=2,ECE=1", arcskip="1" ];
      |||;
      server=>router [ label = "data[seq=x,ack=2,ECE=1,ECT=1,CE=0]", arcskip="1" ];
      router=>client [ label = "data[seq=x,ack=2,ECE=1,ECT=1,CE=0]", arcskip="1"];
      |||;
      client=>router [ label = "data[seq=1,ECT=1,CE=0,CWR=1]", arcskip="1" ];
      router=>server [ label = "data[seq=1,ECT=1,CE=1,CWR=1]", arcskip="1"];
      |||;
      client->server [linecolour=white];


The `CWR` bit of the TCP header provides some form of acknowledgment for the `ECE` bit. When a TCP receiver detects a packet marked with the `CE` bit, it sets the `ECE` bit in all segments that it returns to the sender. Upon reception of an acknowledgment with the `ECE` bit set, the sender reduces its congestion window to reflect a mild congestion and sets the `CWR` bit. This bit remains set as long as the segments received contained the `ECE` bit set. A sender should only react once per round-trip-time to marked packets.

.. .. index:: SCTP ECN Echo chunk, SCTP CWR chunk

.. SCTP uses a different approach to inform the sender once congestion has been detected. Instead of using one bit to carry the congestion notification from the receiver to the sender, SCTP defines an entire ``ECN Echo`` chunk for this. This chunk contains the lowest ``TSN`` that was received in a packet with the `CE` bit set and the number of marked packets received. The SCTP ``CWR`` chunk allows to acknowledge the reception of an ``ECN Echo`` chunk. It echoes the lowest ``TSN`` placed in the ``ECN Echo`` chunk.


The last point that needs to be discussed about Explicit Congestion Notification is the algorithm that is used by routers to detect congestion. On a router, congestion manifests itself by the number of packets that are stored inside the router buffers. As explained earlier, we need to distinguish between two types of routers :

 - routers that have a single FIFO queue
 - routers that have several queues served by a round-robin scheduler

Routers that use a single queue measure their buffer occupancy as the number of bytes or packets stored in the queue [#fslot]_. A first method to detect congestion is to measure the instantaneous buffer occupancy and consider the router to be congested as soon as this occupancy is above a threshold. Typical values of the threshold could be 40% of the total buffer. Measuring the instantaneous buffer occupancy is simple since it only requires one counter. However, this value is fragile from a control viewpoint since it changes frequently. A better solution is to measure the *average* buffer occupancy and consider the router to be congested when this average occupancy is too high. Random Early Detection (RED) [FJ1993]_ is an algorithm that was designed to support Explicit Congestion Notification. In addition to measuring the average buffer occupancy, it also uses probabilistic marking. When the router is congested, the arriving packets are marked with a probability that increases with the average buffer occupancy. The main advantage of using probabilistic marking instead of marking all arriving packets is that flows will be marked in proportion to the number of packets that they transmit. If the router marks 10% of the arriving packets when congested, then a large flow that sends hundred packets per second will be marked 10 times while a flow that only sends one packet per second will not be marked. This probabilistic marking allows marking packets in proportion of their usage of the network resources.

If the router uses several queues served by a scheduler, the situation is different. If a large and a small flow are competing for bandwidth, the scheduler will already favor the small flow that is not using its fair share of the bandwidth. The queue for the small flow will be almost empty while the queue for the large flow will build up. On routers using such schedulers, a good way of marking the packets is to set a threshold on the occupancy of each queue and mark the packets that arrive in a particular queue as soon as its occupancy is above the configured threshold.


Modeling TCP congestion control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Thanks to the NewReno congestion control scheme, TCP can adapt its transmission rate to the losses that occur in the network. Intuitively, the TCP transmission rate decreases when the percentage of losses increases. Researchers have proposed detailed models that allow the prediction of the throughput of a TCP connection when losses occur [MSMO1997]_ . To have some intuition about the factors that affect the performance of TCP, let us consider a very simple model. Its assumptions are not completely realistic, but it gives a good intuition without requiring complex mathematics.

This model considers a hypothetical TCP connection that suffers from equally spaced segment losses. If :math:`p` is the segment loss ratio, then the TCP connection successfully transfers :math:`\frac{1}{p}-1` segments and the next segment is lost. If we ignore the slow-start at the beginning of the connection, TCP in this environment is always in congestion avoidance as there are only isolated losses that can be recovered using fast retransmit. The evolution of the congestion window is thus as shown in the figure below. Note that the `x-axis` of this figure represents time measured in units of one round-trip-time, which is supposed to be constant in the model, and the `y-axis` represents the size of the congestion window measured in MSS-sized segments.

.. figure:: /protocols/figures/tcp-congestion-regular.*
   :align: center
   :scale: 70

   Evolution of the congestion window with regular losses

As the losses are equally spaced, the congestion window always starts at some value (:math:`\frac{W}{2}`), and is incremented by one MSS every round-trip-time until it reaches twice this value (`W`). At this point, a segment is retransmitted and the cycle starts again. If the congestion window is measured in MSS-sized segments, a cycle lasts :math:`\frac{W}{2}` round-trip-times. The bandwidth of the TCP connection is the number of bytes that have been transmitted during a given period of time. During a cycle, the number of segments that are sent on the TCP connection is equal to the area of the yellow trapeze in the figure. Its area is thus :

 :math:`area=(\frac{W}{2})^2 + \frac{1}{2} \times (\frac{W}{2})^2 = \frac{3 \times W^2}{8}`

However, given the regular losses that we consider, the number of segments that are sent between two losses (i.e. during a cycle) is by definition equal to :math:`\frac{1}{p}`. Thus, :math:`W=\sqrt{\frac{8}{3 \times p}}=\frac{k}{\sqrt{p}}`. The throughput (in bytes per second) of the TCP connection is equal to the number of segments transmitted divided by the duration of the cycle :

 :math:`Throughput=\frac{area \times MSS}{time} = \frac{ \frac{3 \times W^2}{8}}{\frac{W}{2} \times rtt}`
 or, after having eliminated `W`, :math:`Throughput=\sqrt{\frac{3}{2}} \times \frac{MSS}{rtt \times \sqrt{p}}`


More detailed models and the analysis of simulations have shown that a first order model of the TCP throughput when losses occur was :math:`Throughput \approx \frac{k \times MSS}{rtt \times \sqrt{p}}`. This is an important result which shows that :

 - TCP connections with a small round-trip-time can achieve a higher throughput than TCP connections having a longer round-trip-time when losses occur. This implies that the TCP congestion control scheme is not completely fair since it favors the connections that have the shorter round-trip-times.
 - TCP connections that use a large MSS can achieve a higher throughput that the TCP connections that use a shorter MSS. This creates another source of unfairness between TCP connections. However, it should be noted that today most hosts are using almost the same MSS, roughly 1460 bytes.

In general, the maximum throughput that can be achieved by a TCP connection depends on its maximum window size and the round-trip-time if there are no losses. If there are losses, it depends on the MSS, the round-trip-time and the loss ratio.

 :math:`Throughput<\min(\frac{window}{rtt},\frac{k \times MSS}{rtt \times \sqrt{p}})`


The CUBIC congestion control scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. spelling:word-list::

   rtt

The NewReno congestion control scheme has historically been the dominant and the standard TCP congestion control scheme. It works well in networks having a small round-trip-time or a low bandwidth*delay product. In networks with a high bandwidth*delay product, a single packet loss can force a TCP sender to spend a lot of time in congestion avoidance. Since NewReno advances its congestion window by one MSS every round-trip-time, it can spend a long time in congestion avoidance before reaching a congestion window that is large enough to fully use the network. Furthermore, NewReno favors connections with a small round-trip-time compared to connections with a longer round-trip-time as shown in the previous section.

Internet researchers have proposed a wide range of congestion control schemes. During the last decade, the CUBIC congestion control scheme has emerged has the standard congestion control scheme. It has been adopted by key TCP implementations and is defined in :rfc:`9438`. 

.. note:: The TCP congestion control zoo

 The first TCP congestion control scheme was proposed by `Van Jacobson`_ in [Jacobson1988]_. In addition to writing the scientific paper, `Van Jacobson`_ also implemented the slow-start and congestion avoidance schemes in release 4.3 `Tahoe` of the BSD Unix distributed by the University of Berkeley. Later, he improved the congestion control by adding the fast retransmit and the fast recovery mechanisms in the `Reno` release of 4.3 BSD Unix. Since then, many researchers have proposed, simulated and implemented modifications to the TCP congestion control scheme. Some of these modifications are still used today, e.g. :

  - `NewReno` (:rfc:`3782`), which was proposed as an improvement of the fast recovery mechanism in the `Reno` implementation.
  - `TCP Vegas`, which uses changes in the round-trip-time to estimate congestion in order to avoid it [BOP1994]_. This is one of the examples of the delay-based congestion control algorithms. A Vegas sender continuously measures the evolution of the round-trip-time and slows down when the round-trip-time increases significantly. This enables Vegas to prevent congestion when used alone. Unfortunately, if Vegas senders compete with more aggressive TCP congestion control schemes that only react to losses, Vegas senders may have difficulties to use their fair share of the available bandwidth.
  - `CUBIC`, which was designed for high bandwidth links and is the default congestion control scheme in Linux since the Linux 2.6.19 kernel [HRX2008]_. It is now used by several operating systems and is becoming the default congestion control scheme :rfc:`8312`. A key difference between CUBIC and the TCP congestion control scheme described in this chapter is that CUBIC is much more aggressive when probing the network. Instead of relying on additive increase after a fast recovery, a CUBIC sender adjusts its congestion by using a cubic function. Thanks to this function, the congestion windows grows faster. This is particularly important in high-bandwidth delay networks.
  - `BBR`, which is being developed by Google researchers and is included in recent Linux kernels [CCG+2016]_. BBR periodically estimates the available bandwidth and the round-trip-times. To adapt to changes in network conditions, BBR regularly tries to send at 1.25 times the current bandwidth. This enables BBR senders to probe the network, but can also cause large amount of losses. Recent scientific articles indicate that BBR is unfair to other congestion control schemes in specific conditions [WMSS2019]_.

 A wide range of congestion control schemes have been proposed in the scientific literature and several of them have been widely deployed. A detailed comparison of these congestion control schemes is outside the scope of this chapter. A recent survey paper describing many of the implemented TCP congestion control schemes may be found in [TKU2019]_.


The CUBIC congestion control scheme was designed with three [#fcubic]_ main principles in mind:

 1. CUBIC increases its congestion window by using both  the concave and convex parts of a cubic function
 2. CUBIC achieves linear bandwidth sharing among flows with different round-trip-times
 3. CUBIC sets is multiplicative window decrease factor in order to balance scalability and efficiency


CUBIC adjusts the congestion window based on the congestion observed on the path. For this, CUBIC uses a cubic function as illustrated below. Compared with the slow-start and congestion avoidance phases of NewReno, the cubic function has several benefits. After having experienced congestion, it remembers the congestion window size that caused congestion and reduces its congestion window to allow the router buffers to drain. After that, it needs to quickly increase its congestion window to be able to fully utilize the network. This is the role of the concave part of the cubic function. It quickly increases the congestion window until reaching the previous value of the congestion window. This is the plateau of the cubic function. The sender hence quicly transmits at a rate that previously caused congestion. Thanks to the plateau of the cubic function, it does not change its transmission rate quickly. After having transmitted at this rate for several round-trip-times without congestion, the sender starts to increase its congestion window using the convex part of the cubic function. This increase is much faster than NewReno's congestion avoidance and allows CUBIC to quickly utilize the available bandwidth. This results in a much higher network utilization than using NewReno. 
    
    
.. tikz:: The concave and convex parts of a cubic function

   \draw[color=red,domain=1:4,variable=\x]    plot (\x,{0.1*(.4*(\x-5)^3)+1})       node[below] {concave};
   \draw[color=blue,domain=4:6,variable=\x]    plot (\x,{0.1*(.4*(\x-5)^3)+1})       node[left] {};
   \draw[color=green,domain=6:9,variable=\x]    plot (\x,{0.1*(.4*(\x-5)^3)+1})       node[left] {convex};     


The parameters of the cubic function can be adjusted to have a faster ramp-up or a longer plateau. This results in a compromise between stability and faster utilization of available network resources, but at the risk of causing more congestion.

The cubic function allows to adjust the congestion window. It is used when an acknowledgment is received and depends on the delay since the previous congestion event. With CUBIC, two flows that share a single bottleneck link will have similar congestion windows. Since their throughput will be :math:`\frac{cwnd}{rtt}`, the flow with a lower rtt will achieve a higher throughput. 

NewReno halves its congestion window at each congestion event. CUBIC also uses a multiplicative decrease when it detects congestion, but using a factor of :math:`0.7` instead of :math:`0.5`. This provides a better balance between scalability and convergence speed than NewReno.

A CUBIC implementation uses the following function to increase its congestion window upon reception of an acknowledgment: :math:`W_{cubic}(t)= C \times (t-K)^3 + W_{max}`. In this function, :math:`t` is the delay between now and the time of the previous congestion event that marks the start of the current congestion avoidance period. :math:`K` is the time period required for the cubic function to increase the congestion window to reach :math:`W_{max}`. :math:`W_{max}` is the congestion window that caused the last congestion event. It corresponds to the plateau of the cubic function. CUBIC uses :math:`W_{cubic}(t)` to compute a target value of the congestion window after one RTT where RTT is the smoothed value of the measured round-trip-time. When a CUBIC sender receives an acknowledgment, it computes :math:`target=W_{cubic}(t+RTT)` and increments :math:`cwnd` by :math:`\frac{target-cwnd}{cwnd}`.

If a CUBIC sender detects congestion, it remembers the current value of :math:`cwnd` as :math:`W_{max}`, sets :math:`ssthresh=cwnd \times 0.7` and sets :math:`cwnd=max(ssthresh,2)`. This is the multiplicative decrease part of CUBIC [#cubicdec]_.

The CUBIC specification recommends values for the :math:`C` and :math:`K` parameters of the cubic function. :math:`C` should be set to 0.4 based on various studies and simulation results. :math:`K` is computed as :math:`K=\sqrt[3]{\frac{W_{max}-cwnd_{epoch}}{C}}` where :math:`cwnd_{epoch}` is the value of the congestion window at the beginning of the current congestion avoidance stage.


We can now observe the evolution of the congestion window with CUBIC. Let us start with an initial congestion window of 10 segments and assume that one of these segments was lost. CUBIC sets its :math:`cwnd` to :math:`0.7 \times 10 = 7` segments. Since :math:`W_{max}=10`, it computes :math:`K=\sqrt[3]{\frac{10-7}{0.4}}=1.96`. When the second congestion event occurs, it updates :math:`W_{max}`, recomputes :math:`K` and starts a new cubic curve. The curve allows it to quickly reach the plateau, but it stays there for several round-trip-times. As there is no congestion during this plateau, it moves to the convex part of the curve and quickly increases the congestion window to efficiently utilize the available network resources.


.. tikz:: Observing the evolution of :math:`cwnd` on a CUBIC connection

    
   \draw[->] (-0.2,0) -- (9,0) node[below] {$t$};
   \draw[->] (0,-0.2) -- (0,4) node[above] {$cwnd$};

   \draw[color=red,domain=0:4]   plot (\x,{0.2*(0.4*((\x-1.957)^3)+10)}) node[left] {};  
   \draw[->,dashed] (4,0.2*20) -- (4,0.2*16) node [below] {fast retransmit};
   \draw[color=red,domain=4:9]   plot (\x,{0.2*(0.4*(((\x-4)-2)^3)+10)}) ;
	  

  

At this point, it is interesting to explore the evolution of the congestion window computed by a CUBIC sender and compare it with the congestion window that a NewReno sender would compute. For simplicity, we ignore the beginning of the connection and assume that both NewReno and CUBIC have reached a :math:`cwnd` of 10 MSS sized segments. At this time a congestion occurs. NewReno sets its :math:`cwnd` to 5 segments and starts congestion avoidance. CUBIC sets its :math:`cwnd` to 7 segments. Since :math:`W_{max}=10`, it computes :math:`K=\sqrt[3]{\frac{10-7}{0.4}}=1.96`. The congestion window of the CUBIC connection is slightly above the congestion window of the NewReno connection, but then it grows much faster when it enters the convex region. This enables CUBIC to utilize network resources much faster than NewReno.


.. tikz:: Comparing the evolution of the congestion window using CUBIC and NewReno


   \draw[->] (-0.2,0) -- (7,0) node[below] {$t$};
   \draw[->] (0,-0.2) -- (0,7) node[above] {$cwnd$};
   \draw[color=blue,domain=0:6]   plot (\x,{0.2*(5+\x)})  node[above] {NewReno};
   \draw[color=red,domain=0:6]   plot (\x,{0.2*(0.4*((\x-1.957)^3)+10)}) node[above] {CUBIC};  
   \draw[-,dashed,color=red] (0,0.2*5) -- (2,0.2*5) node[below] {threshold};  
   \draw[->,dashed]  (0.05,0.2*16) node [right] {fast retransmit} -- (0.05,0.2*10) ;
	  


Mathematical models of the CUBIC congestion control scheme have also been developed. :rfc:`9438` uses a similar deterministic loss model as the one we used earlier. With a multiplicative decrease factor set to :math:`0.7`, this model computes an average congestion window of :math:`\sqrt[4]{\frac{C*3.7}{1.2}} \times \frac{\sqrt[4]{rtt^3}}{\sqrt[4]{p^3}}`. 
   

.. rubric:: Footnotes


.. [#fwrap] In this pseudo-code, we assume that TCP uses unlimited sequence and acknowledgment numbers. Furthermore, we do not detail how the `cwnd` is adjusted after the retransmission of the lost segment by fast retransmit. Additional details may be found in :rfc:`5681`.

.. [#fprivate] In enterprise networks or datacenters, the situation is different since a single company typically controls all the sources and all the routers. In such networks it is possible to ensure that all hosts and routers have been upgraded before turning on ECN on the routers.

.. [#fecnnonce] With the ECT bit, the deployment issue with ECN is solved provided that all sources cooperate. If some sources do not support ECN but still set the ECT bit in the packets that they sent, they will have an unfair advantage over the sources that correctly react to packet markings. Several solutions have been proposed to deal with this problem :rfc:`3540`, but they are outside the scope of this book.

.. [#fslot] The buffers of a router can be implemented as variable or fixed-length slots. If the router uses variable length slots to store the queued packets, then the occupancy is usually measured in bytes. Some routers have use fixed-length slots with each slot large enough to store a maximum-length packet. In this case, the buffer occupancy is measured in packets.

.. [#fcubic] :rfc:`9438` lists four design principles. In addition to the three that we cover in this chapter, :rfc:`9438` also requires fairness with connections using the old NewReno congestion scheme. Since CUBIC is now widely deployed, we ignore this fourth principle.

.. [#cubicdec] This is a simplified version of this multiplicative decrease. Additional details are provided in :rfc:`9438`.
	     
.. include:: /links.rst
