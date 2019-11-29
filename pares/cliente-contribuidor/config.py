# arquivo de comfiguracao do servidor

import socket
#import save

LOGIN = "DickVigarista"
SENHA = "6666"

my_name = "Meu PC"


host_name = socket.gethostname()

my_host = socket.gethostbyname(host_name)
#my_host = "192.168.25.8"
#my_host = "10.242.187.161"
#my_host = "10.242.185.37"
#my_host = "10.246.29.135"
my_host = "10.248.224.98" #IP DO PC DE PEDRO


my_port = 8002

server_host = "9.0.0.1"
#server_host = "10.242.187.161"
#server_host = "10.242.185.37" #Predo
#server_host = "10.246.227.101"
server_host = "10.248.224.98" #IP DO PC DE PEDRO

server_port = 8001

threads_disponiveis = 2
