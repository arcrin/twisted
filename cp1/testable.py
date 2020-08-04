from cp1.ping_pong import PingPongProtocol
import unittest
import io


class BytesTransport(object):
    def __init__ (self, protocol):
        self.protocol = protocol
        self.output = io.BytesIO()

    def write(self, data):
        self.output.write(data)

    def loseConnection(self):
        self.output.close()
        self.protocol.connectionLost(None)


class PingPongProtocolTests(unittest.TestCase):
    def setUp(self):
        self.maximum = 100
        self.protocol = PingPongProtocol("client", maximum=self.maximum)
        self.transport = BytesTransport(self.protocol)
        self.protocol.makeConnection(self.transport)

    def testfirstByteWritten(self):
        self.assertEqual(len(self.transport.output.getvalue()), 1)

    def testbyteWrittenForByte(self):
        self.protocol.dataReceived(b"*")
        self.assertEqual(len(self.transport.output.getvalue()), 2)

    def testreceivingMaximumLosesConnection(self):
        self.protocol.dataReceived(b"*" * self.maximum)
        self.assertTrue(self.transport.output.closed)


if __name__ == '__main__':
    unittest.main()