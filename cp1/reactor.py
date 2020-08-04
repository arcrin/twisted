import select
import socket


class Reactor(object):
    def __init__(self):
        self._readers = {}
        self._writers = {}

    def addReader(self, readable, handler):
        self._readers[readable] = handler

    def addWriter(self, writable, handler):
        self._writers[writable] = handler

    def removeReader(self, readable):
        self._readers.pop(readable, None)

    def removeWriter(self, writable):
        self._writers.pop(writable, None)

    def run(self):
        while self._readers or self._writers:
            r, w, _ = select.select(list(self._readers), list(self._writers), [])
            for readable in r:
                self._readers[readable](self, readable)
            for writable in w:
                if writable in self._writers:
                    self._writers[writable](self, writable)


class BuffersWrites(object):
    def __init__(self, dataToWrite, onCompletion):
        self._buffer = dataToWrite
        self._onCompletion = onCompletion

    def bufferingWrite(self, reactor, sock):
        if self._buffer:
            try:
                written = sock.send(self._buffer)
            except socket.error as e:
                if e.errno != 10035:
                    raise
                return
            else:
                print("Wrote", written, "bytes")
                self._buffer = self._buffer[written:]
        if not self._buffer:
            reactor.removeReader(sock)
            self._onCompletion(reactor, sock)


def accept(reactor, listener):
    server, _ = listener.accept()
    reactor.addReader(server, read)


def read(reactor, sock):
    data = sock.recv(1024)
    if data:
        print("Server received", len(data), " bytes.")
    else:
        sock.colose()
        print("Server closed.")
        reactor.removeReader(sock)


DATA = [b"*", b"*"]


def write(reactor, sock):
    writer = BuffersWrites(b"".join(DATA), onCompletion=write)
    reactor.addWriter(sock, writer.bufferingWrite)
    print("Client buffering", len(DATA), "bytes to write.")
    DATA.extend(DATA)


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1', 0))
listener.listen(1)
client = socket.create_connection(listener.getsockname())
client.setblocking(False)

loop = Reactor()
loop.addWriter(client, write)
loop.addReader(listener, accept)
loop.run()