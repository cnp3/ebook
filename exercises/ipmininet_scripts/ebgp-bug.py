# O. Bonaventure, November 2019, based on the ipmininet examples
import shlex
import ipmininet.router.config.bgp as _bgp
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AF_INET6, CLIENT_PROVIDER, SHARE

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopology(IPTopo):
    """Creates a very simple interdomain topology"""
    def build(self, *args, **kwargs):
        """
         +---$>----AS5--------------=-----+
         |                                |
        AS1 -<$--- AS2 --=--> AS3---=----AS4
         ^                     |
         +-----------$---------+ 
        """
        # Add all routers
        as1 = self.addRouter('as1')
        as2 = self.addRouter('as2')
        as3 = self.addRouter('as3')
        as4 = self.addRouter('as4')
        as5 = self.addRouter('as5')

        routers=self.routers()
        prefix = {routers[i]: '2001:cafe:%04x::/48' % (i+1) for i in range(len(routers ))}

        as1.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as1],)),))
        as2.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as2],)),))
        as3.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as3],)),))
        as4.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as4],)),))
        as5.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as5],)),))


        # Add hosts

        h1= self.addHost("h1")
        h2= self.addHost("h2")
        h3= self.addHost("h3")
        h4= self.addHost("h4")
        h5= self.addHost("h5")

        # Add all links
        l12=self.addLink(as1, as2, delay='10ms')
        l12[as1].addParams(ip="2001:cafe:1:12::1/64")
        l12[as2].addParams(ip="2001:cafe:1:12::2/64")
        
        l13=self.addLink(as1, as3, delay='10ms')
        l13[as1].addParams(ip="2001:cafe:1:13::1/64")
        l13[as3].addParams(ip="2001:cafe:1:13::3/64")
        
        l23=self.addLink(as2, as3, delay='10ms')
        l23[as2].addParams(ip="2001:cafe:2:23::2/64")
        l23[as3].addParams(ip="2001:cafe:2:23::3/64")

        l15=self.addLink(as1, as5, delay='10ms')
        l15[as1].addParams(ip="2001:cafe:1:15::1/64")
        l15[as5].addParams(ip="2001:cafe:1:15::5/64")

        l24=self.addLink(as2, as4, delay='10ms')
        l24[as2].addParams(ip="2001:cafe:2:24::2/64")
        l24[as4].addParams(ip="2001:cafe:2:24::4/64")

        l34=self.addLink(as3, as4, delay='10ms')
        l34[as3].addParams(ip="2001:cafe:3:34::3/64")
        l34[as4].addParams(ip="2001:cafe:3:34::4/64")

        l45=self.addLink(as4, as5, delay='10ms')
        l45[as4].addParams(ip="2001:cafe:4:45::4/64")
        l45[as5].addParams(ip="2001:cafe:4:45::5/64")


        
        # Links to the hosts
        las1h1 = self.addLink(as1, h1)
        las1h1[as1].addParams(ip=("2001:cafe:1:1::1/64"))
        las1h1[h1].addParams(ip=("2001:cafe:1:1::11/64"))

        las2h2 = self.addLink(as2, h2)
        las2h2[as2].addParams(ip=("2001:cafe:2:1::2/64"))
        las2h2[h2].addParams(ip=("2001:cafe:2:1::12/64"))

        las3h3 = self.addLink(as3, h3)
        las3h3[as3].addParams(ip=("2001:cafe:3:1::3/64"))
        las3h3[h3].addParams(ip=("2001:cafe:3:1::13/64"))

        las4h4 = self.addLink(as4, h4)
        las4h4[as4].addParams(ip=("2001:cafe:4:1::4/64"))
        las4h4[h4].addParams(ip=("2001:cafe:4:1::14/64"))

        las5h5 = self.addLink(as5, h5)
        las5h5[as5].addParams(ip=("2001:cafe:5:1::5/64"))
        las5h5[h5].addParams(ip=("2001:cafe:5:1::15/64"))
        
        # Set AS-ownerships
        self.addAS(1, (as1,))
        self.addAS(2, (as2,))
        self.addAS(3, (as3,))
        self.addAS(4, (as4,))
        self.addAS(5, (as5,))
        
        # Add eBGP sessions
        ebgp_session(self, as2, as1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as3, as1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as5, as1, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as3, as4, link_type=CLIENT_PROVIDER)
       
        ebgp_session(self, as2, as3, link_type=SHARE)
        ebgp_session(self, as2, as4, link_type=SHARE)
        ebgp_session(self, as4, as5, link_type=SHARE)
        super(MyTopology, self).build(*args, **kwargs)

    def post_build(self, net):
        for r in self.routers():
            command="/usr/sbin/tcpdump -i any --immediate-mode -c 50 -w ./bgp-"+r+"-trace.pcap tcp port 179"
            p = net[r].popen(shlex.split(command))
            
        super(MyTopology, self).post_build(net)
        
    
net = IPNet(topo=MyTopology()) 
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
