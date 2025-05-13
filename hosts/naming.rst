.. Copyright |copy| 2013, 2019, 2025 by Olivier Bonaventure
.. This file is licensed under a `creative commons licence <https://creativecommons.org/licenses/by-sa/3.0/>`_

.. index:: naming, addressing

.. _naming:

Naming and addressing
---------------------

The network and the transport layers rely on addresses that are encoded as fixed-size bit strings. A network layer address uniquely identifies a host. Several transport layer entities can use the service of the same network layer. For example, a reliable transport protocol and a connectionless transport protocol can coexist on the same host. In this case, the network layer multiplexes the segments produced by these two protocols. This multiplexing is usually achieved by placing in the network packet header a field that indicates which transport protocol should process the segment. Given that there are few different transport protocols, this field does not need to be long. The port numbers play a similar role in the transport layer since they enable it to multiplex data from several application processes.

While addresses are natural for the network and transport layer entities, humans prefer to use names when interacting with network services. Names can be encoded as a character string, and a mapping service allows applications to map a name into the corresponding address. Using names is friendlier for humans, but it also provides a level of indirection which is very useful in many situations.

In the early days of the Internet, only a few hosts (mainly minicomputers) were connected to the network. The most popular applications were :term:`remote login` and file transfer. By 1983, there were already five hundred hosts attached to the Internet [Zakon]_. Each of these hosts was identified by a unique address. Forcing human users to remember the addresses of the hosts that they wanted to use was not user-friendly. Humans prefer to remember names and use them when needed. Using names as aliases for addresses is a common technique in Computer Science. It simplifies the development of applications and allows the developer to ignore the low-level details. For example, by using a programming language instead of writing machine code, a developer can write software without knowing whether the variables that it uses are stored in memory or inside registers.

Because names are at a higher level than addresses, they allow (both in the example of programming above and on the Internet) to treat addresses as mere technical identifiers, which can change at will. Only the names are stable.

.. index:: Network Information Center, hosts.txt

The first solution that allowed applications to use names was the :term:`hosts.txt` file. This file is similar to the symbol table found in compiled code. It contains the mapping between the name of each Internet host and its associated address [#fhosts]_. It was maintained by the SRI International Network Information Center (NIC). When a new host was connected to the network, the system administrator had to register its name and address at the NIC. The NIC updated the :term:`hosts.txt` file on its server. All Internet hosts regularly retrieved the updated :term:`hosts.txt` file from the SRI_ server. This file was stored at a well-known location on each Internet host (see :rfc:`952`) and networked applications could use it to find the address corresponding to a name.

A :term:`hosts.txt` file can be used when there are up to a few hundred hosts on the network. However, it is clearly not suitable for a network containing thousands or millions of hosts. A key issue in a large network is to define a suitable naming scheme. The ARPANet initially used a flat naming space, i.e. each host was assigned a unique name. To limit collisions between names, these names usually contained the name of the institution and a suffix to identify the host inside the institution (a kind of poor man's hierarchical naming scheme). On the ARPANet, few institutions had several hosts connected to the network.

However, the limitations of a flat naming scheme became clear before the end of the ARPANet, and :rfc:`819` proposed a hierarchical naming scheme. While :rfc:`819` discussed the possibility of organizing the names as a directed graph, the Internet opted for a tree structure capable of containing all names. In this tree, the top-level domains are those that are directly attached to the root. The first top-level domain was `.arpa` [#fdnstimeline]_. This top-level name was initially added as a suffix to the names of the hosts attached to the ARPANet and listed in the `hosts.txt` file. In 1984, the `.gov`, `.edu`, `.com`, `.mil`, and `.org` generic top-level domain names were added. :rfc:`1032` proposed the utilization of the two-letter :term:`ISO-3166` country codes as top-level domain names. Since :term:`ISO-3166` defines a two-letter code for each country recognized by the United Nations, this allowed all countries to automatically have a top-level domain. These domains include `.be` for Belgium, `.fr` for France, `.us` for the USA, `.ie` for Ireland, or `.tv` for Tuvalu, a group of small islands in the Pacific, or `.tm` for Turkmenistan. The set of top-level domain names is managed by the Internet Corporation for Assigned Names and Numbers (:term:`ICANN`). :term:`ICANN` adds generic top-level domains that are not related to a country, and the `.cat` top-level domain has been registered for the Catalan language. There are ongoing discussions within :term:`ICANN` to increase the number of top-level domains.

Each top-level domain is managed by an organization that decides how subdomain names can be registered. Most top-level domain names use a first-come, first-served system and allow anyone to register domain names, but there are some exceptions. For example, `.gov` is reserved for the US government, `.int` is reserved for international organizations, and names in the `.ca` are mainly `reserved <http://en.wikipedia.org/wiki/.ca>`_ for companies or users that are present in Canada.

.. tikz:: The tree of domain names
   :libs: shapes

   \tikzset{d/.style = {ellipse, draw},}
   \node {[d] {.}}
      child { node[d] {edu}
              child { node[d] {ucla} }
	      child { node[d] {mit} } }
      child { node[d] {fr} }
      child { node[d] {tv} }
      child { node[d] {com}
         child { node[d] {google} }
	 child { node[d] {sun} }
	 child { node[d] {apple} } }
      child { node[d] {org} }
      child { node[d] {net} }
      child { node[d] {be}
         child { node[d] {uclouvain}
                 child {node {www} } } }
      child { node[d] {in} }
      child { node[d] {ca} }
      child { node[d] {info}
         child {node[d] {computer-networking}
                child { node {www} }
		child { node {blog} } } };


The syntax of the domain names has been defined more precisely in
:rfc:`1035`. This document recommends
the following :term:`BNF` for fully qualified
domain names (the domain names themselves have a much richer syntax).

.. code-block:: abnf
   :caption: BNF of the fully qualified host names

   domain ::= subdomain | " "
   subdomain ::= label | subdomain "." label
   label ::= letter [ [ ldh-str ] let-dig ]
   ldh-str ::= let-dig-hyp | let-dig-hyp ldh-str
   let-dig-hyp ::= let-dig | "-"
   let-dig ::= letter | digit
   letter ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
   digit ::= any one of the ten digits 0 through 9



This grammar specifies that a host name is an ordered list of labels separated by the dot (`.`) character. Each label can contain letters, numbers, and the hyphen character (`-`) [#fidn]_. Fully qualified domain names are read from left to right. The first label is a hostname or a domain name followed by the hierarchy of domains and ending with the root implicitly at the right. The top-level domain name must be one of the registered TLDs [#ftld]_. For example, in the above figure, `www.computer-networking.info` corresponds to a host named `www` inside the `computer-networking` domain that belongs to the `info` top-level domain.

.. note:: Some visually similar characters have different character codes

   The Domain Name System was created at a time when the Internet was mainly used in North America. The initial design assumed that all domain names would be composed of letters and digits :rfc:`1035`. As Internet usage grew in other parts of the world, it became important to support non-ASCII characters. For this, extensions have been proposed to the Domain Name System :rfc:`3490`. In a nutshell, the solution that is used to support Internationalized Domain Names works as follows. First, it is possible to use most of the Unicode characters to encode domain names and hostnames, with a few exceptions (for example, the dot character cannot be part of a name since it is used as a separator). Once a domain name has been encoded as a series of Unicode characters, it is then converted into a string that contains the ``xn--`` prefix and a sequence of ASCII characters. More details on these algorithms can be found in :rfc:`3490` and :rfc:`3492`.

   The possibility of using all Unicode characters to create domain names opened a new form of attack called the `homograph attack <https://en.wikipedia.org/wiki/IDN_homograph_attack>`_. This attack occurs when two character strings or domain names are visually similar but do not correspond to the same server. A simple example is https://G00GLE.COM and https://GOOGLE.COM. These two URLs are visually close but they correspond to different names (the first one does not point to a valid server [#fg00gle]_). With other Unicode characters, it is possible to construct domain names that are visually equivalent to existing ones. See [Zhe2017]_ for additional details on this attack.


This hierarchical naming scheme is a key component of the Domain Name System (DNS). The DNS is a distributed database that contains mappings between fully qualified domain names and addresses. The DNS uses the client-server model. The clients are hosts or applications that need to retrieve the mapping for a given name. Each :term:`nameserver` stores part of the distributed database and answers the queries sent by clients. There is at least one :term:`nameserver` that is responsible for each domain. In the figure below, domains are represented by circles and there are three hosts inside domain `dom` (`h1`, `h2`, and `h3`) and three hosts inside domain `a.sdom1.dom`. As shown in the figure below, a sub-domain may contain both host names and sub-domains.

.. tikz:: A simple tree of domain names
   :libs: shapes

   \tikzset{d/.style = {ellipse, draw},}
   \node {}
      child { node[d] {dom}
	      child { node[d] {sdom2} }
              child { node {h1} }
	      child { node {h2} }
	      child { node {h3} }
	      child { node[d] {sdom1}
	            child { node[d] {a}
		            child { node {h1} }
			    child { node {h2} }
			    child { node {h3} }
		    }
		    child { node[d] {b} }
		    child { node[d] {z} }
		    }
	      };



A :term:`nameserver` that is responsible for domain `dom` can directly answer the following queries :

 - the address of any host residing directly inside domain `dom` (e.g. `h2.dom` in the figure above)
 - the nameserver(s) that are responsible for any direct sub-domain of domain `dom` (i.e. `sdom1.dom` and `sdom2.dom` in the figure above, but not `z.sdom1.dom`)

To retrieve the mapping for host `h2.dom`, a client sends its query to the name server that is responsible for the domain `.dom`. The name server directly answers the query. To retrieve a mapping for `h3.a.sdom1.dom`, a DNS client first sends a query to the name server that is responsible for the `.dom` domain. This nameserver returns the nameserver that is responsible for the `sdom1.dom` domain. This nameserver can now be contacted to obtain the nameserver that is responsible for the `a.sdom1.dom` domain. This nameserver can be contacted to retrieve the mapping for the `h3.a.sdom1.dom` name. Thanks to this structure, it is possible for a DNS client to obtain the mapping of any host inside the `.dom` domain or any of its subdomains. To ensure that any DNS client will be able to resolve any fully qualified domain name, there are special nameservers that are responsible for the root of the domain name hierarchy. These nameservers are called :term:`root nameserver`.

Each root nameserver maintains the list [#froot]_ of all the nameservers that are responsible for each of the top-level domain names and their addresses [#frootv6]_. All root nameservers cooperate and provide the same answers. By querying any of the root nameservers, a DNS client can obtain the nameserver that is responsible for any top-level-domain name. From this nameserver, it is possible to resolve any domain name.


To be able to contact the root nameservers, each DNS client must know their addresses. This implies that DNS clients must maintain an up-to-date list of the addresses of the root nameservers. Without this list, it is impossible to contact the root nameservers. Forcing all Internet hosts to maintain the most recent version of this list would be difficult from an operational point of view. To solve this problem, the designers of the DNS introduced a special type of DNS server : the DNS resolvers. A :term:`resolver` is a server that provides the name resolution service for a set of clients. A network usually contains a few resolvers. Each host in these networks is configured to send all its DNS queries via one of its local resolvers. These queries are called `recursive queries` as the :term:`resolver` must recursively send requests through the hierarchy of nameservers to obtain the `answer`.

DNS resolvers have several advantages over letting each Internet host query directly nameservers. Firstly, regular Internet hosts do not need to maintain the up-to-date list of the addresses of the root servers. Secondly, regular Internet hosts do not need to send queries to nameservers all over the Internet. Furthermore, as a DNS resolver serves a large number of hosts, it can cache the received answers. This allows the resolver to quickly return answers for popular DNS queries and reduces the load on all DNS servers [JSBM2002]_.


Benefits of names
^^^^^^^^^^^^^^^^^

In addition to being more human-friendly, using names instead of addresses inside applications has several important benefits. To understand them, let us consider a popular application that provides information stored on servers. This application involves clients and servers. The server provides information upon requests from client processes. A first deployment of this application would be to rely only on addresses. In this case, the server process would be installed on one host, and the clients would connect to this server to retrieve information. Such a deployment has several drawbacks :

 - if the server process moves to another physical server, all clients must be informed about the new server address.
 - if there are many concurrent clients, the load of the server will increase without any possibility of adding another server without changing the server addresses used by the clients.


Using names solves these problems and provides additional benefits. If the clients are configured with the name of the server, they will query the name service before contacting the server. The name service will resolve the name into the corresponding address. If a server process needs to move from one physical server to another, it suffices to update the name-to-address mapping on the name service to allow all clients to connect to the new server. The name service also enables the servers to better sustain the load. Assume a very popular server which is accessed by millions of users. This service cannot be provided by a single physical server due to performance limitations. Thanks to the utilization of names, it is possible to scale this service by mapping a given name to a set of addresses. When a client queries the name service for the server's name, the name service returns one of the addresses in the set. Various strategies can be used to select one particular address inside the set of addresses. A first strategy is to select a random address in the set. A second strategy is to maintain information about the load on the servers and return the address of the less loaded server. Note that the list of server addresses does not need to remain fixed. It is possible to add and remove addresses from the list to cope with load fluctuations. Another strategy is to infer the location of the client from the name request and return the address of the closest server.

Mapping a single name onto a set of addresses allows popular servers to dynamically scale. There are also benefits in mapping multiple names, possibly a large number of them, onto a single address. Consider the case of information servers run by individuals or SMEs. Some of these servers attract only a few clients per day. Using a single physical server for each of these services would be a waste of resources. A better approach is to use a single server for a set of services that are all identified by different names. This enables service providers to support a large number of server processes, identified by different names, onto a single physical server. If one of these server processes becomes very popular, it will be possible to map its name onto a set of addresses to be able to sustain the load. There are some deployments where this mapping is done dynamically in function of the load.

Names provide a lot of flexibility compared to addresses. For the network, they play a similar role as variables in programming languages. No programmer using a high-level programming language would consider using hardcoded values instead of variables. For the same reasons, all networked applications should depend on names and avoid dealing with addresses as much as possible.

.. _DNS:

The Domain Name System
======================

The last component of the Domain Name System is the DNS protocol. The original DNS protocol runs above both the datagram and the bytestream services. In practice, the datagram service is used when short queries and responses are exchanged, and the bytestream service is used when longer responses are expected. In this section, we first focus on the utilization of the DNS protocol above the datagram service. We will discuss later other recently proposed protocols to carry DNS information.

.. index:: DNS message format

DNS messages are composed of five parts that are named sections in RFC :`1035`. The first three sections are mandatory, and the last two sections are optional. The first section of a DNS message is its `Header`. It contains information about the message type and the content of the other sections. The second section contains the `Question` sent to the nameserver or resolver. The third section contains the `Answer` to the `Question`. When a client sends a DNS query, the `Answer` section is empty. The fourth section, named `Authority`, contains information about the servers that can provide an authoritative answer if required. The last section contains additional information that is supplied by the resolver or nameserver but was not requested in the question.

The header of DNS messages is composed of 12 bytes. The figure below presents its structure.

.. figure:: /pkt/dnsheader.*
   :align: center
   :scale: 100

   The DNS header

The `Transaction ID` (transaction identifier) is a 16-bit random value chosen by the client.
When a client sends a question to a DNS server, it remembers the question and its identifier. When a server returns an answer, it returns in the `Transaction ID` field the identifier chosen by the client. Thanks to this identifier, the client can match the received answer with the question that it sent.

.. dns attacks http://www.cs.columbia.edu/~smb/papers/dnshack.ps
.. http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html
.. http://www.secureworks.com/research/articles/dns-cache-poisoning

The DNS header contains a series of flags. The `QR` flag is used to distinguish between queries and responses. It is set to `0` in DNS queries and `1` in DNS answers. The `Opcode` is used to specify the query type. For instance, a :term:`standard query` is used when a client sends a `name` and the server returns the corresponding `data`. An update request is used when the client sends a `name` and new `data`, and the server then updates its database.

The `AA` bit is set when the server that sent the response has `authority` for the domain name found in the question section. In the original DNS deployments, two types of servers were considered : `authoritative` servers and `non-authoritative` servers. The `authoritative` servers are managed by the system administrators responsible for a given domain. They always store the most recent information about a domain. `Non-authoritative` servers are servers or resolvers that store DNS information about external domains without being managed by the owners of a domain. They may thus provide answers that are out of date. From a security point of view, the `authoritative` bit is not an absolute indication about the validity of an answer. Securing the Domain Name System is a complex problem that was only addressed satisfactorily recently by the utilization of cryptographic signatures in the DNSSEC extensions to DNS described in : RFC:`4033`.

.. These extensions are discussed in chapter :ref:`DNSSEC`.

The `RD` (recursion desired) bit is set by a client when it sends a query to a resolver. Such a query is said to be `recursive` because the resolver will recursively traverse the DNS hierarchy to retrieve the answer on behalf of the client. In the past, all resolvers were configured to perform recursive queries on behalf of any Internet host. However, this exposes the resolvers to several security risks. The simplest one is that the resolver could become overloaded by having too many recursive queries to process. Most resolvers [#f8888]_ only allow recursive queries from clients belonging to their company or network and discard all other recursive queries. The `RA` bit indicates whether the server supports recursion. The `RCODE` is used to distinguish between different types of errors. See : RFC:`1035` for additional details. The last four fields indicate the size of the `Question`, `Answer`, `Authority`, and `Additional` sections of the DNS message.

The last four sections of the DNS message contain `Resource Records` (RR).  All RRs have the same top-level format shown in the figure below.

.. figure:: /pkt/dnsrr.*
   :align: center
   :scale: 100

   DNS Resource Records

In a `Resource Record` (`RR`), the `Name` indicates the name of the node to which this resource record pertains. The two-byte `Type` field indicates the type of resource record. The `Class` field was used to support the utilization of the DNS in other environments than the Internet. The `IN` `Class` refers to Internet names.

The `TTL` field indicates the lifetime of the `Resource Record` in seconds. This field is set by the server that returns an answer and indicates for how long a client or a resolver can store the `Resource Record` inside its cache. A long `TTL` indicates a stable `RR`. Some companies use short `TTL` values for mobile hosts and also for popular servers. For example, a web hosting company that wants to spread the load over a pool of hundred servers can configure its nameservers to return different answers to different clients. If each answer has a small `TTL`, the clients will be forced to send DNS queries regularly. The nameserver will reply to these queries by supplying the address of the less loaded server.

The `RDLength` field is the length of the `RData` field that contains the information of the type specified in the `Type` field.

Several types of DNS RR are used in practice. The `A` type encodes the IPv4 address that corresponds to the specified name. The `AAAA` type encodes the IPv6 address that corresponds to the specified name. A `NS` record contains the name of the DNS server that is responsible for a given domain. For example, a query for the `AAAA` record associated with the `www.ietf.org` name returned the following answer:

.. figure:: /pkt/dns6-www-ietf-org.*
   :align: center

   Query for the `AAAA` record of `www.ietf.org`

This answer contains several pieces of information. First, the name `www.ietf.org` is associated with the IP address `2001:1890:123a::1:1e`. Second, the `ietf.org` domain is managed by six different nameservers. Five of these nameservers are reachable via IPv4 and IPv6.

`CNAME` (or canonical names) are used to define aliases. For example, `www.example.com` could be a `CNAME` for `pc12.example.com`, which is the actual name of the server on which the web server for `www.example.com` runs.

.. note:: Reverse DNS

 The DNS is mainly used to find the address that corresponds to a given name. However, it is sometimes useful to obtain the name that corresponds to an IP address. This is done by using the `PTR` (`pointer`) `RR`. The `RData` part of a `PTR` `RR` contains the name while the `Name` part of the `RR` contains the IP address encoded in the `in-addr.arpa` domain. IPv4 addresses are encoded in the `in-addr.arpa` by reversing the four digits that compose the dotted decimal representation of the address. For example, consider IPv4 address `192.0.2.11`. The hostname associated to this address can be found by requesting the `PTR` `RR` that corresponds to `11.2.0.192.in-addr.arpa`.
 A similar solution is used to support IPv6 addresses : RFC:`3596`, but slightly more complex given the length of the IPv6 addresses. For example, consider IPv6 address `2001:1890:123a::1:1e`. To obtain the name that corresponds to this address, we need first to convert it in a reverse dotted decimal notation : `e.1.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.3.2.1.0.9.8.1.1.0.0.2`. In this notation, each character between dots corresponds to one nibble, i.e. four bits. The low-order byte (`e`) appears first and the high order (`2`) last. To obtain the name that corresponds to this address, one needs to append the `ip6.arpa` domain name and query for `e.1.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.a.3.2.1.0.9.8.1.1.0.0.2.ip6.arpa`. In practice, tools and libraries do the conversion automatically and the user does not need to worry about it.

An important point to note regarding the Domain Name System is that it is extensible. Thanks to the `Type` and `RDLength` fields, the format of the Resource Records can easily be extended. Furthermore, a DNS implementation that receives a new Resource Record that it does not understand can ignore the record while still being able to process the other parts of the message. This allows, for example, a DNS server that only supports IPv6 to
safely ignore the IPv4 addresses listed in the DNS reply for `www.ietf.org` while still being able to correctly parse the Resource Records that it understands. This allowed the Domain Name System to evolve over the years while still preserving the backward compatibility with already deployed DNS implementations.



.. rubric:: Footnotes

.. [#fhosts] The :term:`hosts.txt` file is not maintained anymore. A historical snapshot from April 1984 is available from https://www.saildart.org/HOSTS.TXT%5BHST,NET%5D15

.. [#fdnstimeline] See http://www.donelan.com/dnstimeline.html for a timeline of DNS-related developments.

.. [#fidn] This specification evolved later to support domain names written by using other character sets than us-ASCII :rfc:`5890`. This extension is important to support languages other than English, but a detailed discussion is outside the scope of this document.

.. [#ftld] The official list of top-level domain names is maintained by :term:`IANA` at http://data.iana.org/TLD/tlds-alpha-by-domain.txt. Additional information about these domains may be found at http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains.

.. [#fg00gle] It is interesting to note that to prevent any homograph attack, Google Inc. registered the `g00gle.com` domain name but does not apparently use it.

.. [#froot] A copy of the information maintained by each root nameserver is available at http://www.internic.net/zones/root.zone.

.. [#frootv6] Until February 2008, the root DNS servers only had IPv4 addresses. IPv6 addresses were slowly added to the root DNS servers to avoid creating problems as discussed in http://www.icann.org/en/committees/security/sac018.pdf. As of February 2021, there remain a few DNS root servers that are still not reachable using IPv6. The full list is available at http://www.root-servers.org/.

.. [#f8888] Some DNS resolvers allow any host to send queries. Google operates a `public DNS resolver <https://developers.google.com/speed/public-dns/docs/using>`_ at addresses `2001:4860:4860::8888` and `2001:4860:4860::8844`. Other companies provide similar services.

              
.. spelling:word-list::

   subdomains

.. include:: /links.rst

