from autobahn.twisted.websocket import (WebSocketServerProtocol, WebSocketServerFactory)
import uuid


class EchoServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        """
        Called when a client is connecting to us
        :param request:
        :return:
        """
        print(u"Client connection: {0}".format(request.peer))

    def onOpen(self):
        """
        Called when the WebSocket connection has been opened
        :return:
        """
        print(u"WebSocket connection open")

    def onMessage(self, payload, isBinary):
        """
        Called for each WebSocket message received from this client
        :param payload (str/bytes) : the content of the message
        :param isBinary (bool) : wether the message contains (False) encoded text or non-textual data (True).
                Default is False)
        :return:
        """
        # Simply prints any message we receive
        if isBinary:
            # This is a binary message and can contain pretty much anything
            # Here we recreate the UUID from the bytes the client sent us
            uid = uuid.UUID(bytes=payload)
            print(u"UUID received: {}".format(uid))
        else:
            # This is encoded text. Please note that it is NOT decoded for you,
            # isBinary is merely a courtesy flag manually set by the client
            # on each message. You must know the charset used (here utf8),
            # and call ".decode ()" on the butes object to get a string object.
            print(u"Text message received: {}".format(payload.decode('utf8')))
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        """
        Called when the WebSocket connection for this client closes
        :param wasClean:
        :param code:
        :param reason:
        :return:
        """
        print(u"WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    from twisted.internet import reactor
    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = EchoServerProtocol

    print(u"Listening on ws://127.0.0.1:9000")
    reactor.listenTCP(9000, factory)
    reactor.run()
