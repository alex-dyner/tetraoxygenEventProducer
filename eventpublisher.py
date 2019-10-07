
import socket

class EventPublisher:
    _message_properties = ["product_name", "price", "purchase_date", "product_category", "ip"]

    def __init__(self, config):
        self._hostname = config["hostname"]
        self._port = config["port"]

    def init(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._hostname, self._port))

    def publish(self, event):
        raw_message = ""
        for p in self._message_properties:
            raw_message += "," + str(event.get(p))
        
        message = raw_message[1:] + "\n"
        self._socket.send(message.encode())

    def close(self):
        self._socket.shutdown(socket.SHUT_WR)
        self._socket.close()
