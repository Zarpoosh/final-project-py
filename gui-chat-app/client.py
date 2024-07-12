import threading
import socket
import argparse
import os
import sys
import tkinter as tk


class Send(threading.Thread):
    # listening for user input from command line
    
    # sock the connected sock object
    # name (dtr) : the username provided by theusr


    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        
    def run(self):
        while True:
            print("{}: ".format(self.name), end="" )
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            
            # if we type "quite we leave the chatroome"
            
            if message=="Quit":
                self.sock.sendall("Server:{} has left the chat.".format(self.name).encode("ascii") )
                break
            else:
                self.sock.sendall("{}: {} ".format(self.name, message).encode("ascii") )
        print("\nQuiting...")
        self.sock.close()
        os.sock.close()
        os.exit(0)
        

class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.message = None
    
    def run(self):
        while True:
            message = self.sock.recv(1024).decode("ascii")

            if message:
                if self.messages:
                    self.message.insert(tk.END , message)
                    print("hi")
                    print("\r{} \n{}:".format(message, self.name), end="")
                
                else:
                    print("\r{} \n{}:".format(message, self.name), end="")
            else:
                print("\n no we have lost connection to the server!")
                print("\n Quiting...")
                self.sock.close()
                os.exit(0)
                
                
                
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name=None
        self.message = None
    
    def start(self):
        print("trying to connect to {}:{} ...".format(self.host, self.port))
        self.sock.connect((self.host,self.port))
        
        print("successfully connected to {}:{} ...".format(self.host,self.port))
        
        print()
        
        self.name=input("your name...")
        
        print()
        print("welcome , {}! getitng ready to send and receive messages...".format(self.name))
        
        
        # create send and receive threads
        
        send =Send(self.sock,self.name)
        receive=Receive(self.sock,self.name)
        
        
        
        send.start()
        receive.start()
        
        self.sock.sendall("Server :{} has join to chat.say whatsup!".format(self.name).encode("ascii"))
        
        print("\r Ready to chat . leave the chatroom anytime by typing 'QUIT' \n")
        print('{} : '.format(self.name),end='')
        
        return receive
    
    def send(self, textInput):
        message=textInput.get()
        textInput.delete(0,tk.END)
        self,message.insert(tk.END,'{}: {}' . format(self.name, message))
        
        if message=="QUIT" :
            self.sock.sendall('Server : {} has left the chat.' .format(self.name).encode("ascii"))
            
            print("\n Quiting...")
            self.sock.close()
            os.exit(0)
            
        
        # send mesage to the server for broadcast
        else:
            self.sock.sendall("{} :{}".format(self.name, message).encode("ascii"))
   

def main(host, port):
    # initialize and run gui applicaiton
    
    client=Client(host, port)
    receive=client.start()
    
    
    window=tk.Tk()
    window.title("Chatroom")
    
    fromMessage=tk.Frame(master=window)
    scrollBar=tk.Scrollbar(master=fromMessage)
    messages=tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set())
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y ,expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH ,expand=True)
    
    
    client.messages=messages
    receive.messages=messages
    
    fromMessage.grid(row=0 ,column=0, columnspan=2, sticky="nsew")
    fromEntry=tk.Frame(master=window)
    textInput=tk.Entry(master=fromEntry)
    
    textInput.pack(fill=tk.BOTH, expand=True)
    
    textInput.bind("<Return>" , lambda x: client.send(textInput))
    textInput.insert(0, "write your message here.")
    
    btnSend=tk.Button(
        master=window,
        text="Send",
        command=lambda : client.Send(textInput)
        )
    fromEntry.grid(row=1 , column=0, padx=10, sticky="ew")
    btnSend.grid(row=1 , column=0, padx=10, sticky="ew")
    
    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure (0, minsize=500, weight=1)
    window.columnconfigure (1, minsize=200, weight=0)
    
    window.mainloop()
    
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument("host", help="interface to server listens at")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="TCP port(default 1060 )")
    
    args=parser.parse_args()
    
    main(args.host, args.p)