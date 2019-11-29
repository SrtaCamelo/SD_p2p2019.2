import threading

class Receiver(threading.Thread):

    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.host = my_host
        self.port = my_port

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
                data, addr = sock.recvfrom(1024)
                datas = data.decode()
                meio = datas.find(":")
                controle = datas[:meio]
                funcao = datas[meio:]
                if addr[0] == self.sender.host:
                    if not (controle in self.sender.tarefas):
                        ex = exec(funcao)
                        self.sender.tarefas[controle] = [funcao, ex]
                    if controle in self.sender.tarefas:
                        dest = (self.sender.host, int(self.sender.port))
                        self.sender.sendto(bytes(self.sender.tarefas[controle][1]), dest)
                    else:
                        pass
            except:
                print(vish)
