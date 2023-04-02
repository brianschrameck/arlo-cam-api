import socket
import json

from arlo.messages import Message


class ArloSocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, message):
        self.sock.sendall(message.toNetworkMessage())

    def receive(self):
        chunk = self.sock.recv(1024)
        if chunk == b'':
            return None

        data = chunk.decode(encoding="utf-8")
        if data.startswith("L:"):
            delimiter = data.index(" ")
            dataLength = int(data[2:delimiter])
            json_data = data[delimiter+1:delimiter+1+dataLength]
        else:
            return None

        read = len(json_data)
        while read < dataLength:
            to_read = min(dataLength - read, 1024)
            chunk = self.sock.recv(to_read)
            if chunk == b'':
                return None
            chunk_str = chunk.decode(encoding="utf-8")
            json_data += chunk_str
            read = read + len(chunk_str)

        return Message(json.loads(json_data))

    def close(self):
        self.sock.close()
