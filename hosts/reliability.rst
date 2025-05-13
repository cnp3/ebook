.. Copyright |copy| 2013 by Olivier Bonaventure
.. Some portions of this text come from the first edition of this e-book
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by-sa/3.0/>`_



   
A reliable transport protocol
=============================

Recovering from transmission errors
-----------------------------------

In this section, we develop a reliable datalink protocol running above the physical layer service. To design this protocol, we first assume that the physical layer provides a perfect service. We will then develop solutions to recover from the transmission errors.

The datalink layer is designed to send and receive frames on behalf of a user. We model these interactions by using the `DATA.req` and `DATA.ind` primitives. However, to simplify the presentation and to avoid confusion between a `DATA.req` primitive issued by the user of the datalink layer entity, and a `DATA.req` issued by the datalink layer entity itself, we will use the following terminology :

 - the interactions between the user and the datalink layer entity are represented by using the classical `DATA.req` and the `DATA.ind` primitives
 - the interactions between the datalink layer entity and the framing sub-layer are represented by using `send` instead of `DATA.req` and `recvd` instead of `DATA.ind`

When running on top of a perfect framing sub-layer, a datalink entity can simply issue a `send(SDU)` upon arrival of a `DATA.req(SDU)` [#fsdu]_. Similarly, the receiver issues a `DATA.ind(SDU)` upon receipt of a `recvd(SDU)`. Such a simple protocol is sufficient when a single SDU is sent. This is illustrated in the figure below.


  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(SDU)" ] ,
      b>>c [ label = "Frame(SDU)", arcskip="1"];
      c=>d [ label = "DATA.ind(SDU)" ];





Unfortunately, this is not always sufficient to ensure a reliable delivery of the SDUs. Consider the case where a client sends tens of SDUs to a server. If the server is faster than the client, it will be able to receive and process all the frames sent by the client and deliver their content to its user. However, if the server is slower than the client, problems may arise. The datalink entity contains buffers to store SDUs that have been received as a `Data.request` but have not yet been sent. If the application is faster than the physical link, the buffer may become full. At this point, the operating system suspends the application to let the datalink entity empty its transmission queue. The datalink entity also uses a buffer to store the received frames that have not yet been processed by the application. If the application is slow to process the data, this buffer may overflow and the datalink entity will not able to accept any additional frame. The buffers of the datalink entity have a limited size and if they overflow, the arriving frames will be discarded, even if they are correct.

To solve this problem, a reliable protocol must include a feedback mechanism that allows the receiver to inform the sender that it has processed a frame and that another one can be sent. This feedback is required even though there are no transmission errors. To include such a feedback, our reliable protocol must process two types of frames :

 - data frames carrying a SDU
 - control frames carrying an acknowledgment indicating that the previous frames was correctly processed

These two types of frames can be distinguished by dividing the frame in two parts :

 - the `header` that contains one bit set to `0` in data frames and set to `1` in control frames
 - the payload that contains the SDU supplied by the application

The datalink entity can then be modeled as a finite state machine, containing two states for the receiver and two states for the sender. The figure below provides a graphical representation of this state machine with the sender above and the receiver below.

   .. tikz:: Finite state machines of the simplest reliable protocol (sender above, receiver below)
      :libs: positioning, matrix, automata, arrows

      \tikzstyle{arrow} = [thick,->,>=stealth,font=\small]
      \tikzstyle{every state}=[font=\small, align=center, node distance=5em]
      \node[initial, state] (SW) {Wait\\for\\{\color{blue}SDU}};
      \node[state, right=of SW] (SO) {Wait\\for\\OK};
      \path[arrow] (SW) edge [bend left] node[midway, above] {\begin{tabular}{c}
         Data.req({\color{blue}SDU}) \\
         \hline
         \texttt{send({\color{red}D({\color{blue}SDU})})} \\
      \end{tabular}} (SO)
      (SO) edge [bend left] node [midway, below] {\begin{tabular}{c}
         \texttt{recvd({\color{red}C(OK)})} \\
         \hline
         - \\
      \end{tabular}} (SW);

      \node[initial, state, below=5em of SW] (RW) {Wait\\for\\frame};
      \node[state, right=of RW] (RP) {Process\\{\color{blue}SDU}};
      \path[arrow] (RW) edge [bend left] node[midway, above] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D({\color{blue}SDU})})} \\
         \hline
         Data.ind({\color{blue}SDU}) \\
      \end{tabular}} (RP)
      (RP) edge [bend left] node [midway, below] {\begin{tabular}{c}
         - \\
         \hline
         \texttt{send({\color{red}C(OK)})} \\
      \end{tabular}} (RW);


The above FSM shows that the sender has to wait for an acknowledgment from the receiver before being able to transmit the next SDU.  The figure below illustrates the exchange of a few frames between two hosts.

  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(a)"], b>>c [ label = "D(a)", arcskip="1"];
      c=>d [ label = "DATA.ind(a)" ],c>>b [label= "C(OK)", arcskip="1"];
      |||;
      a=>b [ label = "DATA.req(b)" ], b>>c [ label = "D(b)",arcskip="1"];
      c=>d [ label = "DATA.ind(b)" ], c>>b [label= "C(OK)", arcskip="1"];
      |||;



.. note:: Services and protocols

  An important aspect to understand before studying computer networks is the difference between a *service* and a *protocol*. For this, it is useful to start with real world examples. The traditional Post provides a service where a postman delivers letters to recipients. The Post precisely defines which types of letters (size, weight, etc) can be delivered by using the Standard Mail service. Furthermore, the format of the envelope is specified (position of the sender and recipient addresses, position of the stamp). Someone who wants to send a letter must either place the letter at a Post Office or inside one of the dedicated mailboxes. The letter will then be collected and delivered to its final recipient. Note that for the regular service the Post usually does not guarantee the delivery of each particular letter. Some letters may be lost, and some letters are delivered to the wrong mailbox. If a letter is important, then the sender can use the registered service to ensure that the letter will be delivered to its recipient. Some Post services also provide an acknowledged service or an express mail service that is faster than the regular service.




.. The `Datalink layer` builds on the service provided by the underlying physical layer. The `Datalink layer` allows two hosts that are directly connected through the physical layer to exchange information. The unit of information exchanged between two entities in the `Datalink layer` is a frame. A frame is a finite sequence of bits. Some `Datalink layers` use variable-length frames while others only use fixed-length frames. Some `Datalink layers` provide a connection-oriented service while others provide a connectionless service. Some `Datalink layers` provide reliable delivery while others do not guarantee the correct delivery of the information.

.. An important point to note about the `Datalink layer` is that although the figure below indicates that two entities of the `Datalink layer` exchange frames directly, in reality this is slightly different. When the `Datalink layer` entity on the left needs to transmit a frame, it issues as many `Data.request` primitives to the underlying `physical layer` as there are bits in the frame. The physical layer will then convert the sequence of bits in an electromagnetic or optical signal that will be sent over the physical medium. The `physical layer` on the right hand side of the figure will decode the received signal, recover the bits and issue the corresponding `Data.indication` primitives to its `Datalink layer` entity. If there are no transmission errors, this entity will receive the frame sent earlier.

.. The datalink layer uses the service provided by the physical layer. Although there are many different implementations of the physical layer from a technological perspective, they all provide a service that enables the datalink layer to send and receive bits between directly connected devices. The datalink layer receives packets from the network layer. Two datalink layer entities exchange `frames`. As explained in the previous chapter, most datalink layer technologies impose limitations on the size of the frames. Some technologies only impose a maximum frame size, others enforce both minimum and maximum frames sizes and finally some technologies only support a single frame size. In the latter case, the datalink layer will usually include an adaptation sub-layer to allow the network layer to send and receive variable-length packets. This adaptation layer may include fragmentation and reassembly mechanisms.

.. alternating bit


Reliable data transfer on top of an imperfect link
--------------------------------------------------

The datalink layer must deal with the transmission errors. In practice, we mainly have to deal with two types of errors in the datalink layer :

 - Frames can be corrupted by transmission errors
 - Frames can be lost or unexpected frames can appear


A first glance, loosing frames might seem strange on a single link. However, if we take framing into account, transmission errors can affect the frame delineation mechanism and make the frame unreadable. For the same reason, a receiver could receive two (likely invalid) frames after a sender has transmitted a single frame.

To deal with these types of imperfections, reliable protocols rely on different types of mechanisms. The first problem is transmission errors. Data transmission on a physical link can be affected by the following errors :

 - random isolated errors where the value of a single bit has been modified due to a transmission error
 - random burst errors where the values of `n` consecutive bits have been changed due to transmission errors
 - random bit creations and random bit removals where bits have been added or removed due to transmission errors

The only solution to protect against transmission errors is to add redundancy to the frames that are sent. `Information Theory` defines two mechanisms that can be used to transmit information over a transmission channel affected by random errors. These two mechanisms add redundancy to the transmitted information, to allow the receiver to detect or sometimes even correct transmission errors. A detailed discussion of these mechanisms is outside the scope of this chapter, but it is useful to consider a simple mechanism to understand its operation and its limitations.

`Information theory` defines `coding schemes`. There are different types of coding schemes, but let us focus on coding schemes that operate on binary strings. A coding scheme is a function that maps information encoded as a string of `m` bits into a string of `n` bits. The simplest coding scheme is the (even) parity coding. This coding scheme takes an `m` bits source string and produces an `m+1` bits coded string where the first `m` bits of the coded string are the bits of the source string and the last bit of the coded string is chosen such that the coded string will always contain an even number of bits set to `1`. For example :

 - `1001` is encoded as `10010`
 - `1101` is encoded as `11011`

This parity scheme has been used in some RAMs as well as to encode characters sent over a serial line. It is easy to show that this coding scheme allows the receiver to detect a single transmission error, but it cannot correct it. However, if two or more bits are in error, the receiver may not always be able to detect the error.

Some coding schemes allow the receiver to correct some transmission errors. For example, consider the coding scheme that encodes each source bit as follows :

 - `1` is encoded as `111`
 - `0` is encoded as `000`

For example, consider a sender that sends `111`. If there is one bit in error, the receiver could receive `011` or `101` or `110`. In these three cases, the receiver will decode the received bit pattern as a `1` since it contains a majority of bits set to `1`. If there are two bits in error, the receiver will not be able anymore to recover from the transmission error.

This simple coding scheme forces the sender to transmit three bits for each source bit. However, it allows the receiver to correct single bit errors. More advanced coding systems that allow recovering from errors are used in several types of physical layers.

Besides framing, datalink layers also include mechanisms to detect and sometimes even recover from transmission errors. To allow a receiver to notice transmission errors, a sender must add some redundant information as an `error detection` code to the frame sent. This `error detection` code is computed by the sender on the frame that it transmits. When the receiver receives a frame with an error detection code, it recomputes it and verifies whether the received `error detection code` matches the computed `error detection code`. If they match, the frame is considered to be valid. Many error detection schemes exist and entire books have been written on the subject. A detailed discussion of these techniques is outside the scope of this book, and we will only discuss some examples to illustrate the key principles.

To understand `error detection codes`, let us consider two devices that exchange bit strings containing `N` bits. To allow the receiver to detect a transmission error, the sender converts each string of `N` bits into a string of `N+r` bits. Usually, the `r` redundant bits are added at the beginning or the end of the transmitted bit string, but some techniques interleave redundant bits with the original bits. An `error detection code` can be defined as a function that computes the `r` redundant bits corresponding to each string of `N` bits. The simplest error detection code is the parity bit. There are two types of parity schemes : even and odd parity. With the `even` (resp. `odd`) parity scheme, the redundant bit is chosen so that an even (resp. odd) number of bits are set to `1` in the transmitted bit string of `N+r` bits. The receiver can easily recompute the parity of each received bit string and discard the strings with an invalid parity. The parity scheme is often used when 7-bit characters are exchanged. In this case, the eighth bit is often a parity bit. The table below shows the parity bits that are computed for bit strings containing three bits.

  ====================    ==========     ===========
  3 bits string           Odd parity     Even parity
  ====================    ==========     ===========
  000	     	              1              0
  001                     0              1
  010                     0              1
  100                     0              1
  111                     0              1
  110	     	              1              0
  101	     	              1              0
  011	     	              1              0
  ====================    ==========     ===========

The parity bit allows a receiver to detect transmission errors that have affected a single bit among the transmitted `N+r` bits. If there are two or more bits in error, the receiver may not necessarily be able to detect the transmission error. More powerful error detection schemes have been defined. The Cyclical Redundancy Checks (CRC) are widely used in datalink layer protocols. An N-bits CRC can detect all transmission errors affecting a burst of less than N bits in the transmitted frame and all transmission errors that affect an odd number of bits. Additional details about CRCs may be found in [Williams1993]_.

It is also possible to design a code that allows the receiver to correct transmission errors. The simplest `error correction code` is the triple modular redundancy (TMR). To transmit a bit set to `1` (resp. `0`), the sender transmits `111` (resp. `000`). When there are no transmission errors, the receiver can decode `111` as `1`. If transmission errors have affected a single bit, the receiver performs majority voting as shown in the table below. This scheme allows the receiver to correct all transmission errors that affect a single bit.

  ====================    =============
  Received bits           Decoded bit
  ====================    =============
	 000	     		0
	 001			0
	 010			0
	 100			0
	 111			1
	 110			1
	 101			1
	 011			1
  ====================    =============

Other more powerful error correction codes have been proposed and are used in some applications. The `Hamming Code <https://en.wikipedia.org/wiki/Hamming_code>`_ is a clever combination of parity bits that provides error detection and correction capabilities.


Reliable protocols use error detection schemes, but none of the widely used reliable protocols rely on error correction schemes. To detect errors, a frame is usually divided into two parts :

 - a `header` that contains the fields used by the reliable protocol to ensure reliable delivery. The header contains a checksum or Cyclical Redundancy Check (CRC) [Williams1993]_ that is used to detect transmission errors
 - a `payload` that contains the user data

Some headers also include a `length` field, which indicates the total length of the frame or the length of the payload.

The simplest error detection scheme is the checksum. A checksum is basically an arithmetic sum of all the bytes that a frame is composed of. There are different types of checksums. For example, an eight bit checksum can be computed as the arithmetic sum of all the bytes of (both the header and trailer of) the frame. The checksum is computed by the sender before sending the frame and the receiver verifies the checksum upon frame reception. The receiver discards frames received with an invalid checksum. Checksums can be easily implemented in software, but their error detection capabilities are limited. Cyclical Redundancy Checks (CRC) have better error detection capabilities [SGP98]_, but require more CPU when implemented in software.

.. spelling:word-list::

   png

.. note:: Checksums, CRCs,...

   Most of the protocols in the TCP/IP protocol suite rely on the simple Internet checksum in order to verify that a received packet has not been affected by transmission errors. Despite its popularity and ease of implementation, the Internet checksum is not the only available checksum mechanism. Cyclical Redundancy Checks (CRC_) are very powerful error detection schemes that are used notably on disks, by many datalink layer protocols and file formats such as ``zip`` or ``png``. They can easily be implemented efficiently in hardware and have better error-detection capabilities than the Internet checksum [SGP98]_ . However, CRCs are sometimes considered to be too CPU-intensive for software implementations and other checksum mechanisms are preferred. The TCP/IP community chose the Internet checksum, the OSI community chose the Fletcher checksum [Sklower89]_. Nowadays there are efficient techniques to quickly compute CRCs in software [Feldmeier95]_.

.. , the SCTP protocol initially chose the Adler-32 checksum but replaced it recently with a CRC (see :rfc:`3309`).

.. CRC, checksum, fletcher, crc-32, Internet checksum
.. real checksum http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.8520
.. do not invent your own checksum, use existing ones
.. implementations can be optimised by using table lookups
.. crc : https://en.wikipedia.org/wiki/Cyclic_redundancy_check
.. tcp offload engine http://www.10gea.org/tcp-ip-offload-engine-toe.htm
.. stcp used Adler-32 but it now uses CRC :rfc:`3309`

.. The second imperfection of the network layer is that frames may be lost. As we will see later, the main cause of packet losses in the network layer is the lack of buffers in intermediate routers.

Since the receiver sends an acknowledgment after having received each data frame, the simplest solution to deal with losses is to use a retransmission timer. When the sender sends a frame, it starts a retransmission timer. The value of this retransmission timer should be larger than the `round-trip-time`, i.e. the delay between the transmission of a data frame and the reception of the corresponding acknowledgment. When the retransmission timer expires, the sender assumes that the data frame has been lost and retransmits it. This is illustrated in the figure below.


   .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(a)\nstart timer" ] ,
      b>>c [ label = "D(a)", arcskip="1"];
      c=>d [ label = "DATA.ind(a)" ];
      c>>b [label= "C(OK)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;
      a=>b [ label = "DATA.req(b)\nstart timer" ] ,
      b-x c [ label = "D(b)", arcskip="1", linecolour=red];
      |||;
      a=>b [ linecolour=white, label = "timer expires" ] ,
      b>>c [ label = "D(b)", arcskip="1"];
      c=>d [ label = "DATA.ind(b)" ];
      c>>b [label= "C(OK)", arcskip="1"];
      |||;


.. inginious:: q-rel-delay1



Unfortunately, retransmission timers alone are not sufficient to recover from losses. Let us consider, as an example, the situation depicted below where an acknowledgment is lost. In this case, the sender retransmits the data frame that has not been acknowledged. However, as illustrated in the figure below, the receiver considers the retransmission as a new frame whose payload must be delivered to its user.

   .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(a)\nstart timer" ] ,
      b>>c [ label = "D(a)", arcskip="1"];
      c=>d [ label = "DATA.ind(a)" ];
      c>>b [label= "C(OK)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;
      a=>b [ label = "DATA.req(b)\nstart timer" ] ,
      b>>c [ label = "D(b)", arcskip="1"];
      c=>d [ label = "DATA.ind(b)" ];
      c-x b [label= "C(OK)", linecolour=red, arcskip="1"];
      |||;
      a=>b [ linecolour=white, label = "timer expires" ] ,
      b>>c [ label = "D(b)", arcskip="1"];
      c=>d [ label = "DATA.ind(b) !!!!!", linecolour=red ];
      c>>b [label= "C(OK)", arcskip="1"];
      |||;



.. index:: sequence number

To solve this problem, datalink protocols associate a `sequence number` to each data frame. This `sequence number` is one of the fields found in the header of data frames. We use the notation `D(x,...)` to indicate a data frame whose sequence number field is set to value `x`. The acknowledgments also contain a sequence number indicating the data frames that it is acknowledging. We use `OKx` to indicate an acknowledgment frame that confirms the reception of `D(x,...)`. The sequence number is encoded as a bit string of fixed length. The simplest reliable protocol is the Alternating Bit Protocol (ABP).

.. index:: Alternating Bit Protocol

The Alternating Bit Protocol uses a single bit to encode the sequence number. It can be implemented easily. The sender (resp. the receiver) only require a four-state (resp. three-state) Finite State Machine.

   .. tikz:: Alternating bit protocol: Sender FSM
      :libs: positioning, matrix, automata, arrows

      \tikzstyle{arrow} = [thick,->,>=stealth,font=\small]
      \tikzstyle{every state}=[font=\small, align=center, node distance=5em]
      \node[initial, state] (WD0) {Wait\\for\\{\color{red}D(0,...)}};
      \node[state, right=of WD0] (WC0) {Wait\\for\\{\color{red}C(OK0)}};
      \node[state, below=of WC0] (WD1) {Wait\\for\\{\color{red}D(1,...)}};
      \node[state, below=of WD0] (WC1) {Wait\\for\\{\color{red}C(OK1)}};
      \node[font=\small,align=right,right=of WD1] {All corrupted\\frames are\\discarded in all states};


      \path[arrow]
      (WD0) edge [bend left] node[midway, above] {\begin{tabular}{c}
         Data.req({\color{blue}SDU}) \\
         \hline
         \texttt{send({\color{red}D(0,{\color{blue}SDU},CRC)})} \\
         \texttt{start\_timer()} \\
      \end{tabular}} (WC0)
      (WC0) edge [out=90,in=30,looseness=4] node [midway, right] {\begin{tabular}{c}
         \texttt{recvd({\color{red}C(OK1)})} \\
         or timer expires \\
         \hline
         \texttt{send({\color{red}D(0,{\color{blue}SDU},CRC)})} \\
         \texttt{restart\_timer()} \\
      \end{tabular}} (WC0)
      (WC0) edge [bend left] node [midway, right] {\begin{tabular}{c}
         \texttt{recvd({\color{red}C(OK0)})} \\
         \hline
         \texttt{cancel\_timer()} \\
      \end{tabular}} (WD1)
      (WD1) edge [bend left] node[midway, below] {\begin{tabular}{c}
         Data.req({\color{blue}SDU}) \\
         \hline
         \texttt{send({\color{red}D(1,{\color{blue}SDU},CRC)})} \\
         \texttt{start\_timer()} \\
      \end{tabular}} (WC1)
      (WC1) edge [out=270,in=210,looseness=4] node [midway, left] {\begin{tabular}{c}
         \texttt{recvd({\color{red}C(OK0)})} \\
         or timer expires \\
         \hline
         \texttt{send({\color{red}D(1,{\color{blue}SDU},CRC)})} \\
         \texttt{restart\_timer()} \\
      \end{tabular}} (WC1)
      (WC1) edge [bend left] node [midway, left] {\begin{tabular}{c}
         \texttt{recvd({\color{red}C(OK1)})} \\
         \hline
         \texttt{cancel\_timer()} \\
      \end{tabular}} (WD0);


The initial state of the sender is `Wait for D(0,...)`. In this state, the sender waits for a `Data.request`. The first data frame that it sends uses sequence number `0`. After having sent this frame, the sender waits for an `OK0` acknowledgment. A frame is retransmitted upon expiration of the retransmission timer or if an acknowledgment with an incorrect sequence number has been received.

The receiver first waits for `D(0,...)`. If the frame contains a correct `CRC`, it passes the SDU to its user and sends `OK0`. If the frame contains an invalid CRC, it is immediately discarded. Then, the receiver waits for `D(1,...)`. In this state, it may receive a duplicate `D(0,...)` or a data frame with an invalid CRC. In both cases, it returns an `OK0` frame to allow the sender to recover from the possible loss of the previous `OK0` frame.

   .. tikz:: Alternating bit protocol: Receiver FSM
      :libs: positioning, matrix, automata, arrows

      \tikzstyle{arrow} = [thick,->,>=stealth,font=\small]
      \tikzstyle{every state}=[font=\small, align=center, node distance=5em]
      \node[initial, state] (WD0) {Wait\\for\\{\color{red}D(0,...)}};
      \node[state, right=of WD0] (PD0) {Process\\{\color{red}D(0,...)}};
      \node[state, below=of PD0] (WD1) {Wait\\for\\{\color{red}D(1,...)}};
      \node[state, below=of WD0] (PD1) {Process\\{\color{red}D(1,...)}};
      \node[font=\small,align=right,right=of PD0] {All corrupted\\frames are\\discarded in all states};


      \path[arrow]
      (WD0) edge [bend left] node[midway, above] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D(0,{\color{blue}SDU},CRC)})} \\
         \texttt{AND is\_ok({\color{red}CRC},{\color{blue}SDU})} \\
         \hline
         Data.ind({\color{blue}SDU}) \\
      \end{tabular}} (PD0)
      (WD0) edge [out=170,in=110,looseness=4] node [midway, left] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D(1,{\color{blue}SDU},CRC)})} \\
         \texttt{AND is\_ok({\color{red}CRC},{\color{blue}SDU})} \\
         \hline
         \texttt{send({\color{red}C(OK1)})} \\
      \end{tabular}} (WD0)
      (PD0) edge [bend left] node [midway, right] {\begin{tabular}{c}
         - \\
         \hline
         \texttt{send({\color{red}C(OK0)})} \\
      \end{tabular}} (WD1)
      (WD1) edge [bend left] node[midway, below] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D(1,{\color{blue}SDU},CRC)})} \\
         \texttt{AND is\_ok({\color{red}CRC},{\color{blue}SDU})} \\
         \hline
         Data.ind({\color{blue}SDU}) \\
      \end{tabular}} (PD1)
      (WD1) edge [out=0,in=300,looseness=4] node [midway, right] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D(0,{\color{blue}SDU},CRC)})} \\
         \texttt{AND is\_ok({\color{red}CRC},{\color{blue}SDU})} \\
         \hline
         \texttt{send({\color{red}C(OK0)})} \\
      \end{tabular}} (WD1)
      (PD1) edge [bend left] node [midway, left] {\begin{tabular}{c}
         - \\
         \hline
         \texttt{send({\color{red}C(OK1)})} \\
      \end{tabular}} (WD0);


.. note:: Dealing with corrupted frames

 The receiver FSM of the Alternating bit protocol discards all frames that contain an invalid CRC. This is the safest approach since the received frame can be completely different from the frame sent by the remote host. A receiver should not attempt at extracting information from a corrupted frame because it cannot know which portion of the frame has been affected by the error.


The figure below illustrates the operation of the alternating bit protocol.


.. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(a)\nstart timer" ] ,
      b>>c [ label = "D(0,a)", arcskip="1"];
      c=>d [ label = "DATA.ind(a)" ];
      c>>b [label= "C(OK0)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;
      a=>b [ label = "DATA.req(b)\nstart timer" ];
      b>>c [ label = "D(1,b)", arcskip="1"];
      c=>d [ label = "DATA.ind(b)" ];
      c>>b [label= "C(OK1)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;
      a=>b [ label = "DATA.req(c)\nstart timer" ] ,
      b>>c [ label = "D(0,c)", arcskip="1"];
      c=>d [ label = "DATA.ind(c)" ];
      c>>b [label= "C(OK0)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;

The Alternating Bit Protocol can recover from the losses of data or control frames. This is illustrated in the two figures below. The first figure shows the loss of one data frame.

.. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(a)\nstart timer" ] ,
      b>>c [ label = "D(0,a)", arcskip="1"];
      c=>d [ label = "DATA.ind(a)" ];
      c>>b [label= "C(OK0)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;
      a=>b [ label = "DATA.req(b)\nstart timer" ] ,
      b-x c [ label = "D(1,b)", arcskip="1", linecolour=red];
      |||;
      |||;
      a=>b [ linecolour=white, label = "timer expires" ] ,
      b>>c [ label = "D(1,b)", arcskip="1"];
      c=>d [ label = "DATA.ind(b)" ];
      c>>b [label= "C(OK1)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;

The second figure illustrates how the hosts handle the loss of one control frame.

.. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(a)\nstart timer" ] ,
      b>>c [ label = "D(0,a)", arcskip="1"];
      c=>d [ label = "DATA.ind(a)" ];
      c>>b [label= "C(OK0)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];

      |||;
      a=>b [ label = "DATA.req(b)\nstart timer" ] ,
      b>>c [ label = "D(1,b)", arcskip="1"];
      c=>d [ label = "DATA.ind(b)" ];
      c-x b [label= "C(OK1)", linecolour=red, arcskip="1"];
      |||;
      a=>b [ linecolour=white, label = "timer expires" ] ,
      b>>c [ label = "D(1,b)", arcskip="1"];
      c=>d [ label = "Duplicate frame\nignored", textcolour=red, linecolour=white ];
      c>>b [label= "C(OK1)", arcskip="1"];
      b->a [linecolour=white, label="cancel timer"];
      |||;

..
   note:: Random errors versus malicious modifications
   The protocols of the transport layer are designed to recover from the random errors and losses that may occur in the underlying layers. There random errors are caused by
   see [SPMR09]_ for how to recompute a CRC
   Checksums and CRCs should not be confused with hash functions such as MD5 defined in :rfc:`1321` or `SHA-1 <http://www.itl.nist.gov/fipspubs/fip180-1.htm>`_ .


The Alternating Bit Protocol can recover from transmission errors and frame losses. However, it has one important drawback. Consider two hosts that are directly connected by a 50 Kbits/sec satellite link that has a 250 milliseconds propagation delay. If these hosts send 1000 bits frames, then the maximum throughput that can be achieved by the alternating bit protocol is one frame every :math:`20+250+250=520` milliseconds if we ignore the transmission time of the acknowledgment. This is less than 2 Kbits/sec !

.. inginious:: mcq-rel-abp

.. inginious:: q-rel-alt-bit-1

.. inginious:: q-rel-alt-bit-2


Go-back-n and selective repeat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To overcome the performance limitations of the alternating bit protocol, reliable protocols rely on `pipelining`. This technique allows a sender to transmit several consecutive frames without being forced to wait for an acknowledgment after each frame. Each data frame contains a sequence number encoded as an `n` bits field.

.. figure:: /principles/figures/pipelining2.*
   :align: center
   :scale: 70

   Pipelining improves the performance of reliable protocols

`Pipelining` allows the sender to transmit frames at a higher rate. However this higher transmission rate may overload the receiver. In this case, the frames sent by the sender will not be correctly received by their final destination. The reliable protocols that rely on pipelining allow the sender to transmit `W` unacknowledged frames before being forced to wait for an acknowledgment from the receiving entity.

This is implemented by using a `sliding window`. The sliding window is the set of consecutive sequence numbers that the sender can use when transmitting frames without being forced to wait for an acknowledgment. The figure below shows a sliding window containing five frames (`6,7,8,9` and `10`). Two of these sequence numbers (`6` and `7`) have been used to send frames and only three sequence numbers (`8`, `9` and `10`) remain in the sliding window. The sliding window is said to be closed once all sequence numbers contained in the sliding window have been used.

.. figure:: /principles/figures/slidingwin2.*
   :align: center
   :scale: 100

   The sliding window

The figure below illustrates the operation of the sliding window. It uses a sliding window of three frames. The sender can thus transmit three frames before being forced to wait for an acknowledgment. The sliding window moves to the higher sequence numbers upon the reception of each acknowledgment. When the first acknowledgment (`OK0`) is received, it enables the sender to move its sliding window to the right and sequence number `3` becomes available. This sequence number is used later to transmit the frame containing `d`.


.. figure:: /principles/figures/gbnwin.*
   :align: center
   :scale: 60

   Sliding window example


In practice, as the frame header includes an `n` bits field to encode the sequence number, only the sequence numbers between :math:`0` and :math:`2^{n}-1` can be used. This implies that, during a long transfer, the same sequence number will be used for different frames and the sliding window will wrap. This is illustrated in the figure below assuming that `2` bits are used to encode the sequence number in the frame header. Note that upon reception of `OK1`, the sender slides its window and can use sequence number `0` again.


.. figure:: /principles/figures/gbnwinex.*
   :align: center
   :scale: 60

   Utilization of the sliding window with modulo arithmetic

.. index:: go-back-n


Unfortunately, frame losses do not disappear because a reliable protocol uses a sliding window. To recover from losses, a sliding window protocol must define :

 - a heuristic to detect frame losses
 - a `retransmission strategy` to retransmit the lost frames


.. index:: cumulative acknowledgments

The simplest sliding window protocol uses the `go-back-n` recovery. Intuitively, `go-back-n` operates as follows. A `go-back-n` receiver is as simple as possible. It only accepts the frames that arrive in-sequence. A `go-back-n` receiver discards any out-of-sequence frame that it receives. When `go-back-n` receives a data frame, it always returns an acknowledgment containing the sequence number of the last in-sequence frame that it has received. This acknowledgment is said to be `cumulative`. When a `go-back-n` receiver sends an acknowledgment for sequence number `x`, it implicitly acknowledges the reception of all frames whose sequence number is earlier than `x`. A key advantage of these cumulative acknowledgments is that it is easy to recover from the loss of an acknowledgment. Consider for example a `go-back-n` receiver that received frames `1`, `2` and `3`. It sent `OK1`, `OK2` and `OK3`. Unfortunately, `OK1` and `OK2` were lost. Thanks to the cumulative acknowledgments, when the sender receives `OK3`, it knows that all three frames have been correctly received.

The figure below shows the FSM of a simple `go-back-n` receiver. This receiver uses two variables : `lastack` and `next`. `next` is the next expected sequence number and `lastack` the sequence number of the last data frame that has been acknowledged. The receiver only accepts the frame that are received in sequence. `maxseq` is the number of different sequence numbers (:math:`2^n`).


   .. tikz:: Go-back-n: receiver FSM
      :libs: positioning, matrix, automata, arrows

      \tikzstyle{arrow} = [thick,->,>=stealth,font=\small]
      \tikzstyle{every state}=[font=\small, align=center, node distance=12em]
      \node[initial, state] (W) {Wait};
      \node[state, right=of W] (P) {Process\\{\color{blue}SDU}};
      \node[font=\small,align=right,right=of P] {All corrupted\\frames are\\discarded in all states};
      \path[arrow]
      (W) edge [bend left] node[midway, above] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D(next,{\color{blue}SDU},CRC)})} \\
         \texttt{AND is\_ok({\color{red}CRC},{\color{blue}SDU})} \\
         \hline
         Data.ind({\color{blue}SDU}) \\
      \end{tabular}} (P)
      (P) edge [bend left] node [midway, below] {\begin{tabular}{c}
         - \\
         \hline
         \texttt{send({\color{red}C(OK,next,CRC)});} \\
         \texttt{lastack = next;} \\
         \texttt{next = (next + 1) \% maxseq;} \\
      \end{tabular}} (W)
      (W) edge [out=270,in=210,looseness=8] node [midway, left] {\begin{tabular}{c}
         \texttt{recvd({\color{red}D(t != next,{\color{blue}SDU},CRC)})} \\
         \texttt{AND is\_ok({\color{red}CRC},{\color{blue}SDU})} \\
         \hline
         \texttt{discard({\color{blue}SDU});} \\
         \texttt{send({\color{red}C(OK,lastack,CRC)});} \\
      \end{tabular}} (W);


A `go-back-n` sender is also very simple. It uses a sending buffer that can store an entire sliding window of frames [#fsizesliding]_. The frames are sent with increasing sequence numbers (modulo `maxseq`). The sender must wait for an acknowledgment once its sending buffer is full. When a `go-back-n` sender receives an acknowledgment, it removes from the sending buffer all the acknowledged frames and uses a retransmission timer to detect frame losses. A simple `go-back-n` sender maintains one retransmission timer per connection. This timer is started when the first frame is sent. When the `go-back-n sender` receives an acknowledgment, it restarts the retransmission timer only if there are still unacknowledged frames in its sending buffer. When the retransmission timer expires, the `go-back-n` sender assumes that all the unacknowledged frames currently stored in its sending buffer have been lost. It thus retransmits all the unacknowledged frames in the buffer and restarts its retransmission timer.


   .. tikz:: Go-back-n: sender FSM
      :libs: positioning, matrix, automata, arrows

      \tikzstyle{arrow} = [thick,->,>=stealth,font=\small]
      \tikzstyle{every state}=[font=\small, align=center, node distance=5em]
      \node[initial, state] (W) {Wait};
      \node[font=\small,align=right,below right=8em of W] {All corrupted\\frames are\\discarded in all states};
      \path[arrow]
      (W) edge [in=30,out=330,looseness=7] node[midway, right] {\begin{tabular}{l}
         Data.req({\color{blue}SDU}) \\
         \texttt{AND size(buffer) < W} \\
         \hline
         \texttt{if (seq == unack) \{ start\_timer(); \}} \\
         \texttt{buffer.insert(seq, {\color{blue}SDU});} \\
         \texttt{send({\color{red}D(seq,{\color{blue}SDU},CRC)});} \\
         \texttt{seq = (seq + 1) \% maxseq;}\\
      \end{tabular}} (W)
      (W) edge [in=270,out=210,looseness=7] node [midway, below] {\begin{tabular}{l}
         \texttt{recvd({\color{red}C(OK,t,CRC)})} \\
         \texttt{AND is\_crc\_ok({\color{red}C(OK,t,CRC)})} \\
         \hline
         \texttt{buffer.remove\_acked\_frames()}\\
         \texttt{unack = (t + 1) \% maxseq;}\\
         \texttt{if (unack == seq) \{ }\\
         \texttt{    cancel\_timer();}\\
         \texttt{\} else \{ }\\
         \texttt{    restart\_timer();}\\
         \texttt{\} }\\
      \end{tabular}} (W)
      (W) edge [out=150,in=90,looseness=7] node [midway, above] {\begin{tabular}{l}
         timer expires \\
         \hline
         \texttt{for all (i, SDU) in buffer \{ }\\
         \texttt{    send(\color{red}D(i,{\color{blue}SDU},CRC);} \\
         \texttt{\} }\\
         \texttt{restart\_timer();}
      \end{tabular}} (W);


The operation of `go-back-n` is illustrated in the figure below. In this figure, note that upon reception of the out-of-sequence frame `D(2,c)`, the receiver returns a cumulative acknowledgment `C(OK,0)` that acknowledges all the frames that have been received in sequence. The lost frame is retransmitted upon the expiration of the retransmission timer.

.. figure:: /principles/figures/gbnex2.*
   :align: center
   :scale: 70

   Go-back-n : example


The main advantage of `go-back-n` is that it can be easily implemented, and it can also provide good performance when only a few frames are lost. However, when there are many losses, the performance of `go-back-n` quickly drops for two reasons :

 - the `go-back-n` receiver does not accept out-of-sequence frames
 - the `go-back-n` sender retransmits all unacknowledged frames once it has detected a loss


.. inginious:: mcq-rel-gbn

.. index:: selective repeat

`Selective repeat` is a better strategy to recover from losses. Intuitively, `selective repeat` allows the receiver to accept out-of-sequence frames. Furthermore, when a `selective repeat` sender detects losses, it only retransmits the frames that have been lost and not the frames that have already been correctly received.

A `selective repeat` receiver maintains a sliding window of `W` frames and stores in a buffer the out-of-sequence frames that it receives. The figure below shows a five-frame receive window on a receiver that has already received frames `7` and `9`.

.. figure:: /principles/figures/selrepeatwin2.*
   :align: center
   :scale: 70

   The receiving window with selective repeat

A `selective repeat` receiver discards all frames having an invalid CRC, and maintains the variable `lastack` as the sequence number of the last in-sequence frame that it has received. The receiver always includes the value of `lastack` in the acknowledgments that it sends. Some protocols also allow the `selective repeat` receiver to acknowledge the out-of-sequence frames that it has received. This can be done for example by placing the list of the correctly received, but out-of-sequence frames in the acknowledgments together with the `lastack` value.

When a `selective repeat` receiver receives a data frame, it first verifies whether the frame is inside its receiving window. If yes, the frame is placed in the receive buffer. If not, the received frame is discarded and an acknowledgment containing `lastack` is sent to the sender. The receiver then removes all consecutive frames starting at `lastack` (if any) from the receive buffer. The payloads of these frames are delivered to the user, `lastack` and the receiving window are updated, and an acknowledgment acknowledging the last frame received in sequence is sent.

The `selective repeat` sender maintains a sending buffer that can store up to `W` unacknowledged frames. These frames are sent as long as the sending buffer is not full. Several implementations of a `selective repeat` sender are possible. A simple implementation associates one retransmission timer to each frame. The timer is started when the frame is sent and canceled upon reception of an acknowledgment that covers this frame. When a retransmission timer expires, the corresponding frame is retransmitted and this retransmission timer is restarted. When an acknowledgment is received, all the frames that are covered by this acknowledgment are removed from the sending buffer and the sliding window is updated.

The figure below illustrates the operation of `selective repeat` when frames are lost. In this figure, `C(OK,x)` is used to indicate that all frames, up to and including sequence number `x` have been received correctly.

.. figure:: /principles/figures/selrepeat.*
   :align: center
   :scale: 70

   Selective repeat : example

.. index:: selective acknowledgments

Pure cumulative acknowledgments work well with the `go-back-n` strategy. However, with only cumulative acknowledgments a `selective repeat` sender cannot easily determine which frames have been correctly received after a data frame has been lost. For example, in the figure above, the second `C(OK,0)` does not inform explicitly the sender of the reception of `D(2,c)` and the sender could retransmit this frame although it has already been received. A possible solution to improve the performance of `selective repeat` is to provide additional information about the received frames in the acknowledgments that are returned by the receiver. For example, the receiver could add in the returned acknowledgment the list of the sequence numbers of all frames that have already been received. Such acknowledgments are sometimes called `selective acknowledgments`. This is illustrated in the figure above.

.. ..figure:: png/manque
      :align: center
      :scale: 70

..   TODO : SACK Selective repeat : example


In the figure above, when the sender receives `C(OK,0,[2])`, it knows that all frames up to and including `D(0,...)` have been correctly received. It also knows that frame `D(2,...)` has been received and can cancel the retransmission timer associated to this frame. However, this frame should not be removed from the sending buffer before the reception of a cumulative acknowledgment (`C(OK,2)` in the figure above) that covers this frame.

.. inginious:: mcq-rel-sr

.. note:: Maximum window size with `go-back-n` and `selective repeat`

 A reliable protocol that uses `n` bits to encode its sequence number can send up to :math:`2^n` successive frames. However, to ensure a reliable delivery of the frames, `go-back-n` and `selective repeat` cannot use a sending window of :math:`2^n` frames.
 Consider first `go-back-n` and assume that a sender sends :math:`2^n` frames. These frames are received in-sequence by the destination, but all the returned acknowledgments are lost. The sender will retransmit all frames. These frames will all be accepted by the receiver and delivered a second time to the user. It is easy to see that this problem can be avoided if the maximum size of the sending window is :math:`{2^n}-1` frames.
 A similar problem occurs with `selective repeat`. However, as the receiver accepts out-of-sequence frames, a sending window of :math:`{2^n}-1` frames is not sufficient to ensure a reliable delivery. It can be easily shown that to avoid this problem, a `selective repeat` sender cannot use a window that is larger than :math:`\frac{2^n}{2}` frames.


.. `Go-back-n` or `selective repeat` are used to provide a reliable data transfer above an unreliable physical layer service. Until now, we have assumed that the size of the sliding window was fixed for the entire lifetime of the connection. In practice a  layer entity is usually implemented in the operating system and shares memory with other parts of the system. Furthermore, a transport layer entity must support several (possibly hundreds or thousands) of transport connections at the same time. This implies that the memory which can be used to support the sending or the receiving buffer of a transport connection may change during the lifetime of the connection [#fautotune]_ . Thus, a transport protocol must allow the sender and the receiver to adjust their window sizes.

.. To deal with this issue, transport protocols allow the receiver to advertise the current size of its receiving window in all the acknowledgments that it sends. The receiving window advertised by the receiver bounds the size of the sending buffer used by the sender. In practice, the sender maintains two state variables : `swin`, the size of its sending window (that may be adjusted by the system) and `rwin`, the size of the receiving window advertised by the receiver. At any time, the number of unacknowledged frames cannot be larger than :math:`\min(swin,rwin)` [#facklost]_ . The utilization of dynamic windows is illustrated in the figure below.

.. .. figure:: ../../book/transport/svg/transport-fig-039.png
     :align: center
     :scale: 90

      Dynamic receiving window

.. The receiver may adjust its advertised receive window based on its current memory consumption, but also to limit the bandwidth used by the sender. In practice, the receive buffer can also shrink as the application may not able to process the received data quickly enough. In this case, the receive buffer may be completely full and the advertised receive window may shrink to `0`. When the sender receives an acknowledgment with a receive window set to `0`, it is blocked until it receives an acknowledgment with a positive receive window. Unfortunately, as shown in the figure below, the loss of this acknowledgment could cause a deadlock as the sender waits for an acknowledgment while the receiver is waiting for a data frame.

.. .. figure:: ../../book/transport/png/transport-fig-040-c.png
      :align: center
      :scale: 70

      Risk of deadlock with dynamic windows


.. index:: persistence timer

.. To solve this problem, transport protocols rely on a special timer : the `persistence timer`. This timer is started by the sender whenever it receives an acknowledgment advertising a receive window set to `0`. When the timer expires, the sender retransmits an old frame in order to force the receiver to send a new acknowledgment, and hence send the current receive window size.

..
 ..  note:: Negative acknowledgments

.. To conclude our description of the basic mechanisms found in transport protocols, we still need to discuss the impact of segments arriving in the wrong order. If two consecutive segments are reordered, the receiver relies on their sequence numbers to reorder them in its receive buffer. Unfortunately, as transport protocols reuse the same sequence number for different segments, if a segment is delayed for a prolonged period of time, it might still be accepted by the receiver. This is illustrated in the figure below where segment `D(1,b)` is delayed.

..
 .. figure:: png/transport-fig-041-c.png
    :align: center
    :scale: 70

    Ambiguities caused by excessive delays

.. index:: maximum segment lifetime (MSL)

.. To deal with this problem, transport protocols combine two solutions. First, they use 32 bits or more to encode the sequence number in the segment header. This increases the overhead, but also increases the delay between the transmission of two different segments having the same sequence number. Second, transport protocols require the network layer to enforce a `Maximum Segment Lifetime (MSL)`. The network layer must ensure that no packet remains in the network for more than MSL seconds. In the Internet the MSL is assumed [#fmsl]_ to be 2 minutes :rfc:`793`. Note that this limits the maximum bandwidth of a transport protocol. If it uses `n` bits to encode its sequence numbers, then it cannot send more than :math:`2^n` segments every MSL seconds.

.. index:: piggybacking

Reliable protocols often need to send data in both directions. To reduce the overhead caused by the acknowledgments, most reliable protocols use `piggybacking`. Thanks to this technique, a datalink entity can place the acknowledgments and the receive window that it advertises for the opposite direction of the data flow inside the header of the data frames that it sends. The main advantage of piggybacking is that it reduces the overhead as it is not necessary to send a complete frame to carry an acknowledgment. This is illustrated in the figure below where the acknowledgment number is underlined in the data frames. Piggybacking is only used when data flows in both directions. A receiver will generate a pure acknowledgment when it does not send data in the opposite direction as shown in the bottom of the figure.

.. figure:: /principles/figures/piggyback2.*
   :align: center
   :scale: 70

   Piggybacking example


.. inginious:: q-rel-gbn-max

.. inginious:: q-rel-sr-max


               Connection establishment
^^^^^^^^^^^^^^^^^^^^^^^^

Like the connectionless service, the connection-oriented service allows several applications running on a given host to exchange data with other hosts. The port numbers described above for the connectionless service are also used by the connection-oriented service to multiplex several applications. Similarly, connection-oriented protocols use checksums/CRCs to detect transmission errors and discard segments containing an invalid checksum/CRC.

An important difference between the connectionless service and the connection-oriented one is that the transport entities in the latter maintain some state during lifetime of the connection. This state is created when a connection is established and is removed when it is released.

The simplest approach to establish a transport connection would be to define two special control segments : `CR` (Connection Request) and `CA` (Connection Acknowledgment). The `CR` segment is sent by the transport entity that wishes to initiate a connection. If the remote entity wishes to accept the connection, it replies by sending a `CA` segment. The `CR` and `CA` segments contain `port numbers` that allow identifying the communicating applications. The transport connection is considered to be established once the `CA` segment has been received. At that point, data segments can be sent in both directions.


.. msc::

      a1 [label="", linecolour=white],
      a [label="", linecolour=white],
      b [label="Source", linecolour=black],
      z [label="Provider", linecolour=white],
      c [label="Destination", linecolour=black],
      d [label="", linecolour=white],
      d1 [label="", linecolour=white];

      a1=>b [ label = "CONNECT.req" ] ,
      b>>c [ label = "CR", arcskip="1", textcolour=red];
      c=>d1 [ label = "CONNECT.ind" ];

      d1=>c [ label = "CONNECT.resp" ] ,
      c>>b [ label = "CA", arcskip="1", textcolour=red];
      b=>a1 [ label = "CONNECT.conf" ];

      a1=>b [ linecolour=white, textcolour=blue, label = "Connection\nestablished" ] ,
      c=>d1 [ linecolour=white, textcolour=blue, label = "Connection\nestablished" ];


Unfortunately, this scheme is not sufficient given the unreliable network layer. Since the network layer is imperfect, the `CR` or `CA` segments can be lost, delayed, or suffer from transmission errors. To deal with these problems, the control segments must be protected by a CRC or a checksum to detect transmission errors. Furthermore, since the `CA` segment acknowledges the reception of the `CR` segment, the `CR` segment can be protected using a retransmission timer.

Unfortunately, this scheme is not sufficient to ensure the reliability of the transport service. Consider for example a short-lived transport connection where a single, but important transfer (e.g. money transfer from a bank account) is sent. Such a short-lived connection starts with a `CR` segment acknowledged by a `CA` segment, then the data segment is sent, acknowledged and the connection terminates. Unfortunately, as the network layer service is unreliable, delays combined to retransmissions may lead to the situation depicted in the figure below, where a delayed `CR` and data segments from a former connection are accepted by the receiving entity as valid segments, and the corresponding data is delivered to the user. Duplicating SDUs is not acceptable, and the transport protocol must solve this problem.



.. msc::

      a1 [label="", linecolour=white],
      a [label="", linecolour=white],
      b [label="Source", linecolour=black],
      z [label="Provider", linecolour=white],
      c [label="Destination", linecolour=black],
      d [label="", linecolour=white],
      d1 [label="", linecolour=white];

      a1=>b [ label = "CONNECT.req" ] ,
      b>>c [ label = "CR", arcskip="1", textcolour=red];
      c=>d1 [ label = "CONNECT.ind" ];

      d1=>c [ label = "CONNECT.resp" ] ,
      c>>b [ label = "CA", arcskip="1", textcolour=red];
      b=>a1 [ label = "CONNECT.conf" ];

      a1=>b [ linecolour=white, textcolour=blue, label = "First connection\nestablished" ] ,
      c=>d1 [ linecolour=white, textcolour=blue, label = "First connection\nestablished" ];

      a1=>b [ label = "", linecolour=white];

      a1=>b [ linecolour=white, textcolour=red, label = "First connection\nclosed" ] ,
      c=>d1 [ linecolour=white, textcolour=red, label = "First connection\nclosed" ];

      z>>c [ label = "CR", arcskip="1", textcolour=red];
      c=>d1 [ label = "How to detect duplicates ?" ],
      c>>b [ label = "CA", arcskip="1", textcolour=red];
      a1=>b [ label = "", linecolour=white];
      z>>c [ label = "D", arcskip="1"];


.. index:: Maximum Segment Lifetime (MSL), transport clock


To avoid these duplicates, transport protocols require the network layer to bound the `Maximum Segment Lifetime (MSL)`. The organization of the network must guarantee that no segment remains in the network for longer than `MSL` seconds. For example, on today's Internet, `MSL` is expected to be 2 minutes. To avoid duplicate transport connections, transport protocol entities must be able to safely distinguish between a duplicate `CR` segment and a new `CR` segment, without forcing each transport entity to remember all the transport connections that it has established in the past.

A classical solution to avoid remembering the previous transport connections to detect duplicates is to use a clock inside each transport entity. This `transport clock` has the following characteristics :

 - the `transport clock` is implemented as a `k` bits counter and its clock cycle is such that :math:`2^k \times cycle >> MSL`. Furthermore, the `transport clock` counter is incremented every clock cycle and after each connection establishment. This clock is illustrated in the figure below.
 - the `transport clock` must continue to be incremented even if the transport entity stops or reboots

.. figure:: /principles/figures/transport-clock.*
   :align: center
   :scale: 70

   Transport clock


It should be noted that `transport clocks` do not need and usually are not synchronized to the real-time clock. Precisely synchronizing real-time clocks is an interesting problem, but it is outside the scope of this document. See [Mills2006]_ for a detailed discussion on synchronizing the real-time clock.

This `transport clock` can now be combined with an exchange of three segments, called the `three way handshake`, to detect duplicates. This `three way handshake` occurs as follows :

 #. The initiating transport entity sends a `CR` segment. This segment requests the establishment of a transport connection. It contains a port number (not shown in the figure) and a sequence number (`seq=x` in the figure below) whose value is extracted from the `transport clock`. The transmission of the `CR` segment is protected by a retransmission timer.

 #. The remote transport entity processes the `CR` segment and creates state for the connection attempt. At this stage, the remote entity does not yet know whether this is a new connection attempt or a duplicate segment. It returns a `CA` segment that contains an acknowledgment number to confirm the reception of the `CR` segment (`ack=x` in the figure below) and a sequence number (`seq=y` in the figure below) whose value is extracted from its transport clock. At this stage, the connection is not yet established.

 #. The initiating entity receives the `CA` segment. The acknowledgment number of this segment confirms that the remote entity has correctly received the `CR` segment. The transport connection is considered to be established by the initiating entity and the numbering of the data segments starts at sequence number `x`. Before sending data segments, the initiating entity must acknowledge the received `CA` segments by sending another `CA` segment.

 #. The remote entity considers the transport connection to be established after having received the segment that acknowledges its `CA` segment. The numbering of the data segments sent by the remote entity starts at sequence number `y`.

 The three way handshake is illustrated in the figure below.

.. figure:: /principles/figures/transport-twh.*
   :align: center
   :scale: 70

   Three-way handshake

Thanks to the three way handshake, transport entities avoid duplicate transport connections. This is illustrated by considering the three scenarios below.

The first scenario is when the remote entity receives an old `CR` segment. It considers this `CR` segment as a connection establishment attempt and replies by sending a `CA` segment. However, the initiating host cannot match the received `CA` segment with a previous connection attempt. It sends a control segment (`REJECT` in the figure below) to cancel the spurious connection attempt. The remote entity cancels the connection attempt upon reception of this control segment.

.. figure:: /principles/figures/transport-twh-dup.*
   :align: center
   :scale: 70

   Three-way handshake : recovery from a duplicate `CR`

A second scenario is when the initiating entity sends a `CR` segment that does not reach the remote entity and receives a duplicate `CA` segment from a previous connection attempt. This duplicate `CA` segment cannot contain a valid acknowledgment for the `CR` segment as the sequence number of the `CR` segment was extracted from the transport clock of the initiating entity. The `CA` segment is thus rejected and the `CR` segment is retransmitted upon expiration of the retransmission timer.


.. figure:: /principles/figures/transport-twh-dup2.*
   :align: center
   :scale: 70

   Three-way handshake : recovery from a duplicate `CA`

The last scenario is less likely, but it is important to consider it as well. The remote entity receives an old `CR` segment. It notes the connection attempt and acknowledges it by sending a `CA` segment. The initiating entity does not have a matching connection attempt and replies by sending a `REJECT`. Unfortunately, this segment never reaches the remote entity. Instead, the remote entity receives a retransmission of an older `CA` segment that contains the same sequence number as the first `CR` segment. This `CA` segment cannot be accepted by the remote entity as a confirmation of the transport connection as its acknowledgment number cannot have the same value as the sequence number of the first `CA` segment.

.. figure:: /principles/figures/transport-twh-dup3.*
   :align: center
   :scale: 70

   Three-way handshake : recovery from duplicates `CR` and `CA`


Data transfer
^^^^^^^^^^^^^

Now that the transport connection has been established, it can be used to transfer data. To ensure a reliable delivery of the data, the transport protocol will include sliding windows, retransmission timers and `go-back-n` or `selective repeat`. However, we cannot simply reuse the techniques from the datalink because a transport protocol needs to deal with more types of errors than a reliable protocol in datalink layer. The first difference between the two layers is the transport layer must face with more variable delays. In the datalink layer, when two hosts are connected by a link, the transmission delay or the round-trip-time over the link is almost fixed. In a network that can span the globe, the delays and the round-trip-times can vary significantly on a per packet basis. This variability can be caused by two factors. First, packets sent through a network do not necessarily follow the same path to reach their destination. Second, some packets may be queued in the buffers of routers when the load is high and these queuing delays can lead to increased end-to-end delays. A second difference between the datalink layer and the transport layer is that a network does not always deliver packets in sequence. This implies that packets may be reordered by the network. Furthermore, the network may sometimes duplicate packets. The last issue that needs to be dealt with in the transport layer is the transmission of large SDUs. In the datalink layer, reliable protocols transmit small frames. Applications could generate SDUs that are much larger than the maximum size of a packet in the network layer. The transport layer needs to include mechanisms to fragment and reassemble these large SDUs.

To deal with all these characteristics of the network layer, we need to adapt the techniques that we have introduced in the datalink layer.

The first point which is common between the two layers is that both use CRCs or checksums to detect transmission errors. Each segment contains a CRC/checksum which is computed over the entire segment (header and payload) by the sender and inserted in the header. The receiver recomputes the CRC/checksum for each received segment and discards all segments with an invalid CRC.

Reliable transport protocols also use sequence numbers and acknowledgment numbers. While reliable protocols in the datalink layer use one sequence number per frame, reliable transport protocols consider all the data transmitted as a stream of bytes. In these protocols, the sequence number placed in the segment header corresponds to the position of the first byte of the payload in the bytestream. This sequence number allows detecting losses but also enables the receiver to reorder the out-of-sequence segments. This is illustrated in the figure below.

  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(abcde)" ] ,
      b>>c [ arcskip="1", label="1:abcde"];
      c=>d [label="DATA.ind(abcde)"];
      |||;
      a=>b [ label = "DATA.req(fghijkl)" ] ,
      b>>c [ arcskip="1", label="6:fghijkl"];
      c=>d [label="DATA.ind(fghijkl)"];


Using sequence numbers to count bytes has also one advantage when the transport layer needs to fragment SDUs in several segments. The figure below shows the fragmentation of a large SDU in two segments. Upon reception of the segments, the receiver will use the sequence numbers to correctly reorder the data.

  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(abcdefghijkl)" ] ,
      b>>c [ arcskip="1", label="1:abcde"];
      |||;
      b>>c [ arcskip="1", label="6:fghijkl"];
      c=>d [label="DATA.ind(abcdefghijkl)"];


Compared to reliable protocols in the datalink layer, reliable transport protocols encode their sequence numbers using more bits. 32 bits and 64 bits sequence numbers are frequent in the transport layer while some datalink layer protocols encode their sequence numbers in an 8 bits field. This large sequence number space is motivated by two reasons. First, since the sequence number is incremented for each transmitted byte, a single segment may consume one or several thousands of sequence numbers. Second, a reliable transport protocol must be able to detect delayed segments. This can only be done if the number of bytes transmitted during the MSL period is smaller than the sequence number space. Otherwise, there is a risk of accepting duplicate segments.

`Go-back-n` and `selective repeat` can be used in the transport layer as in the datalink layer. Since the network layer does not guarantee an in-order delivery of the packets, a transport entity should always store the segments that it receives out-of-sequence. For this reason, most transport protocols will opt for some form of selective repeat mechanism.

In the datalink layer, the sliding window has usually a fixed size which depends on the amount of buffers allocated to the datalink layer entity. Such a datalink layer entity usually serves one or a few network layer entities. In the transport layer, the situation is different. A single transport layer entity serves a large and varying number of application processes. Each transport layer entity manages a pool of buffers that needs to be shared between all these processes. Transport entity are usually implemented inside the operating system kernel and shares memory with other parts of the system. Furthermore, a transport layer entity must support several (possibly hundreds or thousands) of transport connections at the same time. This implies that the memory which can be used to support the sending or the receiving buffer of a transport connection may change during the lifetime of the connection [#fautotune]_ . Thus, a transport protocol must allow the sender and the receiver to adjust their window sizes.

To deal with this issue, transport protocols allow the receiver to advertise the current size of its receiving window in all the acknowledgments that it sends. The receiving window advertised by the receiver bounds the size of the sending buffer used by the sender. In practice, the sender maintains two state variables : `swin`, the size of its sending window (that may be adjusted by the system) and `rwin`, the size of the receiving window advertised by the receiver. At any time, the number of unacknowledged segments cannot be larger than :math:`\min(swin,rwin)` [#facklost]_ . The utilization of dynamic windows is illustrated in the figure below.

.. figure:: /principles/figures/transport-dwin.*
   :align: center
   :scale: 100

   Dynamic receiving window

The receiver may adjust its advertised receive window based on its current memory consumption, but also to limit the bandwidth used by the sender. In practice, the receive buffer can also shrink as the application may not able to process the received data quickly enough. In this case, the receive buffer may be completely full and the advertised receive window may shrink to `0`. When the sender receives an acknowledgment with a receive window set to `0`, it is blocked until it receives an acknowledgment with a positive receive window. Unfortunately, as shown in the figure below, the loss of this acknowledgment could cause a deadlock as the sender waits for an acknowledgment while the receiver is waiting for a data segment.

.. figure:: /principles/figures/transport-win-deadlock.*
   :align: center
   :scale: 60

   Risk of deadlock with dynamic windows


.. index:: persistence timer

To solve this problem, transport protocols rely on a special timer : the `persistence timer`. This timer is started by the sender whenever it receives an acknowledgment advertising a receive window set to `0`. When the timer expires, the sender retransmits an old segment in order to force the receiver to send a new acknowledgment, and hence send the current receive window size.

To conclude our description of the basic mechanisms found in transport protocols, we still need to discuss the impact of segments arriving in the wrong order. If two consecutive segments are reordered, the receiver relies on their sequence numbers to reorder them in its receive buffer. Unfortunately, as transport protocols reuse the same sequence number for different segments, if a segment is delayed for a prolonged period of time, it might still be accepted by the receiver. This is illustrated in the figure below where segment `D(1,b)` is delayed.


.. figure:: /principles/figures/transport-ambiguities.*
    :align: center
    :scale: 60

    Ambiguities caused by excessive delays

.. index:: maximum segment lifetime (MSL)

To deal with this problem, transport protocols combine two solutions. First, they use 32 bits or more to encode the sequence number in the segment header. This increases the overhead, but also increases the delay between the transmission of two different segments having the same sequence number. Second, transport protocols require the network layer to enforce a `Maximum Segment Lifetime (MSL)`. The network layer must ensure that no packet remains in the network for more than MSL seconds. In the Internet the MSL is assumed [#fmsl]_ to be 2 minutes :rfc:`793`. Note that this limits the maximum bandwidth of a transport protocol. If it uses `n` bits to encode its sequence numbers, then it cannot send more than :math:`2^n` segments every MSL seconds.


Connection release
^^^^^^^^^^^^^^^^^^

.. index:: abrupt connection release

When we discussed the connection-oriented service, we mentioned that there are two types of connection releases : `abrupt release` and `graceful release`.

The first solution to release a transport connection is to define a new control segment (e.g. the `DR` segment for Disconnection Request) and consider the connection to be released once this segment has been sent or received. This is illustrated in the figure below.


.. figure:: /principles/figures/transport-abrupt.*
   :align: center
   :scale: 60

   Abrupt connection release

As the entity that sends the `DR` segment cannot know whether the other entity has already sent all its data on the connection, SDUs can be lost during such an `abrupt connection release`.

.. index:: graceful connection release

The second method to release a transport connection is to release independently the two directions of data transfer. Once a user of the transport service has sent all its SDUs, it performs a `DISCONNECT.req` for its direction of data transfer. The transport entity sends a control segment to request the release of the connection *after* the delivery of all previous SDUs to the remote user. This is usually done by placing in the `DR` the next sequence number and by delivering the `DISCONNECT.ind` only after all previous `DATA.ind`. The remote entity confirms the reception of the `DR` segment and the release of the corresponding direction of data transfer by returning an acknowledgment. This is illustrated in the figure below.

.. figure:: /principles/figures/transport-graceful.*
   :align: center
   :scale: 70

   Graceful connection release


.. [#fsdu] SDU is the acronym of Service Data Unit. We use it as a generic term to represent the data that is transported by a protocol.

.. [#fsizesliding] The size of the sliding window can be either fixed for a given protocol or negotiated during the connection establishment phase. Some protocols allow to change the maximum window size during the data transfer. We will explain these techniques with real protocols later.


.. [#fautotune] For a discussion on how the sending buffer can change, see e.g. [SMM1998]_

.. [#facklost] Note that if the receive window shrinks, it might happen that the sender has already sent a segment that is not anymore inside its window. This segment will be discarded by the receiver and the sender will retransmit it later.

.. [#fmsl] In reality, the Internet does not strictly enforce this MSL. However, it is reasonable to expect that most packets on the Internet will not remain in the network during more than 2 minutes. There are a few exceptions to this rule, such as :rfc:`1149` whose implementation is described in http://www.blug.linux.no/rfc1149/ but there are few real links supporting :rfc:`1149` in the Internet.
   
.. spelling:word-list::

   multi
   Multi

.. include:: /links.rst


