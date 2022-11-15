from mininet.topo import Topo
class customTopo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip ='192.0.1.1' )
        h2 = self.addHost('h2', ip ='192.0.1.2 )
        router = self.addNode('r1', cls=LinuxRouter, ip='193.0.1.1')