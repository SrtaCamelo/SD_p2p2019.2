import socket
import threading
from config import * #abre asconfiguracoes
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
        otra = False
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
            if otra:
                #se comunica com todos os vizinhos.
                pass

class PeerServer(Receiver):
    def __init__(self,my_host,my_port,sender,col, emp, con):
        threading.Thread.__init__(self, name="Server")
        self.host = my_host
        self.port = my_port
        self.sender = sender
        self.col = col
        self.emp = emp
        self.con = con
        self.sessao_col = {}
        self.sessao_emp = {}

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))

        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            datas = data.decode()
            print ("received message:", addr, datas)

            operacao = datas.split()[0]

            # O cliente inicia a comunicacao
            if operacao == 'Hello':
                self.sender.host = addr[0]
                self.sender.port = int(datas.split()[-1])
                print(self.sender.port)
                #time.sleep(2)
                self.sender.message = "%i"%public

                ### todas as mensagens vao terminar com a porta destino

            # O Server manda a chave publica se as credenciais forem validas
            elif operacao == 'ACESSCON:':
                login = datas.split()[1]
                senha = datas.split()[2]
                
                col_user = self.col.loc[login]
                col_senha = col_user[0]

                print(senha, col_senha)
                
                if senha == col_senha:
                    self.sender.host = addr[0]
                    self.sender.port = int(datas.split()[-1])
                    self.sender.message = "OKAY!"

                    th = datas.split()[3]
                    porta = datas.split()[-1]
                    indice = addr[0]
                    projetos = self.col.loc[login].tolist()
                    
                    self.sessao_col[indice] = [login, porta, th, projetos]

                print(self.sessao_col)


            elif operacao == "ACESSEMP:":
                pass
                    

            elif datas == "ESTOU TE ESPERANDO!!!":
                #reenvia as informacoes do empregador, ou nao faz nada
                pass

            # O Empregador pede novas maquinas
            elif operacao == 'BEG!':
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
