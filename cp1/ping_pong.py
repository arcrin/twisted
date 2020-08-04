import socket
import errno
import select


class Reactor(object):
    def __init__(self):
        self._readers = set()
        self._writers = set()

    def addReader(self, transport):
        self._readers.add(transport)

    def addWriter(self, transport):
        self._writers.add(transport)

    def removeReader(self, readable):
        self._readers.discard(readable)

    def removeWriter(self, writable):
        self._writers.discard(writable)

    def run(self):
        while self._readers or self._writers:
            r, w, _ = select.select(self._readers, self._writers, [])
            for readable in r:
                readable.doRead()
            for writable in w:
                if writable in self._writers:
                    writable.doWrite()


class PingPongProtocol(object):
    def __init__(self, identity, maximum=None):
        self._identity = identity
        self._received = 0
        self._maximum = maximum

    def makeConnection(self, transport):
        self.transport = transport
        self.transport.write(b'*')

    def dataReceived(self, data):
        self._received += len(data)
        if self._maximum is not None and self._received >= self._maximum:
            print(self._identity, "is closing the connection")
            self.transport.loseConnection()
        else:
            self.transport.write(b'*')
            print(self._identity, "wrote a byte")

    def connectionLost(self, exceptionOrNone):
        print(self._identity, "lost the connection:", exceptionOrNone)


class Transport(object):
    def __init__(self, reactor, sock, protocl):
        self._reactor = reactor
        self._socket = sock
        self._protocol = protocl
        self._buffer = b''
        self._onCompletion = lambda: None

    def doWrite(self):
        if self._buffer:
            try:
                written = self._socket.send(self._buffer)
            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    self._tearDown(e)
                return
            else:
                print("Wrote", written, 'bytes')
                self._buffer = self._buffer[written:]

        if not self._buffer:
            self._reactor.removeWriter(self)
            self._onCompletion()

    def doRead(self):
        data = self._socket.recv(1024)
        if data:
            self._protocol.dataReceived(data)
        else:
            self._tearDown(None)

    def fileno(self):
        return self._socket.fileno()

    def write(self, data):
        self._buffer += data
        self._reactor.addWriter(self)
        self.doWrite()

    def loseConnection(self):
        if self._buffer:
            def complete():
                self._tearDown(None)
            self._onCompletion = complete
        else:
            self._tearDown(None)

    def _tearDown(self, exceptionOrNone):
        self._reactor.removeWriter(self)
        self._reactor.removeReader(self)
        self._socket.close()
        self._protocol.connectionLost(exceptionOrNone)

    def activate(self):
        self._socket.setblocking(False)
        self._protocol.makeConnection(self)
        self._reactor.addReader(self)
        self._reactor.addWriter(self)


class Listener(Transport):
    def activate(self):
        self._reactor.addReader(self)

    def doRead(self):
        server, _ = self._socket.accept()
        protocol = PingPongProtocol("Server")
        Transport(self._reactor, server, protocol).activate()


listenerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenerSock.bind(('127.0.0.1', 0))
listenerSock.listen(1)
clientSock = socket.create_connection(listenerSock.getsockname())

loop = Reactor()
Listener(loop, listenerSock, None).activate()
Transport(loop, clientSock, PingPongProtocol("Client", maximum=100)).activate()
loop.run()