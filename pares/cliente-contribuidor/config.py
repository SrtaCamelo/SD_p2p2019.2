# arquivo de comfiguracao do servidor

import socket
#import save

LOGIN = "DickVigarista"
SENHA = "6666"

my_name = "Meu PC"


host_name = socket.gethostname()

my_host = socket.gethostbyname(host_name)
my_port = 8002

server_host = "9.0.0.1"
server_host = "10.242.187.161"
server_port = 8001

threads_disponiveis = 2
