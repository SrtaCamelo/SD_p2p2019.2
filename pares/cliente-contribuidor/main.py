import socket
import threading
from config import * #abre as configuracoes
import pandas as pd

import PEER

ENCODING = 'utf-8'





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
        ## Aqui eh guardada o numero de controle e a resposta
        self.tarefas = {}

    def run(self):
        while True:
            if self.message != "":
                message = bytes(self.message, 'utf-8')
                print(self.message)
                try:
                    self.sock.sendto(message, (self.host, self.port))
                except ValueError:
                    print("erro")
                    #print(ValueError)
                self.message = ""



class ColabStart(Receiver):
    def __init__(self,sock,sender,login,senha):
        threading.Thread.__init__(self, name="Starter")
        self.sock = sock
        self.sender = sender

    def listen(self):

        esp = True
        self.sock.settimeout(5)
        #self.sender.message = "HELLO!"
        myaddr = self.sock.getsockname()[1]
        print(myaddr)
        
        while esp:
            try:
                #Envia a porta e espera a chave publica
                self.sender.message = "Hello port %i"%myaddr
                data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
                print ("received message:", addr, data)
                
                if (addr[0] == server_host):
                    esp = False
            except:
                print("timeout")

        esp = True

        while esp:
            try:
                #Envia "ACESS: login senha threads porta"
                mensagem = "ACESSCON: %s %s %i %s"%(LOGIN, SENHA, threads_disponiveis, myaddr)
                self.sender.message = mensagem

                data, addr = self.sock.recvfrom(1024)

                #Recebe a confirmacao ou gera timeout
                if addr[0]==self.sender.host:
                    esp = False
            except:
                print("Senha errada!")

        esp = True
        self.sock.settimeout(20)

        while esp:
            try:
                #espera a alocacao
                data, addr = self.sock.recvfrom(1024)

                data = data.decode()
                print("printando decode")
                print(data)
                if addr[0]==self.sender.host:
                    if data == "ONDE ESTA AGORA?":
                        self.sender.message = 'AMIGO EU ESTOU AQUI!'
                    elif data.split("!")[0] == "LET IT GO":
                        #Extraí o IP e a Porta do Empregador
                        self.sender.host = data.split()[-2]
                        self.sender.port = int(data.split()[-1])
                        message = "Conexao realizada com sucesso"
                        message = bytes(message, 'utf-8')
                        self.sender.sock.sendto(message, (data.split()[-2],int(data.split()[-1])))

                        esp = False
            except:
                self.sender.message = "ESTOU TE ESPERANDO!!!"
                print("nao sei")
                
        esp = True

        #recebe o(os) script(s)
        while esp:
            try:
                
                # espera a alocacao
                data, addr = self.sock.recvfrom(1024)
                datas = data.decode()


            except:
                print("Tiem ot")
        #Espera o arquivo
        #salva o .py

    def run(self):
        self.listen()



def main(my_host,my_port,server_host,server_port,login,senha):
    print("@:\t\t", my_host)
    print("port:\t\t", my_port)

    #Aqui eh gerada a unica porta para enviar informacao
    sender = Sender()
    sender.start()
    sender.host = server_host
    sender.port = server_port

    #Aqui sao gerados os sockets para receber mensagens
    sock = []
    for i in range(threads_disponiveis):
        a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        a.bind((my_host, my_port+i))
        sock.append(a)

    #Aqui o colaborador faz o startup
    svcom = ColabStart(sock[0],sender,login,senha)
    svcom.listen()
    #svcom.start()

    #O .py com as funcoes eh importado aqui

    #Sao gerados os i threads da aplicacao
    for i in sock:
        #Um objeto da classe PeerColab() eh declarado
        print(i)

def makehost(my_host, my_port):
    receiver = Receiver(my_host, my_port)
    oh = receiver.start()
    return oh

th = None

if __name__ == '__main__':
    main(my_host,my_port,server_host,server_port,LOGIN,SENHA)
    print()
