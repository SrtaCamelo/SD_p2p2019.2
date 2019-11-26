import socket
import threading
from config import * #abre as configuracoes
import pandas as pd
import time

ENCODING = 'utf-8'


def openUsers():
    col = pd.read_csv('colaborador.csv', header = 0)
    col.set_index('usuario', inplace = True)
    emp = pd.read_csv('empregador.csv', header = 0)
    emp.set_index('projeto', inplace = True)
    con = pd.read_csv('controle.csv', header = 0)
    return col, emp, con

def saveUsers():
    pass


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


class Sender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name="messenger_sender")
        self.host = "0.0.0.0"
        self.port = "6666"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.message = ""

    def run(self):
        while True:

            if self.message != "":
                try:
                    message = bytes(self.message, 'utf-8')
                    print(self.message)
                    print(message)
                    self.sock.sendto(message, (self.host, self.port))
                    self.message = ""
                except ValueError:
                    print("erro")
                    #print(ValueError)
                    self.message = ""

class PeerServer(Receiver):
    def __init__(self,my_host,my_port,sender,col, emp, con):
        threading.Thread.__init__(self, name="Server")
        self.host = my_host
        self.port = my_port
        self.sender = sender

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))

        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            datas = data.decode()
            print ("received message:", addr, datas)
            

            # O cliente inicia a comunicacao
            if datas[:5] == 'Hello':
                self.sender.host = addr[0]
                self.sender.port = int(datas.split()[-1])
                print(self.sender.port)
                #time.sleep(2)
                self.sender.message = "%i"%public

            # O Server manda a chave publica se as credenciais forem validas
            elif datas[:6] == 'ACESS:':
                login = datas.split()[1]
                senha = datas.split()[2]
                col_senha = self.col.loc[self.col.iloc[:, -1] == login]["senha"]
                if senha == col_senha:
                    pass

                pass

            # O Empregador pede novas maquinas
            elif datas[:4] == 'BEG!':
                pass

            # O Server pede a confirmacao dos clientes para manterem logados
            elif datas == 'AMIGO EU ESTOU AQUI!':
                pass

def main(my_host,my_port):
    print("@:\t\t", my_host)
    print("port:\t\t", my_port)
    sender = Sender()
    sender.start()

    col, emp, con = openUsers()

    own = PeerServer(my_host,my_port,sender,col, emp, con)
    own.start()

def makehost(my_host, my_port):
    receiver = Receiver(my_host, my_port)
    oh = receiver.start()
    return oh

th = None

if __name__ == '__main__':
    print("Host:\t\t", host_name)
    main(my_host, my_port)
    #ohost = makehost(my_host, my_port)

    co = pd.DataFrame(columns = ["usuario","ip","portas","disponibilidade","projetos","RAM","CPU"])#colaboradores online
    em = pd.DataFrame(columns = ["projeto","ip","porta","orcamento","contrato","colaboradores"])#projetos online
    print()
    #th = vizinhanca()
