# O. Bonaventure, November 2019, based on the ipmininet examples

import ipmininet.router.config.bgp as _bgp
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AF_INET6, CLIENT_PROVIDER, SHARE

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopology(IPTopo):
    """Creates a very simple interdomain topology"""
    def build(self, *args, **kwargs):
        """
        AS1 --$--> AS2 --$--> AS3
         |                     |
         +-----------=---------+ 
        """
        # Add all routers
        as1 = self.addRouter('as1')
        as2 = self.addRouter('as2')
        as3 = self.addRouter('as3')

        routers=self.routers()
        prefix = {routers[i]: '2001:cafe:%04x::/48' % (i+1) for i in range(len(routers ))}

        as1.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as1],)),))
        as2.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as2],)),))
        as3.addDaemon(BGP, address_families=(AF_INET6(networks=(prefix[as3],)),))


        # Add hosts

        h1= self.addHost("h1")
        h2= self.addHost("h2")
        h3= self.addHost("h3")
        

        # Add all links
        l12=self.addLink(as1, as2)
        l12[as1].addParams(ip="2001:cafe:1:12::1/64")
        l12[as2].addParams(ip="2001:cafe:1:12::2/64")
        
        l13=self.addLink(as1, as3)
        l13[as1].addParams(ip="2001:cafe:1:13::1/64")
        l13[as3].addParams(ip="2001:cafe:1:13::3/64")
        l23=self.addLink(as2, as3)
        l23[as2].addParams(ip="2001:cafe:2:23::2/64")
        l23[as3].addParams(ip="2001:cafe:2:23::3/64")

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


        
        # Set AS-ownerships
        self.addAS(1, (as1,))
        self.addAS(2, (as2,))
        self.addAS(3, (as3,))
        
        # Add eBGP sessions
        ebgp_session(self, as1, as2, link_type=CLIENT_PROVIDER)
        ebgp_session(self, as2, as3, link_type=CLIENT_PROVIDER)
  
       
        ebgp_session(self, as1, as3, link_type=SHARE)
 

        super(MyTopology, self).build(*args, **kwargs)

    
net = IPNet(topo=MyTopology()) 
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
