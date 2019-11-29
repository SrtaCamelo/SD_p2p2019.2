import threading

class Receiver(threading.Thread):

    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.host = my_host
        self.port = my_port
        self.chamadas = {}

    def listen(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))

        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print ("received message:", data)

    def run(self):
        self.listen()

class PeerColab(Receiver):
    def __init__(self,sock,th,sender):
        threading.Thread.__init__(self, name="Colab_%i"%th)
        self.sock = sock
        self.sender = sender

    def listen(self):
        while True:
            try:
                
                pass
            except:
                pass
