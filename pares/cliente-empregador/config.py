# arquivo de comfiguracao do servidor

import socket
#import save

PROJETO = "calculos"
LOGIN = "TomasTurbando"
SENHA = "14785236987412369852147"

my_name = "O K RA"


host_name = socket.gethostname()

my_host = socket.gethostbyname(host_name)
my_host = "10.242.187.161"
#my_host = "10.246.29.135"
my_port = 8100

#server_host = "9.0.0.1"
server_host = "10.242.187.161"
server_host = "10.242.185.37" #Predo
#server_host = "10.246.227.101"
server_port = 8001

files = ["operacoes.py"]
