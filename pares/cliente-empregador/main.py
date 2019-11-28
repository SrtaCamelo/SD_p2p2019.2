import socket
import threading
from config import * #abre as configuracoes
import pandas as pd

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


class FeetchCol(Receiver):
    def __init__(self,sock,sender,server,login,senha):
        threading.Thread.__init__(self, name="Feetch")
        self.sock = sock
        self.sender = sender
        self.server = server #esse eh o thread que envia tarefas para os colaboradores

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
                mensagem = "ACESSEMP: %s %s %s %s"%(LOGIN, SENHA, PROJETO, myaddr)
                self.sender.message = mensagem

                data, addr = self.sock.recvfrom(1024)

                #Recebe a confirmacao ou gera timeout
                if addr[0]==self.sender.host:
                    esp = False
            except:
                print("Senha errada!")

        esp = True
        self.sock.settimeout(5)

        self.server.start()

        #BEG

        modulos = {}

        for i in files:
            with open(i, "rb") as f:
                data = f.readlines()
            modulos[i] = [len(data), data]

        #print(modulos)

        while esp:
            try:
                mensagem = "BEG! %s %i %s"%(PROJETO, self.server.alocados, myaddr)
                self.sender.message = mensagem
                data, addr = self.sock.recvfrom(1024)
                datas = data.decode()
                print(datas)
                if addr[0] == server_host:
                    if datas == "ONDE ESTA AGORA?":
                        self.sender.message = 'AMIGO EU ESTOU AQUI!'
                    elif datas.split("!")[0] == "LET IT GO":
                        col, th, porta = datas.split("!")[1].split()
                        if not(col in self.server.col):
                            th = int(th)
                            porta = int(porta)
                            portas = list(range(porta, porta+th))
                            self.server.alocados += 1
                            self.server.col[col] = {"threads":th, "portas":portas, "tarefas":{}}
                        print(self.server.col)
                elif addr[0] in self.col:
                    if datas.split()[0] in modulos:
                        modulo = datas.split()[0]
                        posicao = int(datas.split()[1])
                        porta = int(datas.split()[-1])
                        self.sender.sendto(modulos[modulo][1][posicao] (addr[0], porta))
                    #O empregador vai transferir o arquivo para o colaborador
                    else:
                        mensagem = ""
                        for i in modulos:
                            mensagem = mensagem + " %s %i"%(i, modulos[i][0])
                        porta = int(datas.split()[-1])
                        self.sender.sendto(bytes(mensagem), (addr[0], porta))
            except:
                print("Time Out")

        #Espera o arquivo
        #salva o .py

    def run(self):
        self.listen()

class PeerEmp(Receiver):
    def __init__(self,sock,sender):
        threading.Thread.__init__(self, name="Empregador")
        self.sock = sock
        self.sender = sender
        self.alocados = 0
        self.col = {} #sessao atual dos colaboradores
        self.trabalhos = {} #trabalhos ja realizados numero:[chamada, resultado]

    def listen(self):
        #o Empregador vai carregar um script e vai processar ele aqui.
        #o parse vai encontrar as definicoes de variaveis e passalas para os colaboradores
        #O parse vai segmentar o que pode ser paralelizavel dentro de um bloco
        #Ao encontrar um prange(), todas as chamadas serao feitas de forma paralela
        script = list(range(1000))
        for i in script:
            while True:
                pass

def main(my_host,my_port,server_host,server_port,login,senha):
    print("@:\t\t", my_host)
    print("port:\t\t", my_port)

    #Aqui eh gerada a unica porta para enviar informacao
    sendera = Sender()
    sendera.start()
    sendera.host = server_host
    sendera.port = server_port

    senderb = Sender()
    senderb.host = server_host
    senderb.port = server_port
    senderb.start()

    #Aqui sao gerados os sockets para receber mensagens dos clientes
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_host, my_port+1))

    svcom = PeerEmp(sock, sendera)
    #svcom.start()

    socksv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socksv.bind((my_host, my_port))

    #Aqui o colaborador faz o startup
    feet = FeetchCol(socksv,senderb,svcom,login,senha)
    #svcom.listen()
    feet.start()

    #Inicia o PeerEmp

    #O .py com as funcoes eh importado aqui

def makehost(my_host, my_port):
    receiver = Receiver(my_host, my_port)
    oh = receiver.start()
    return oh

th = None

if __name__ == '__main__':
    main(my_host,my_port,server_host,server_port,LOGIN,SENHA)
    print()
