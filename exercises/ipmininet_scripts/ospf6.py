# O. Bonaventure, 2019, inspired from IPMininet documentation

import shlex
from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        # Add routers (OSPF daemon is added by default with the default config)

        r1 = self.addRouter("r1")
        r2 = self.addRouter("r2")
        r3 = self.addRouter("r3")
        a = self.addHost("a")
        b = self.addHost("b")

        lr1r2 = self.addLink(r1, r2, igp_cost=1)
        lr1r2[r1].addParams(ip=("2001:db8:1341:12::1/64"))
        lr1r2[r2].addParams(ip=("2001:db8:1341:12::2/64"))

        lr1r3 = self.addLink(r1, r3, igp_cost=5)
        lr1r3[r1].addParams(ip=("2001:db8:1341:13::1/64"))
        lr1r3[r3].addParams(ip=("2001:db8:1341:13::3/64"))

        lr2r3 = self.addLink(r2, r3, igp_cost=3)
        lr2r3[r2].addParams(ip=("2001:db8:1341:23::2/64"))
        lr2r3[r3].addParams(ip=("2001:db8:1341:23::3/64"))
        
        lr1a = self.addLink(r1, a, igp_passive=True)
        lr1a[r1].addParams(ip=("2001:db8:1341:1::1/64"))
        lr1a[a].addParams(ip=("2001:db8:1341:1::A/64"))

        lr3b = self.addLink(r3, b, igp_passive=True)
        lr3b[r3].addParams(ip=("2001:db8:1341:3::3/64"))
        lr3b[b].addParams(ip=("2001:db8:1341:3::B/64"))


        super(MyTopology, self).build(*args, **kwargs)

    def post_build(self, net):
        for r in self.routers():
            command="/usr/sbin/tcpdump --immediate-mode -c 100 -w ./"+r+"-trace.pcap proto ospf"
            p = net[r].popen(shlex.split(command))
            print("launched "+r+" "+command)
            
        super(MyTopology, self).post_build(net)

net = IPNet(topo=MyTopology(), allocate_IPs=False)  # Disable IP auto-allocation
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
