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
         +---$>----AS3---$>-- AS4---$>---AS7---$>--AS8
         |          ||         ||         $        |
         |          ||         ||         \/       |
        AS1 -<$--- AS2 --$--> AS5---=---AS6-----=---
   
        """
        # Add all routers and hosts
        r=[None]*9
        h=[None]*9
        for i in range(1,9):
            r[i] = self.addRouter("as"+str(i))
            h[i]=self.addHost("h"+str(i))
            r[i].addDaemon(BGP, address_families=(AF_INET6(networks=('2001:cafe:%04x::/48' % (i),)),))
            self.addAS(i, (r[i],))

        
        # Add all links
        l12=self.addLink(r[1], r [2], delay='10ms')
        l12[r[1]].addParams(ip="2001:cafe:1:12::1/64")
        l12[r[2]].addParams(ip="2001:cafe:1:12::2/64")
        
        l13=self.addLink(r[1], r[3], delay='10ms')
        l13[r[1]].addParams(ip="2001:cafe:1:13::1/64")
        l13[r[3]].addParams(ip="2001:cafe:1:13::3/64")
        
        l23=self.addLink(r[2], r[3], delay='10ms')
        l23[r[2]].addParams(ip="2001:cafe:2:23::2/64")
        l23[r[3]].addParams(ip="2001:cafe:2:23::3/64")

        l25=self.addLink(r[2], r[5], delay='10ms')
        l25[r[2]].addParams(ip="2001:cafe:2:25::2/64")
        l25[r[5]].addParams(ip="2001:cafe:2:25::5/64")

        l34=self.addLink(r[3], r[4], delay='10ms')
        l34[r[3]].addParams(ip="2001:cafe:3:34::3/64")
        l34[r[4]].addParams(ip="2001:cafe:3:34::4/64")

        l45=self.addLink(r[4], r[5], delay='10ms')
        l45[r[4]].addParams(ip="2001:cafe:4:45::4/64")
        l45[r[5]].addParams(ip="2001:cafe:4:45::5/64")

        l47=self.addLink(r[4], r[7], delay='10ms')
        l47[r[4]].addParams(ip="2001:cafe:4:47::4/64")
        l47[r[7]].addParams(ip="2001:cafe:4:47::7/64")

        l56=self.addLink(r[5], r[6], delay='10ms')
        l56[r[5]].addParams(ip="2001:cafe:5:56::5/64")
        l56[r[6]].addParams(ip="2001:cafe:5:56::6/64")

        l78=self.addLink(r[7], r[8], delay='10ms')
        l78[r[7]].addParams(ip="2001:cafe:7:78::7/64")
        l78[r[8]].addParams(ip="2001:cafe:7:78::8/64")
        
        l68=self.addLink(r[6], r[8], delay='10ms')
        l68[r[6]].addParams(ip="2001:cafe:6:68::6/64")
        l68[r[8]].addParams(ip="2001:cafe:6:68::8/64")

        
        l67=self.addLink(r[6], r[7], delay='10ms')
        l67[r[6]].addParams(ip="2001:cafe:6:67::6/64")
        l67[r[7]].addParams(ip="2001:cafe:6:67::7/64")
        # Links to the hosts
        for i in range (1,9):
            l = self.addLink(r[i],h[i])
            l[r[i]].addParams(ip=('2001:cafe:%04x:1::%04x/64' %(i, i)))
            l[h[i]].addParams(ip=('2001:cafe:%04x:1::%04x/64' %(i,16+i)))
        


        # Add eBGP sessions
        ebgp_session(self, r[2], r[1], link_type=CLIENT_PROVIDER)
        ebgp_session(self, r[1], r[3], link_type=CLIENT_PROVIDER)
        ebgp_session(self, r[3], r[4], link_type=CLIENT_PROVIDER)
        ebgp_session(self, r[2], r[5], link_type=CLIENT_PROVIDER)
        ebgp_session(self, r[4], r[7], link_type=CLIENT_PROVIDER)
        ebgp_session(self, r[7], r[6], link_type=CLIENT_PROVIDER)
        ebgp_session(self, r[7], r[8], link_type=CLIENT_PROVIDER)
        
        ebgp_session(self, r[2], r[3], link_type=SHARE)
        ebgp_session(self, r[4], r[5], link_type=SHARE)
        ebgp_session(self, r[5], r[6], link_type=SHARE)
        ebgp_session(self, r[8], r[6], link_type=SHARE)
        
            

            
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
