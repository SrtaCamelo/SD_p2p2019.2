class PeerColab(Receiver):
    def __init__(self,sock,th,sender):
        threading.Thread.__init__(self, name="Colab_%i"%th)
        self.sock = sock
        self.sender = sender

    def listen(self):
        pass
