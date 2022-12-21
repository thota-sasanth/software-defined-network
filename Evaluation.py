from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import Node

class LinuxRouter(Node):
    
    def terminate(self):
        
        self.cmd('sysctl net.ipv4.ip_forward=0')

        
        super(LinuxRouter,self).terminate()
    def config(self, **params):
        super(LinuxRouter,self).config(**params)
        
        self.cmd('sysctl net.ipv4.ip_forward=1')

class MyTopo(Topo):
    def build(self, *args, **params):

        
        h1 = self.addHost('h1', ip='190.0.1.1/16')
        h2 = self.addHost('h2', ip='195.0.1.1/16')

        
        r1 = self.addNode('r1', cls=LinuxRouter,ip=None)
        r2 = self.addNode('r2', cls=LinuxRouter,ip=None)

        
        r3 = self.addNode('r3', cls=LinuxRouter,ip=None)
        r4 = self.addNode('r4', cls=LinuxRouter,ip=None)


        
        self.addLink(h1, r1, intfName1 = 'h1-eth1',params1={"ip":"190.0.1.1/16"},  intfName2='r1-eth1',params2={ "ip" : "190.0.1.2/16" })
        self.addLink(r1, r2, intfName1 = "r1-eth2",params1 = {"ip":"191.0.1.1/16"}, intfName2='r2-eth2', params2={ 'ip' : '191.0.1.2/16' } )

        
        self.addLink(r1, r3,  intfName1='r1-eth3',params1={ 'ip' : '192.0.1.1/16' }, intfName2 = "r3-eth3",  params2 = {"ip":"192.0.1.2/16"},)
        self.addLink(r2, r4, intfName1="r2-eth4", params1 = {"ip":"193.0.1.1/16"},  intfName2='r4-eth4',params2 = {"ip":"193.0.1.2/16"})
        
        self.addLink(r3, r4, intfName1='r3-eth5',params1={ 'ip' : '194.0.1.1/16' }, intfName2 = "r4-eth5",params2 = {"ip":"194.0.1.2/16"} )


        
        self.addLink(r4, h2, intfName1 = "r4-eth6",params1 = {"ip":"195.0.1.2/16"},  intfName2 = "h2-eth6", params2 = {"ip":"195.0.1.1/16"})
    

my_net = Mininet(topo=MyTopo())

my_net["h1"].cmd("ip route add default via 190.0.1.2 dev h1-eth1")

my_net["r3"].cmd('ip route add default via 194.0.1.2 dev r3-eth5')


my_net["r3"].cmd('ip route add 190.0.0.0/16 via 192.0.1.1 dev r3-eth3')
my_net["r3"].cmd('ip route add 191.0.0.0/16 via 192.0.1.1 dev r3-eth3')

my_net["r4"].cmd('ip route add default via 193.0.1.1 dev r4-eth4')
my_net["r4"].cmd('ip route add 192.0.0.0/16 via 194.0.1.1 dev r4-eth5')



my_net["r3"].cmd("tc qdisc add dev r3-eth3 root handle 1: tbf rate 100mbit burst 1280  limit 1280 ")
my_net["r3"].cmd("tc qdisc add dev r3-eth5 root handle 1: tbf rate 100mbit burst 1280  limit 1280 ")



my_net["r4"].cmd("tc qdisc add dev r4-eth4 root handle 1: tbf rate 100mbit burst 1280  limit 1280 ")
my_net["r4"].cmd("tc qdisc add dev r4-eth5 root handle 1: tbf rate 100mbit burst 1280  limit 1280 ")

my_net["r4"].cmd("tc qdisc add dev r4-eth6 root handle 1: tbf rate 100mbit burst 1280  limit 1280 ")

my_net["r1"].cmd("tc qdisc add dev r1-eth1 parent 1:1 handle 10: netem delay 30ms")

my_net["r1"].cmd("tc qdisc add dev r1-eth2 parent 1:1 handle 10: netem delay 30ms")
my_net["r1"].cmd("tc qdisc add dev r1-eth3 parent 1:1 handle 10: netem delay 30ms")


my_net["r2"].cmd("tc qdisc add dev r2-eth2 parent 1:1 handle 10: netem delay 30ms")




my_net.start()


CLI(my_net)

my_net.stop()

