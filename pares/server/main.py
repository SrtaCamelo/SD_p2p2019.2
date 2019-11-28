### todas as mensagens vao terminar com a porta destino
### Nome dos projetos são UNICOS CARALHO

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
                    print(self.host)
                    print(self.port)
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
        self.sessao_col = {} # Sessao Atual do Colaborador
        self.sessao_emp = {} # Sessao Atual do Empregador
        self.sessao_emp_ip = {} # A partir do IP do Empregador tem-se o nome do projeto

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
                # O Server manda a chave publica
                self.sender.message = "%i"%public
               # print(self.sender.host)



            # O server le a mensagem e verifica o login e senha
            # CONLABORADOR
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

                    th = datas.split()[3] # QUANTIDADE DE THRADES
                    porta = datas.split()[-1] # PORTA DO COLABORADOR
                    indice = addr[0] # IP DO COLABORADOR
                    projetos = self.col.loc[login].tolist()[2]
                    
                    self.sessao_col[indice] = [login, porta, th, projetos, ""]

                print(self.sessao_col)

            # Empregador
            elif operacao == "ACESSEMP:":
                login = datas.split()[1]
                senha = datas.split()[2]
                proje = datas.split()[3]
                
                col_user = self.col.loc[login]
                col_senha = col_user[0]

                print(senha, col_senha)
                
                if senha == col_senha:
                    emp_proje = self.emp.loc[proje].to_list()
                    if login == emp_proje[0]:
                        self.sender.host = addr[0]
                        self.sender.port = int(datas.split()[-1])
                        self.sender.message = "OKAY!"

                        #Ainda falta guardar o empregador na tabela self.emp
                        ip_emp = addr[0]
                        porta = datas.split()[-1]
                        self.sessao_emp[proje] = [ip_emp,porta,login,"depois","depois",0,0,0]
                        print(self.sessao_emp)
                    
            # COLABORADOR
            elif datas == "ESTOU TE ESPERANDO!!!":
                # reenvia as informacoes do empregador, ou nao faz nada
                # O Server Encontra na secao atual dos colaborados qual projeto esta alocado e envia confirmacao caso exista para Coloborador
                # Se nao houver nada na secao atual...ele faz porra nenhuma (PASS)
                indice = addr[0]
                print('########## TESTE ############')
                print(self.sessao_col[indice][-1])
                print('########## TESTE ############')
                if self.sessao_col[indice][-1] != "":
                    ip_emp = self.sessao_emp[self.sessao_col[indice][-1]][0]
                    porta = self.sessao_emp[self.sessao_col[indice][-1]][1]
                    self.sender.message = "LET IT GO! " + ip_emp + " " + str(porta)
                else:
                    print("FAZENDO PORRA NENHUMA E SE FODA VOCE!!!")
                    pass

            # O Empregador pede novas maquinas
            elif operacao == 'BEG!':
                # atualiza o cliente para ele se comunicar com o server
                # Mandar o IP e as POrtas do Colaborador para o EMpregador, com a finalidade de criar comunicao entre eles
                ip_emp = addr[0]
                nome_projeto = datas.split()[1]
                porta_emp = datas.split()[-1]
                ip_col = busca_ipColaborador(self.sessao_col,nome_projeto)
                th_col = self.sessao_col[ip_col][2]
                porta_col = self.sessao_col[ip_col][1]
                # "LET IT GO! IP_COL TH_COL PORTA_COL"
                print("################# TESTE2 ###############")
                print("LET IT GO! " + ip_col + " " + str(th_col) + " " + porta_col)
                print("################# TESTE2 ###############")
                self.sender.host = ip_emp
                self.sender.port = int(porta_emp)
                self.sender.message = "LET IT GO! " + ip_col + " " + str(th_col) + " " + porta_col
                time.sleep(1)
                # O BEG envia para o colaborador um aviso de confirmacao da alocacao e altera a tabela dele para act = "NOME_DO_PROJETO"
                self.sender.host = ip_col
                self.sender.port = int(porta_col)
                self.sender.message = "LET IT GO! %s %s"%(ip_emp,porta_emp)



            # O Server pede a confirmacao dos clientes para manterem logados
            elif datas == 'AMIGO EU ESTOU AQUI!':
                pass


## Essa Funcao busca o Ip do Colaborador a partir do nome do projeto
def busca_ipColaborador(s_col,nom_pro):
    for i in s_col:
        if (nom_pro in s_col[i][3].split()) or "todos" in s_col[i][3].split():
            if s_col[i][4] == "":
                return i

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
