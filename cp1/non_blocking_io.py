import socket, errno

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1', 0))
listener.listen(1)
client = socket.create_connection(listener.getsockname())
server, _ = listener.accept()
server.setblocking(False)

try:
    while True: print(server.send(b"*"*1024))
except socket.error as e:
    print(e)