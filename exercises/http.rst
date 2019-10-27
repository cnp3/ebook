.. Copyright |copy| 2013, 2019 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <http://creativecommons.org/licenses/by/3.0/>`_


The HyperText Transfer Protocol
===============================

An important difference between HTTP/1.0, HTTP/1.1 and HTTP/2.0 is their utilization of the underlying transport connections. Answer the three questions below to confirm that you understand the difference between these versions of the HTTP protocol.

.. inginious:: mcq-http-10

.. inginious:: mcq-http-11

.. inginious:: mcq-http-20


1.  System administrators who are responsible for web servers often want to monitor these servers and check that they are running correctly. As a HTTP server uses TCP on port 80, the simplest solution is to open a TCP connection on port 80 and check that the TCP connection is accepted by the remote host. However, as HTTP/1.x is an ASCII-based protocol, it is also very easy to write a small script that downloads a web page on the server and compares its content with the expected one. Use `telnet` or `ncat` to verify that a web server is running on host `www.computer-networking.info` [#fhttp]_


2. Instead of using `telnet` on port 80, it is also possible to use a command-line tool such as curl_ Use curl_ with the `--trace-ascii tracefile` option to store in `tracefile` all the information exchanged by curl_ when accessing the server.

   - what is the version of HTTP used by your version of curl_ ?
   - can you explain the different headers placed by curl_ in the request ?
   - can you explain the different headers found in the response ?

3. HTTP 1.1, specified in :rfc:`2616`, forces the client to include the `Host:` header in all its requests. HTTP 1.0 does not define the `Host:` header, by most implementations support it. By using `telnet` and `curl` retrieve the first page of the http://www.computer-networking.info web server by sending http requests with and without the `Host:` header. Explain the difference between the two. 

4. The headers sent in a HTTP request allow the client to provide additional information to the server. One of these headers is the `Accept-Language` header that allows to indicate the preferred language of the client [#flang]_. For example, `curl -HAccept-Language:en http://www.google.be` will send to `http://www.google.be` a HTTP request indicating English (`en`) as the preferred language. Does google provides a different page in French (`fr`) and Walloon (`wa`) ? Same question for `http://www.uclouvain.be` (given the size of the homepage, use ``diff`` to compare the different pages retrieved from `www.uclouvain.be`)

5. Compare the size of the http://www.yahoo.com and http://www.google.com web pages by downloading them with curl_

6. The `ipvfoo <https://code.google.com/p/ipvfoo/>`_ extension on google chrome allows to visually detect whether a website is using IPv6 and IPv4, but also to see which web sites have been contacted when rendering a given web page. Some websites are distributed over several dozens of different servers. Can you find one ?

7. Some websites are reachable over both IPv4 and IPv6 while others are only reachable over IPv4 [#fv6only]_. You can use the `-6` (resp. `-4`) option to force curl_ to only use IPv6 (resp. IPv4). Verify that `www.computer-networking.info` is reachable over IPv6 and IPv4 and then check whether your university website already supports IPv6.

8. curl_ supports a huge number of options and parameters that are described in its `man page <https://curl.haxx.se/docs/manpage.html>`_ Some of them allow you to force the utilization of a specific version of HTTP. These include `--http0.9`, `--http1.0`, `--http1.1` and `http2`. Using the latter, verify whether your favorite website supports HTTP/2.0.

As for the DNS, besides using software tools that implement the HTTP protocols, it can also be useful to analyze packet traces with wireshark_ . The exercises below contain simple packet traces collected with different versions of the HTTP protocol.

.. inginious:: mcq-http-trace

.. inginious:: mcq-pkt-http2-1

.. inginious:: mcq-pkt-http2-2

.. inginious:: mcq-pkt-http2-3
	       

.. rubric:: Footnotes


.. [#fhttp] The minimum command sent to a HTTP server is `GET / HTTP/1.0` followed by CRLF and a blank line.

.. [#flang] The list of available language tags can be found at http://www.iana.org/assignments/language-subtag-registry Versions in other formats are available at http://www.langtag.net/registries.html Additional information about the support of multiple languages in Internet protocols may be found in rfc5646_

.. [#fv6only] There are probably very few websites that only support IPv6 and not IPv4. If you find one, let us know by submitting a pull-request to change this exercise.

.. include:: /links.rst
