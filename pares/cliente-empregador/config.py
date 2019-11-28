# arquivo de comfiguracao do servidor

import socket
#import save

PROJETO = "calculos"
LOGIN = "TomasTurbando"
SENHA = "14785236987412369852147"

my_name = "O K RA"


host_name = socket.gethostname()

my_host = socket.gethostbyname(host_name)
my_port = 8008

server_host = "9.0.0.1"
server_port = 8001

threads_disponiveis = 2
