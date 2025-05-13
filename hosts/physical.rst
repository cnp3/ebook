.. Copyright |copy| 2013, 2025 by Olivier Bonaventure
.. Some portions of this text come from the first edition of this e-book
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by-sa/3.0/>`_


********************
Connecting two hosts
********************

.. index:: electrical cable, optical fiber, multi-mode optical fiber, single-mode optical fiber



The first step when building a network, even a worldwide network such as the Internet, is to connect two hosts together. This is illustrated in the figure below.

   .. tikz:: Connecting two hosts together
      :libs: positioning, matrix

      \tikzset{router/.style = {rectangle, draw, text centered, minimum height=2em}, }
      \tikzset{host/.style = {circle, draw, text centered, minimum height=2em}, }
      \node[host] (B) {B};
      \node[host, right=of B] (A) {A};

      \path[draw,thick]
      (A) edge (B);


To enable the two hosts to exchange information, they need to be linked together by some kind of physical media. Computer networks have used various types of physical media to exchange information, notably :

 - `electrical cable`. Information can be transmitted over different types of electrical cables. The most common ones are the twisted pairs (that are used in the telephone network, but also in enterprise networks) and the coaxial cables (that are still used in cable TV networks, but are no longer used in enterprise networks). Some networking technologies operate over the classical electrical cable.
 - `Optical fiber`. Optical fibers are frequently used in public and enterprise networks when the distance between the communication devices is larger than one kilometer. There are two main types of optical fibers : multi-mode and single-mode. Multi-mode is much cheaper than single-mode fiber because a LED can be used to send a signal over a multi-mode fiber while a single-mode fiber must be driven by a laser. Due to the different modes of propagation of light, multi-mode fibers are limited to distances of a few kilometers while single-mode fibers can be used over distances greater than several tens of kilometers. In both cases, repeaters can be used to regenerate the optical signal at one endpoint of a fiber to send it over another fiber.
 - `Wireless`. In this case, a radio signal is used to encode the information exchanged between the communicating devices. Many types of modulation techniques are used to send information over a wireless channel and there is a lot of innovation in this field with new techniques appearing every year. While most wireless networks rely on radio signals, some use a laser that sends light pulses to a remote detector. These optical techniques allow us to create point-to-point links while radio-based techniques can be used to build networks containing devices spread over a small geographical area.


The physical layer
==================

These physical media can be used to exchange information once this information has been converted into a suitable electrical signal. Entire telecommunication courses and textbooks are devoted to the problem of converting analog or digital information into an electrical signal so that it can be transmitted over a given physical `link`. In this book, we only consider two very simple schemes that allow us to transmit information over an electrical cable. This enables us to highlight the key problems when transmitting
information over a physical link. We are only interested in techniques that allow transmitting digital information through the wire. Here, we will focus on the transmission of bits, i.e. either `0` or `1`.

.. note:: Bit rate

 In computer networks, the bit rate of the physical layer is always expressed in bits per second. One Mbps is one million bits per second, and one Gbps is one billion bits per second. This is in contrast with memory specifications that are usually expressed in bytes (8 bits), KiloBytes (1024 bytes), or MegaBytes (1048576 bytes). Transferring one MByte through a 1 Mbps link lasts 8.39 seconds.

  ========        ===============
  Bit rate        Bits per second
  ========        ===============
  1 Kbps	  :math:`10^3`
  1 Mbps	  :math:`10^6`
  1 Gbps	  :math:`10^9`
  1 Tbps	  :math:`10^{12}`
  ========        ===============


To understand some of the principles behind the physical transmission of information, let us consider the simple case of an electrical wire that is used to transmit bits. Assume that the two communicating hosts want to transmit one thousand bits per second. To transmit these bits, the two hosts can agree on the following rules :

 - On the sender side :
    - set the voltage on the electrical wire at ``+5V`` during one millisecond to transmit a bit set to `1`
    - set the voltage on the electrical wire at ``-5V`` during one millisecond to transmit a bit set to `0`

 - On the receiver side :
    - every millisecond, record the voltage applied on the electrical wire. If the voltage is set to ``+5V``, record the reception of bit `1`. Otherwise, record the reception of bit `0`

.. index:: time-sequence diagram

This transmission scheme has been used in some early networks. We use it as a basis to understand how hosts communicate.  From a computer science viewpoint, dealing with voltages is unusual. Computer scientists frequently rely on models that enable them to reason about the issues that they face without having to consider all implementation details. The physical transmission scheme described above can be represented by using a `time-sequence diagram`.

A `time-sequence diagram` describes the interactions between communicating hosts. By convention, the communicating hosts are represented in the left and right parts of the diagram, while the electrical link occupies the middle of the diagram. In such a time-sequence diagram, time flows from the top to the bottom of the diagram. The transmission of one bit of information is represented by three arrows. Starting from the left, the first horizontal arrow represents the request to transmit one bit of information. This request is represented by a `primitive`, which can be considered as a kind of procedure call. This primitive has one parameter (the bit being transmitted) and a name (`DATA.request` in this example). By convention, all primitives that are named `something.request` correspond to a request to transmit some information. The dashed arrow indicates the transmission of the corresponding electrical signal on the wire. Electrical and optical signals do not travel instantaneously. The diagonal dashed arrow indicates that it takes some time for the electrical signal to be transmitted from `Host A` to `Host B`. Upon reception of the electrical signal, the electronics on `Host B`'s network interface detect the voltage and convert it into a bit. This bit is delivered as a `DATA.indication` primitive. All primitives that are named `something.indication` correspond to the reception of some information. The dashed lines also represent the relationship between two (or more) primitives. Such a time-sequence diagram provides information about the ordering of the different primitives, but the distance between two primitives does not represent a precise amount of time.

  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="Physical link", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(0)" ] ,
      b>>c [ label = "0", arcskip="1"];
      c=>d [ label = "DATA.ind(0)" ];



Time-sequence diagrams are useful when trying to understand the characteristics of a given communication scheme. When considering the above transmission scheme, it is useful to evaluate whether this scheme allows the two communicating hosts to reliably exchange information. A digital transmission is considered reliable when a sequence of bits that is transmitted by a host is received correctly at the other end of the wire. In practice, achieving perfect reliability when transmitting information using the above scheme is difficult. Several problems can occur with such a transmission scheme.


The first problem is that electrical transmission can be affected by electromagnetic interference. Interference can have various sources including natural phenomena (like thunderstorms, variations of the magnetic field,...) but also other electrical signals (such as interference from neighboring cables, interference from neighboring antennas,...). Due to these various types of interference, there is unfortunately no guarantee that when a host transmits one bit on a wire, the same bit is received at the other end. This is illustrated in the figure below where a `DATA.request(0)` on the left host leads to a `Data.indication(1)` on the right host.


  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="Physical link", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];
      a=>b [ label = "DATA.req(0)" ] ,
      b>>c [ label = "", arcskip="1"];
      c=>d [ label = "DATA.ind(1)" ];


With the above transmission scheme, a bit is transmitted by setting the voltage on the electrical cable to a specific value during some period of time. We have seen that due to electromagnetic interference, the voltage measured by the receiver can differ from the voltage set by the transmitter. This is the main cause of transmission errors. However, this is not the only type of problem that can occur. Besides defining the voltages for bits `0` and `1`, the above transmission scheme also specifies the duration of each bit. If one million bits are sent every second, then each bit lasts 1 microsecond. On each host, the transmission (resp. the reception) of each bit is triggered by a local clock having a 1 MHz frequency. These clocks are the second source of problems when transmitting bits over a wire. Although the two clocks have the same specification, they run on different hosts, possibly at a different temperature and with a different source of energy. In practice, it is possible that the two clocks do not operate at exactly the same frequency. Assume that the clock of the transmitting host operates at exactly 1000000 Hz while the receiving clock operates at 999999 Hz. This is a very small difference between the two clocks. However, when using the clock to transmit bits, this difference is important. With its 1000000 Hz clock, the transmitting host will generate one million bits during a period of one second. During the same period, the receiving host will sense the wire 999999 times and thus will receive one bit less than the bits originally transmitted. This small difference in clock frequencies implies that bits can "disappear" during their transmission on an electrical cable. This is illustrated in the figure below.

  .. msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="Physical link", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(0)" ] ,
      b>>c [ label = "", arcskip="1"];
      c=>d [ label = "DATA.ind(0)" ];

      a=>b [ label = "DATA.req(0)" ];


      a=>b [ label = "DATA.req(1)" ] ,
      b>>c [ label = "", arcskip="1"];
      c=>d [ label = "DATA.ind(1)" ];


A similar reasoning applies when the clock of the sending host is slower than the clock of the receiving host. In this case, the receiver will sense more bits than the bits that have been transmitted by the sender. This is illustrated in the figure below where the second bit received on the right was not transmitted by the left host.


  … msc::

      a [label="", linecolour=white],
      b [label="Host A", linecolour=black],
      z [label="Physical link", linecolour=white],
      c [label="Host B", linecolour=black],
      d [label="", linecolour=white];

      a=>b [ label = "DATA.req(0)" ] ,
      b>>c [ label = "", arcskip=1];
      c=>d [ label = "DATA.ind(0)" ];

      c=>d [ label = "DATA.ind(0)" ];

      a=>b [ label = "DATA.req(1)" ] ,
      b>>c [ label = "", arcskip=1];
      c=>d [ label = "DATA.ind(1)" ];


From a Computer Science viewpoint, the physical transmission of information through a wire is often considered as a black box that allows transmitting bits. This black box is commonly referred to as the `physical layer service` and is represented by using the `DATA.request` and `DATA.indication` primitives introduced earlier. This physical layer service facilitates the sending and receiving of bits, by abstracting the technological details that are involved in the actual transmission of the bits as an electromagnetic signal. However, it is important to remember that the `physical layer service` is imperfect and has the following characteristics :

 - the `Physical layer service` may change, e.g. due to electromagnetic interference, the value of a bit being transmitted
 - the `Physical layer service` may deliver `more` bits to the receiver than the bits sent by the sender
 - the `Physical layer service` may deliver `fewer` bits to the receiver than the bits sent by the sender.



.. index:: Manchester encoding

Many other types of encodings have been defined to transmit information over an electrical cable. All physical layers are able to send and receive physical symbols that represent values `0` and `1`. However, for various reasons that are outside the scope of this chapter, several physical layers exchange other physical symbols as well. For example, the Manchester encoding used in several physical layers can send four different symbols. The Manchester encoding is a differential encoding scheme in which time is divided into fixed-length periods. Each period is divided into two halves and two different voltage levels can be applied. To send a symbol, the sender must set one of these two voltage levels during each half period. To send a `1` (resp. `0`), the sender must set a high (resp. low) voltage during the first half of the period and a low (resp. high) voltage during the second half. This encoding ensures that there will be a transition at the middle of each period and allows the receiver to synchronize its clock to the sender's clock. Apart from the encodings for `0` and `1`, the Manchester encoding also supports two additional symbols : `InvH` and `InvB` where the same voltage level is used for the two half periods. By definition, these two symbols cannot appear inside a frame which is only composed of `0` and `1`. Some technologies use these special symbols as markers for the beginning or end of frames.


 .. figure:: /principles/figures/manchester.*
    :align: center
    :scale: 50

    Manchester encoding



.. index:: Physical layer


.. tikz:: The Physical layer 
   :libs: positioning, matrix, arrows

            \tikzstyle{arrow} = [thick,<->,>=stealth]
            \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=8em}, }

            \node[elem] (pm) {Physical};

            \node[elem, left=8em of pm] (pl) {Physical};

            \draw[rectangle, thick, draw, fill=gray!20] ([xshift=1em, yshift=-1em]pl.south) rectangle ([xshift=-1em]pm.south) node [midway, below=.5em] {\scriptsize Physical transmission medium};

            \draw[arrow] (pl.east) -- (pm.west) node [midway, above] {Bits} node [midway, below] {\tiny 01010010100010101001010};


All the functions related to the physical transmission or information through a wire (or a wireless link) are usually known as the `physical layer`. The physical layer allows two or more entities that are directly attached to the same transmission medium to exchange bits. Being able to exchange bits is important as virtually any information can be encoded as a sequence of bits. Electrical engineers are used to processing streams of bits, but computer scientists usually prefer to deal with higher-level concepts. A similar issue arises with file storage. Storage devices such as hard-disks also store streams of bits. There are hardware devices that process the bit stream produced by a hard-disk, but computer scientists have designed filesystems to allow applications to easily access such storage devices. These filesystems are typically divided into several layers as well. Hard-disks store sectors of 512 bytes or more. Unix filesystems group sectors in larger blocks that can contain data or `inodes` representing the structure of the filesystem. Finally, applications manipulate files and directories that are translated into blocks, sectors, and eventually bits by the operating system.

.. index:: Datalink layer, frame

Computer networks use a similar approach. Each layer provides a service that is built above the underlying layer and is closer to the needs of the applications. We will explore the different layers of the protocol stack in this book. 


The datalink layer
==================

.. index:: frame

Computer scientists are usually not interested in exchanging bits between two hosts. They prefer to write software that deals with larger blocks of data in order to transmit messages or complete files. Thanks to the physical layer service, it is possible to send a continuous stream of bits between two hosts. This stream of bits can include logical blocks of data, but we need to be able to extract each block of data from the bit stream despite the imperfections of the physical layer. In many networks, the basic unit of information exchanged between two directly connected hosts is often called a `frame`. A `frame` can be defined as a sequence of bits that has a particular syntax or structure. We will see examples of such frames later in this chapter.

To enable the transmission/reception of frames, the first problem to be solved is how to encode a frame as a sequence of bits, so that the receiver can easily recover the received frame despite the limitations of the physical layer.


.. index:: framing

If the physical layer were perfect, the problem would be very simple. We would simply need to define how to encode each frame as a sequence of consecutive bits. The receiver would then easily be able to extract the frames from the received bits. Unfortunately, the imperfections of the physical layer make this framing problem slightly more complex. Several solutions have been proposed and are used in practice in different network technologies.

Framing
-------

The `framing` problem can be defined as : "`How does a sender encode frames so that the receiver can efficiently extract them from the stream of bits that it receives from the physical layer`".

A first solution to this problem is to require the physical layer to remain idle for some time after the transmission of each frame. These idle periods can be detected by the receiver and serve as a marker to delineate frame boundaries. Unfortunately, this solution is not acceptable for two reasons. First, some physical layers cannot remain idle and always need to transmit bits. Second, inserting an idle period between frames decreases the maximum bit rate that can be achieved.

.. note:: Bit rate and bandwidth

  Bit rate and bandwidth are often used to characterize the transmission capacity of the physical service. The original definition of `bandwidth <https://www.merriam-webster.com/dictionary/bandwidth>`_, as listed in the `Webster dictionary <https://www.merriam-webster.com/dictionary>`_ is `a range of radio frequencies which is occupied by a modulated carrier wave, which is assigned to a service, or over which a device can operate`. This definition corresponds to the characteristics of a given transmission medium or receiver. For example, the human ear is able to decode sounds in roughly the 0-20 KHz frequency range. By extension, bandwidth is also used to represent the capacity of a communication system in bits per second. For example, a Gigabit Ethernet link is theoretically capable of transporting one billion bits per second.


.. index:: bit stuffing, stuffing (bit)

Given that multi-symbol encodings cannot be used by all physical layers, a generic solution which can be used with any physical layer that is able to transmit and receive only bits `0` and `1` is required. This generic solution is called `stuffing` and two variants exist : `bit stuffing` and `character stuffing`. To enable a receiver to easily delineate the frame boundaries, these two techniques reserve special bit strings as frame boundary markers and encode the frames so that these special bit strings do not appear inside the frames.

`Bit stuffing` reserves the `01111110` bit string as the frame boundary marker and ensures that there will never be six consecutive `1` symbols transmitted by the physical layer inside a frame. With bit stuffing, a frame is sent as follows. First, the sender transmits the marker, i.e. `01111110`. Then, it sends all the bits of the frame and inserts an additional bit set to `0` after each sequence of five consecutive `1` bits. This ensures that the sent frame never contains a sequence of six consecutive bits set to `1`. As a consequence, the marker pattern cannot appear inside the frame sent. The marker is also sent to mark the end of the frame. The receiver performs the opposite to decode a received frame. It first detects the beginning of the frame thanks to the `01111110` marker. Then, it processes the received bits and counts the number of consecutive bits set to `1`. If a `0` follows five consecutive bits set to `1`, this bit is removed since it was inserted by the sender. If a `1` follows five consecutive bits set to `1`, it indicates a marker if it is followed by a bit set to `0`. The table below illustrates the application of bit stuffing to some frames.

 ===========================   =============================================
 Original frame	      	       Transmitted frame
 ===========================   =============================================
 0001001001001001001000011     01111110000100100100100100100001101111110
 0110111111111111111110010     01111110011011111011111011111011001001111110
 0111110                       011111100111110001111110
 01111110		                0111111001111101001111110
 ===========================   =============================================


For example, consider the transmission of `0110111111111111111110010`. The sender will first send the `01111110` marker followed by `011011111`. After these five consecutive bits set to `1`, it inserts a bit set to `0` followed by `11111`. A new `0` is inserted, followed by `11111`. A new `0` is inserted followed by the end of the frame `110010` and the `01111110` marker.


Bit stuffing increases the number of bits required to transmit each frame. The worst case for bit stuffing is of course a long sequence of bits set to `1` inside the frame. If transmission errors occur, stuffed bits or markers can be in error. In these cases, the frame affected by the error and possibly the next frame will not be correctly decoded by the receiver, but it will be able to resynchronize itself at the next valid marker.


.. index:: character stuffing, stuffing (character)

Bit stuffing can be easily implemented in hardware. However, implementing it in software is difficult given the complexity of performing bit manipulations in software. Software implementations prefer to process characters than bits; software-based datalink layers usually use `character stuffing`. This technique operates on frames that contain an integer number of characters. In computer networks, characters are usually encoded by relying on the :term:`ASCII` table. This table defines the encoding of various alphanumeric characters as a sequence of bits. :rfc:`20` provides the ASCII table that is used by many Internet protocols. For example, the table defines the following binary representations :

 - `A` : `1000011` b
 - `0` : `0110000` b
 - `z` : `1111010` b
 - `@` : `1000000` b
 - `space` : `0100000` b

In addition, the :term:`ASCII` table also defines several non-printable or control characters. These characters were designed to allow an application to control a printer or a terminal. These control characters include `CR` and `LF`, that are used to terminate a line, and the `BEL` character which causes the terminal to emit a sound.

 - `NUL`: `0000000` b
 - `BEL`: `0000111` b
 - `CR` : `0001101` b
 - `LF` : `0001010` b
 - `DLE`: `0010000` b
 - `STX`: `0000010` b
 - `ETX`: `0000011` b

Some characters are used as markers to delineate the frame boundaries. Many `character stuffing` techniques use the `DLE`, `STX`, and `ETX` characters of the ASCII character set. `DLE STX` (resp. `DLE ETX`) is used to mark the beginning (end) of a frame. When transmitting a frame, the sender adds a `DLE` character after each transmitted `DLE` character. This ensures that none of the markers can appear inside the transmitted frame. The receiver detects the frame boundaries and removes the second `DLE` when it receives two consecutive `DLE` characters. For example, to transmit frame `1 2 3 DLE STX 4`, a sender will first send `DLE STX` as a marker, followed by `1 2 3 DLE`. Then, the sender transmits an additional `DLE` character followed by `STX 4` and the `DLE ETX` marker.


 ===========================================  ===============================================================
 Original frame	      	                      Transmitted frame
 ===========================================  ===============================================================
 **1** **2** **3** **4**		      `DLE STX` **1** **2** **3** **4** `DLE ETX`
 **1** **2** **3** **DLE** **STX** **4**      `DLE STX` **1** **2** **3** **DLE** `DLE` **STX** **4** `DLE ETX`
 **DLE STX DLE ETX**	                      `DLE STX` **DLE** `DLE` **STX** **DLE** `DLE` **ETX** `DLE ETX`
 ===========================================  ===============================================================

`Character stuffing`, like bit stuffing, increases the length of the transmitted frames. For `character stuffing`, the worst frame is a frame containing many `DLE` characters. When transmission errors occur, the receiver may incorrectly decode one or two frames (e.g. if the errors occur in the markers). However, it will be able to resynchronize itself with the next correctly received markers.

Bit stuffing and character stuffing allow recovering frames from a stream of bits or bytes. This framing mechanism provides a richer service than the physical layer. Through the framing service, one can send and receive complete frames. This framing service can also be represented by using the `DATA.request` and `DATA.indication` primitives. This is illustrated in the figure below, assuming hypothetical frames containing four useful bits and one bit of framing for graphical reasons.

  .. msc::

      a [label="", linecolour=white],
      bf [label="Framing-A", linecolour=black],
      bp [label="Phys-A", linecolour=black],
      cp [label="Phys-B", linecolour=black],
      cf [label="Framing-B", linecolour=black],
      d [label="", linecolour=white];

      a=>bf [ label = "DATA.req(1...1)", textcolour=red ];
      bf=>bp [label="DATA.req(0)"],
      bp>>cp [label="0", arcskip=1];
      cp=>cf [label="DATA.ind(0)"];
      bf=>bp [label="DATA.req(1)"],
      bp>>cp [label="1", arcskip=1];
      cp=>cf [label="DATA.ind(1)"];
      ...;
      bf=>bp [label="DATA.req(1)"],
      bp>>cp [label="1", arcskip=1];
      cp=>cf [label="DATA.ind(1)"];
      bf=>bp [label="DATA.req(0)"],
      bp>>cp [label="0", arcskip=1];
      cp=>cf [label="DATA.ind(0)"];
      cf=>d [ label = "DATA.ind(1...1)", textcolour=red ];


We can now build upon the framing mechanism to allow the hosts to exchange frames containing an integer number of bits or bytes. Once the framing problem has been solved, we can use these frames to carry Internet packets.

.. inginious:: mcq-rel-framing

.. inginious:: q-rel-delay


.. note:: Framing on the Internet

   The bit stuffing and character stuffing described above are generic solutions applied by various protocols. When Internet hosts used dial-up modems or serial transmission to exchange data, they used protocols such as SLIP defined in :rfc:`1035` or PPP defined in :rfc:`1661`.

   The Serial Line IP (SLIP) protocol uses character stuffing with two special characters (``END``, 192 in decimal and ``ESC``, 219 in decimal).

   .. todo:: Exercise to parse a SLIP frame
   
   The Point-to-Point Protocol (PPP) supports different techniques of framing. :rfc:`1662` describes how character stuffing and bit stuffing can be used by PPP.

   .. todo:: more complex, exercise with PPP, or perhaps show PPP frames, but there is very little information at https://wiki.wireshark.org/PPP Maybe exercises based on reading RFC 1662

:numref:`fig-datalink-layer` illustrates the second layer of the protocol stack that uses the services provided by the Physical layer to exchange frames. We will use the word frame throughout this book to refer to the unit of information exchanged between two datalink layer entities.
   
.. _fig-datalink-layer:
.. tikz:: The Datalink layer in the protocol stack 
   :libs: positioning, matrix, arrows
	  
           \tikzstyle{arrow} = [thick,<-,>=stealth]
            \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, minimum width=8em}, }

            \node[elem] (dm) {Datalink};

            \node[elem, left=8em of dm] (dl) {Datalink};

            \draw[arrow,<->] (dl.east) -- (dm.west) node [midway, above] {Frames} ;

            \node[elem, below=0em of dm] (pm) {Physical};

            \node[elem, below=0em of dl] (pl) {Physical};

            \draw[rectangle, thick, draw, fill=gray!20] ([xshift=1em, yshift=-1em]pl.south) rectangle ([xshift=-1em]pm.south) node [midway, below=.5em] {\scriptsize Physical transmission medium};

            \draw[arrow,<->] (pl.east) -- (pm.west) node [midway, above] {Bits} node [midway, below] {\tiny 01010010100010101001010};
                      
	     
	  

.. spelling:word-list::

   multi
   Multi

.. include:: /links.rst


