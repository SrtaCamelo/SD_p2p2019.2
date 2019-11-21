import socket
import threading
 
ENCODING = 'utf-8'
 
 
class Receiver(threading.Thread):
 
    def __init__(self, my_host, my_port):
        threading.Thread.__init__(self, name="messenger_receiver")
        self.host = my_host
        self.port = my_port


    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.bind((self.host, self.port))
        sock.listen(10)
        while True:
            connection, client_address = sock.accept()
            try:
                full_message = ""
                while True:
                    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                    full_message = full_message + data.decode(ENCODING)
                    if not data:
                        print("{}: {}".format(client_address, full_message.strip()))
                        break
            finally:
                connection.shutdown(2)
                connection.close()
 
    def run(self):
        self.listen()
 
 
class Sender(threading.Thread):
 
    def __init__(self, my_friends_host, my_friends_port):
        threading.Thread.__init__(self, name="messenger_sender")
        self.host = my_friends_host
        self.port = my_friends_port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)  # Change TTL (=20) to suit
        while True:
            message = input("")
            s.sendto(message, (self.host, self.port))
            s.shutdown(2)
            s.close()
 
 
def main():
    my_host = input("which is my host? ")
    my_port = int(input("which is my port? "))
    receiver = Receiver(my_host, my_port)
    my_friends_host = input("what is your friend's host? ")
    my_friends_port = int(input("what is your friend's port?"))
    sender = Sender(my_friends_host, my_friends_port)
    treads = [receiver.start(), sender.start()]
    return [receiver, sender]
 
th = None

if __name__ == '__main__':
    th = main()
