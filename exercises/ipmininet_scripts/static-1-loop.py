from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig, STATIC, StaticRoute
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        # Change the config object for RouterConfig
        # because it does not add by default OSPF or OSPF6
        r1 = self.addRouter("r1", config=RouterConfig)
        r2 = self.addRouter("r2", config=RouterConfig)
        r3 = self.addRouter("r3", config=RouterConfig)
        a = self.addHost("a")
        b = self.addHost("b")

        lr1r2 = self.addLink(r1, r2)
        lr1r2[r1].addParams(ip=("2001:db8:1341:12::1/64"))
        lr1r2[r2].addParams(ip=("2001:db8:1341:12::2/64"))

        lr1r3 = self.addLink(r1, r3)
        lr1r3[r1].addParams(ip=("2001:db8:1341:13::1/64"))
        lr1r3[r3].addParams(ip=("2001:db8:1341:13::3/64"))

        lr2r3 = self.addLink(r2, r3)
        lr2r3[r2].addParams(ip=("2001:db8:1341:23::2/64"))
        lr2r3[r3].addParams(ip=("2001:db8:1341:23::3/64"))
        
        lr1a = self.addLink(r1, a)
        lr1a[r1].addParams(ip=("2001:db8:1341:1::1/64"))
        lr1a[a].addParams(ip=("2001:db8:1341:1::A/64"))

        lr3b = self.addLink(r3, b)
        lr3b[r3].addParams(ip=("2001:db8:1341:3::3/64"))
        lr3b[b].addParams(ip=("2001:db8:1341:3::B/64"))

        # Add static routes
        r1.addDaemon(STATIC, static_routes=[StaticRoute("2001:db8:1341:3::/64", "2001:db8:1341:12::2")])

        r2.addDaemon(STATIC, static_routes=[StaticRoute("2001:db8:1341::/60", "2001:db8:1341:12::1"),
                                            StaticRoute("2001:db8:1341:1::/64", "2001:db8:1341:12::1")])
        
        r3.addDaemon(STATIC, static_routes=[StaticRoute("2001:db8:1341:1::/64", "2001:db8:1341:13::1")])                     

        super(MyTopology, self).build(*args, **kwargs)

net = IPNet(topo=MyTopology(), allocate_IPs=False)  # Disable IP auto-allocation
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
