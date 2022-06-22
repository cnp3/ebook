.. Copyright |copy| 2013 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


********************
Serving applications
********************



Multiple choices questions
==========================

.. inginious:: mcq-transport


Open questions
==============

1. Which are the mechanisms that should be included in a transport protocol providing an unreliable connectionless transport service that can detect transmission errors, but not correct them ?

2. A reliable connection oriented transport places a 32 bits sequence number inside the segment header to number the segments. This sequence number is incremented for each data segment. The connection starts as shown in the figure below :

  .. msc::

     a [label="", linecolour=white],
     b [label="Host A", linecolour=black],
     z [label="", linecolour=white],
     c [label="Host B", linecolour=black],
     d [label="", linecolour=white];
     a=>b [ label = "CONNECT.req()" ] ,
     b>>c [ label = "CR(seq=1341)", arcskip="1"];
     c=>d [ label = "CONNECT.ind()" ];
     d=>c [ label = "CONNECT.resp()" ],
     c>>b [ label = "CA(ack=1341,seq=2141)", arcskip="1"];
     b=>a [ label = "CONNECT.conf()" ];
     b>>c [ label = "CA(seq=1341,ack=2141)", arcskip="1"];
     |||;
     a=>b [ label = "DATA.req(a)" ];


 Continue the connection so that `Host B` sends `Hello` as data and `Host A` replies by sending `Pleased to meet you`. After having received the response, `Host B` closes the connection gracefully and `Host A` does the same. Discuss on the state that needs to be maintained inside each host.

3. A transport connection that provides a message-mode service has been active for some time and all data has been exchanged and acknowledged in both directions. As in the exercise above, the sequence number is incremented after the transmission of each segment. At this time, `Host A` sends two DATA segments as shown in the figure below.

  .. msc::

     a [label="", linecolour=white],
     b [label="Host A", linecolour=black],
     z [label="", linecolour=white],
     c [label="Host B", linecolour=black],
     d [label="", linecolour=white];
     a=>b [ label = "DATA.req(abc)" ] ,
     b-x c [ label = "DATA(seq=1123,abc)", arcskip="1"];
     a=>b [ label = "DATA.req(def)" ] ,
     b>>c [ label = "DATA(seq=1124,def)", arcskip="1"];
     a=>b [ label = "DISCONNECT.req(graceful,A->B)" ];
     |||;


  What are the acknowledgments sent by `Host B`. How does `Host A` react and how does it terminate the connection ?


4. Consider a reliable connection-oriented transport protocol that provides the bytestream service. In this transport protocol, the sequence number that is placed inside each DATA segment reflects the position of the bytes in the bytestream. Considering the connection shown below, provide the DATA segments that are sent by `Host A` in response to the `DATA.request`, assuming that one segment is sent for each `DATA.request`.

  .. msc::

     a [label="", linecolour=white],
     b [label="Host A", linecolour=black],
     z [label="", linecolour=white],
     c [label="Host B", linecolour=black],
     d [label="", linecolour=white];
     a=>b [ label = "CONNECT.req()" ] ,
     b>>c [ label = "CR(seq=8765)", arcskip="1"];
     c=>d [ label = "CONNECT.ind()" ];
     d=>c [ label = "CONNECT.resp()" ],
     c>>b [ label = "CA(ack=8765,seq=4321)", arcskip="1"];
     b=>a [ label = "CONNECT.conf()" ];
     b>>c [ label = "CA(seq=8765,ack=4321)", arcskip="1"];
     |||;
     a=>b [ label = "DATA.req(a)" ];
     |||;
     a=>b [ label = "DATA.req(bcdefg)" ];
     |||;
     a=>b [ label = "DATA.req(ab)" ];
     |||;
     a=>b [ label = "DATA.req(bbbbbbbbbbbb)" ];


5. Same question as above, but consider now that the transport protocol tries to send large DATA segments whenever possible. For this exercise, we consider that a DATA segment can contain up to 8 bytes of data in the payload. Do not forget to show the acknowledgments in your answer.

6. Consider a transport protocol that provides a reliable connection-oriented bytestream service. You observe the segments sent by a host that uses this protocol. Does the time-sequence diagram below reflects a valid implementation of this protocol ? Justify your answer.

  .. msc::

     a [label="", linecolour=white],
     b [label="Host A", linecolour=black],
     z [label="", linecolour=white],
     c [label="Host B", linecolour=black],
     d [label="", linecolour=white];
     a=>b [ label = "DATA.req(abc)" ] ,
     b-x c [ label = "DATA(seq=1123,abc)", arcskip="1"];
     a=>b [ label = "DATA.req(def)" ] ,
     b-x c [ label = "DATA(seq=1126,def)", arcskip="1"];
     |||;
     b>>c [ label = "DATA(seq=1123,abcdef)", arcskip="1"];
     |||;

7. In the above example, the two `DATA` segments were lost before arriving at the destination. Discuss the following scenario and explain how the receiver should react to the reception of the last `DATA` segment.

  .. msc::

     a [label="", linecolour=white],
     b [label="Host A", linecolour=black],
     z [label="", linecolour=white],
     c [label="Host B", linecolour=black],
     d [label="", linecolour=white];
     a=>b [ label = "DATA.req(abc)" ] ,
     b-x c [ label = "DATA(seq=1123,abc)", arcskip="1"];
     a=>b [ label = "DATA.req(def)" ] ,
     b>> c [ label = "DATA(seq=1126,def)", arcskip="1"];
     |||;
     b>>c [ label = "DATA(seq=1123,abcdef)", arcskip="1"];
     |||;

8. A network layer service guarantees that a packet will never live during more than 100 seconds inside the network. Consider a reliable connection-oriented transport protocol that places a 32 bits sequence number inside each segment. What is the maximum rate (in segments per second) at which is should sent data segments to prevent having two segments with the same sequence number inside the network ?


Practice
========

1. Amazon provides the `S3 storage service <https://s3.amazonaws.com/>`_ where companies and researchers can store lots of information and perform computations on the stored information. Amazon allows users to send files through the Internet, but also by sending hard-disks. Assume that a 1 Terabyte hard-disk can be delivered within 24 hours to Amazon by courier service. What is the minimum bandwidth required to match the bandwidth of this courier service ?


.. inginious:: TFTP


Discussion questions
====================

1. In the transport layer, the receive window advertised by a receiver can vary during the lifetime of the connection. What are the causes for these variations ?

2. A reliable connection-oriented protocol can provide a message-mode service or a byte stream service. Which of the following usages of the sequence numbers is the best suited for each of these services ?

  a. DATA segments contain a sequence number that is incremented for each byte transmitted
  b. DATA segments contain a sequence number that is incremented for each DATA segment transmitted

3. Some transport protocols use 32 bits sequence numbers while others use 64 bits sequence number. What are the advantages and drawbacks of each approach ?

4. Consider a transport protocol that provides the bytestream service and uses 32 bits sequence number to represent the position of the first byte of the payload of DATA segments in the bytestream. How would you modify this protocol so that it can provide a message-mode service ? Consider first short messages that always fit inside a single segment. In a second step, discuss how you could support messages of unlimited size.

5. What is piggybacking and what are the benefits of this technique ?

..  To be written : connect by name API is key !  http://www.stuartcheshire.org/IETF72/


.. rubric:: Footnotes


.. include:: /links.rst

