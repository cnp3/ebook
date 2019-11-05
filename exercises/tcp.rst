.. Copyright |copy| 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


TCP basics
==========


TCP is one of the key protocols in today's Internet. A TCP connection always starts with a three-way handshake. The exercises below should help you to improve your understandings of this first phase of a TCP connection.


.. inginious:: tcp-syn-port

.. inginious:: tcp-syn

.. inginious:: tcp-syn-seq-ack

.. inginious:: tcp-syn-ack-bits

.. inginious:: tcp-reorder-twh
	       
.. inginious:: tcp-reorder-twh2


Once the connection is established, the client and the server can exchange data and acknowledgments. 


.. inginious:: tcp-data-ack

.. inginious:: tcp-data-ack2

.. inginious:: tcp-infer-ack	       
	       
.. inginious:: tcp-reorder-data	       
	       

A connection ends with the transmission of segments that include the `FIN` flag that marks the end of the data transfer.

.. inginious:: tcp-fin

	       
	       
TCP can be extended by using options that are negotiated during the three-way handshake.

.. inginious:: tcp-syn-timestamp

.. inginious:: tcp-wscale	       

.. inginious:: tcp-hl-syn

	       
With your knowledge of TCP, you should now be able to reorder all the segments exchanged over a TCP connection.


.. inginious:: tcp-reorder-conn

	       
	       
.. rubric:: Footnotes




.. include:: /links.rst
