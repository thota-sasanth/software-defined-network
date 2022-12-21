from mininet.node import Node
from mininet.net import Mininet
from contextlib import contextmanager
from mininet.topo import Topo
from mininet.cli import CLI
import os

class Router(Node):
    
    @contextmanager
    def in_router_dir(self):

        
        working_dir = os.getcwd()
        self.cmd('cd %s' % self.name)

        
        yield
        
        self.cmd('cd %s' % working_dir) 
    

class MyTopo(Topo):
    def build(self, *args, **params):

        h1 = self.addHost( 'h1', ip='190.0.1.1/16',cls=Router)
        h2 = self.addHost( 'h2', ip='195.0.1.1/16',cls=Router)

        
        r1 = self.addNode( 'r1', cls=Router, ip=None )
        r2 = self.addNode( 'r2', cls=Router, ip=None)
        r3 = self.addNode( 'r3', cls=Router, ip=None )

        
        r4 = self.addNode( 'r4', cls=Router, ip=None)
        
        self.addLink(h1, r1, intfName1 = 'h1-eth1',params1={"ip":"190.0.1.1/16"},  intfName2='r1-eth1',params2={ "ip" : "190.0.1.2/16" })
        self.addLink(r1, r2, intfName1 = "r1-eth2",params1 = {"ip":"191.0.1.1/16"}, intfName2='r2-eth2', params2={ 'ip' : '191.0.1.2/16' } )

        
        self.addLink(r1, r3,  intfName1='r1-eth3',params1={ 'ip' : '192.0.1.1/16' }, intfName2 = "r3-eth3",  params2 = {"ip":"192.0.1.2/16"})
        
        self.addLink(r2, r4, intfName1="r2-eth4", params1 = {"ip":"193.0.1.1/16"},  intfName2='r4-eth4',params2 = {"ip":"193.0.1.2/16"})
        self.addLink(r3, r4, intfName1='r3-eth5',params1={ 'ip' : '194.0.1.1/16' }, intfName2 = "r4-eth5",params2 = {"ip":"194.0.1.2/16"} )


        
        self.addLink(r4, h2, intfName1 = "r4-eth6",params1 = {"ip":"195.0.1.2/16"},  intfName2 = "h2-eth6", params2 = {"ip":"195.0.1.1/16"})
        

my_net = Mininet(topo=MyTopo())




my_net.start()
CLI(my_net)

my_net.stop()
