from twisted.internet import protocol, reactor
from twisted.trial import unittest
from twisted.internet.testing import StringTransportWithDisconnection, MemoryReactor
import ipaddress as address


class PingPongProtocol(protocol.Protocol):
    def __init__(self):
        self._received = 0

    def connectionMade(self):
        self.transport.write(b"*")

    def dataReceived(self, data):
        self._received += len(data)
        if self.factory._maximum is not None and self._received >= self.factory._maximum:
            print(self.factory._identity, "is closing the connection")
            self.transport.loseConnection()
        else:
            self.transport.write(b'*')
            print(self.factory._identity, "wrote a byte")

    def connectionLost(self, reason=None):
        print(self.factory._identity, "lost the connection:", reason)


class PingPongServerFactory(protocol.Factory):
    protocol = PingPongProtocol
    _identity = "Server"

    def __init__(self, maximum=None):
        self._maximum = maximum


class PingPongClientFactory(protocol.ClientFactory):
    protocol = PingPongProtocol
    _identity = "Client"

    def __init__(self, maximum=None):
        self._maximum = maximum


# listener = reactor.listenTCP(port=0,
#                              factory=PingPongServerFactory(),
#                              interface='127.0.0.1')
# address = listener.getHost()
# reactor.connectTCP(host=address.host,
#                    port=address.port,
#                    factory=PingPongClientFactory(maximum=100))
# reactor.run()

class PingPongProtocolTests(unittest.SynchronousTestCase):
    def setUp(self):
        self.maximum = 100
        self.reactor = MemoryReactor()
        self.factory = PingPongClientFactory(self.maximum)
        self.protocol = self.factory.buildProtocol(address.IPv4Address(
            "TCP","localhost",1234))
        self.transport = StringTransportWithDisconnection()
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol
    def test_firstByteWritten(self):
        self.assertEqual(len(self.transport.value()), 1)
    def test_byteWrittenForByte(self):
        self.protocol.dataReceived(b"*")
        self.assertEqual(len(self.transport.value()), 2)
    def test_receivingMaximumLosesConnection(self):
        self.protocol.dataReceived(b"*" * self.maximum)
        self.assertFalse(self.transport.connected)

