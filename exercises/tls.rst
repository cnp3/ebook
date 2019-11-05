.. Copyright |copy| 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


TLS and ssh
===========

One of the first motivations for the deployment of wide area networks such as the Internet was to enable researchers to connect to distant servers. For many years, these connections were carried out by using a simple application layer protocol such as telnet over a TCP connection. With telnet, all the characters typed by the user are sent in cleartext over the TCP connection. This implies that if someone is able to capture the packets transmitted over the network, he/she can collect sensitive information such as user names or passwords.

.. inginious:: q-pkt-telnet

.. inginious:: q-pkt-telnet2


Fortunately, telnet is rarely used without TLS these days and system administrators usually prefer to deploy more secure protocols such as ``ssh``.  	       
	       

.. inginious:: q-pkt-ssh-1

.. inginious:: q-pkt-ssh-2

.. inginious:: q-pkt-ssh-3

The Transport Layer Security (TLS) protocol is now used by a wide range of applications, even if the most popular one is HTTPS. In the exercises below, you will analyze some of the features of TLS by looking at the packets that are exchanged over a TLS session.

.. inginious:: q-pkt-tls-1

.. inginious:: q-pkt-tls-2

.. inginious:: q-pkt-tls-4

.. inginious:: q-pkt-tls-smtp
	       

	       

.. rubric:: Footnotes




.. include:: /links.rst
