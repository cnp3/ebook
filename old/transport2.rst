.. Copyright |copy| 2013,2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_

****************************
Internet transport protocols
****************************


Transport protocols rely on the service provided by the network layer. On the Internet, the network layer provides a connectionless service. The network layer identifies each (interface of a) host by using an IP address. It enables hosts to transmit packets that contain up to 64 KBytes of payload to any destination reachable through the network. The network layer does not guarantee the delivery of information, cannot detect transmission errors and does not preserve sequence integrity.

Several transport protocols have been designed to provide a richer service to the applications. The two most widely deployed transport protocols on the Internet are the User Datagram Protocol (UDP) and the Transmission Control Protocol (TCP). A third important transport protocol, the Stream Control Transmission Protocol (SCTP) :rfc:`4960` appeared in the early 2000s. It is currently used by some particular applications such as signaling in Voice over IP networks. SCTP was described in the second edition of the e-book.

The Real Time Transport Protocol (RTP), defined in :rfc:`3550` is another important protocol that is used by many multimedia applications. It includes functions that belong to the transport layer, but also functions that are related to the encoding of the information. Due to space limitations, we do not discuss it in this section.

The most recent Internet transport protocol is QUIC, defined in :rfc:`9000`. QUIC is a protocol that runs above UDP but includes both the reliability techniques that are included in TCP and the security features of TLS.
Reliability and security are more closely integrated inside QUIC than
when TLS runs above TCP.
