# O. Bonaventure, December 2019, based on the ipmininet examples
import shlex
from ipmininet.iptopo import IPTopo

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI


class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        # Switches with manually set STP priority
        s3 = self.addSwitch("s3", prio=3, lo_addresses=["2001:1::4/64"])
        s4 = self.addSwitch("s4", prio=4, lo_addresses=["2001:1::4/64"])
        s6 = self.addSwitch("s6", prio=6, lo_addresses=["2001:1::6/64"])
        s7 = self.addSwitch("s7", prio=7, lo_addresses=["2001:1::7/64"])
        s9 = self.addSwitch("s9", prio=9, lo_addresses=["2001:1::9/64"])

        # Hub
        #hub1 = self.addHub("hub1")

        # Links
        self.addLink(s3, s9, stp_cost=1)  # Cost changed for both interfaces
        l37=self.addLink(s3, s7)  
        l37[s3].addParams(stp_cost=1) # cost changed for s3->s7
        l37[s7].addParams(stp_cost=1) # cost changed for s7->s3
        self.addLink(s9, s7) # default cost of 1
        self.addLink(s6, s9)
        self.addLink(s6, s4)
        self.addLink(s7, s4)

        super(MyTopology, self).build(*args, **kwargs)



    def post_build(self, net):
        for s in self.switches():
            command="/usr/sbin/tcpdump -i any --immediate-mode -c 50 -w ./stp-"+s+"-trace.pcap stp"
            p = net[s].popen(shlex.split(command))
            
        super(MyTopology, self).post_build(net)
        
    
net = IPNet(topo=MyTopology()) 
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
