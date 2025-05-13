.. Copyright |copy| 2010 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_

*********************
The application layer
*********************

Networked applications rely on the transport service. As explained earlier, there are two main types of transport services :

 - the `connectionless` service
 - the `connection-oriented` or `byte-stream` service

The connectionless service allows applications to easily exchange messages or Service Data Units. On the Internet, this service is provided by the UDP protocol that will be explained in the next chapter. The connectionless transport service on the Internet is unreliable, but is able to detect transmission errors. This implies that an application will not receive data that has been corrupted due to transmission errors.

The connectionless transport service allows networked application to exchange messages. Several networked applications may be running at the same time on a single host. Each of these applications must be able to exchange SDUs with remote applications. To enable these exchanges of SDUs, each networked application running on a host is identified by the following information :

 - the `host` on which the application is running
 - the `port number` on which the application `listens` for data

On the Internet, the `port number` is an integer and the `host` is identified by its IPv4 or IPv6 address. There are two types of Internet addresses :

 - `IP version 4` addresses that are 32 bits wide
 - `IP version 6` addresses that are 128 bits wide

A host that only has an IPv4 address cannot communicate with a host having only an IPv6 address. The figure below illustrates two applications that are using the datagram service provided by UDP on hosts that are using IPv4 addresses.


    .. tikz:: The connectionless or datagram service
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, node distance=5em, font=\small}, }
        \node[elem, minimum width=16em] (N) {Datagram service};
        \node[elem, above=of N.west, anchor=west] (A1) {Application 1};
        \node[elem, above=of N.east, anchor=east] (A2) {Application 2};

        \draw[thick] ([xshift=3em, yshift=-1em]A1.west) -- ([xshift=3em, yshift=1em]N.west) node[midway] (I1) {\Large $\bullet$};
        \draw[thick] ([xshift=-3em, yshift=-1em]A2.east) -- ([xshift=-3em, yshift=1em]N.east) node[midway] (I2) {\Large $\bullet$};

        \node[left=of I1, align=left, font=\scriptsize] (T1) {Identification:\\IP address: 130.104.32.107\\Protocol: UDP\\Port: 1234};
        \node[right=of I2, align=left, font=\scriptsize] (T2) {Identification:\\IP address: 139.165.16.12\\Protocol: UDP\\Port: 53};

        \draw[arrow] (I1) -- (T1);
        \draw[arrow] (I2) -- (T2);


The second transport service is the connection-oriented service. On the Internet, this service is often called the `byte-stream service` as it creates a reliable byte stream between the two applications that are linked by a transport connection. Like the datagram service, the networked applications that use the byte-stream service are identified by the host on which they run and a port number. These hosts can be identified by an address or a name. The figure below illustrates two applications that are using the byte-stream service provided by the TCP protocol on IPv6 hosts. The byte-stream service provided by TCP is reliable and bidirectional.

    .. tikz:: The connection-oriented or byte-stream service
        :libs: positioning, matrix, arrows

        \tikzstyle{arrow} = [thick,->,>=stealth]
        \tikzset{elem/.style = {rectangle, thick, draw, text centered, minimum height=2em, node distance=5em, font=\small}, }
        \node[elem, minimum width=16em] (N) {Byte-stream service};
        \node[elem, above=of N.west, anchor=west] (A1) {Application 1};
        \node[elem, above=of N.east, anchor=east] (A2) {Application 2};

        \draw[thick] ([xshift=3em, yshift=-1em]A1.west) -- ([xshift=3em, yshift=1em]N.west) node[midway] (I1) {\Large $\bullet$};
        \draw[thick] ([xshift=-3em, yshift=-1em]A2.east) -- ([xshift=-3em, yshift=1em]N.east) node[midway] (I2) {\Large $\bullet$};

        \node[left=of I1, align=left, font=\scriptsize] (T1) {Identification:\\IP address: 2001:db8::200c:417a\\Protocol: TCP\\Port: 1234};
        \node[right=of I2, align=left, font=\scriptsize] (T2) {Identification:\\IP address: 2001:4860:a005::68\\Protocol: TCP\\Port: 53};

        \draw[arrow] (I1) -- (T1);
        \draw[arrow] (I2) -- (T2);

