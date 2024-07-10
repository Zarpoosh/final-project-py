import threading
import socket
import argparse
import so

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections=[]
        self.host=host
        self.port=port
    def run(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        
        sock.listen(1)
        print("listening", sock.getsockname())
        
        while True:
            # accepting new connections
            sc, socket=sock.accept()
            print(f"accepting a new connections from{sc.getpeername()} to P{sc.sockname()}")
            
            
            #  cretae a new threads
            server_socket=ServerSocket(sc, sockname, self)
            
            
            # start new threads
            server_socket.start()
            
            
            # add threads to active connectionss
            self.connections.append(server_socket)
            print("ready to recive messsage from" , sc.getpeername())
            
    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.sockname != source:
                connection.sockname(message)
    
    def remove_connection(self, connection):
        self.connections.remove(connection)