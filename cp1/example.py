import socket
import select

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1', 0))
listener.listen(1)
client = socket.create_connection(listener.getsockname())
server, _ = listener.accept()

maybeReadable = [listener, client, server]
maybeWritable = [client, server]
readable, writable, _ = select.select(maybeReadable, maybeWritable, [],0)


