from autobahn.twisted.util import sleep
from autobahn.twisted.websocket import (WebSocketClientProtocol, WebSocketClientFactory)
from twisted.internet.defer import Deferred, inlineCallbacks
import uuid


class ChatClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        print(response.peer)

    def onOpen(self):
        print("Connected to server")

    def onMessage(self, payload, isBinary):
        print("Some message received from server")

    def onClose(self, wasClean, code, reason):
        print("Disconnected from server")


if __name__ == '__main__':
    from twisted.internet import reactor

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = ChatClientProtocol

    reactor.connectTCP(u"127.0.0.1", 9000, factory)
    reactor.run()