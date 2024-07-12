# import socket
# import sqlite3

# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind the socket to a address and port
# server_address = ('localhost', 10000)
# sock.bind(server_address)

# # Create a SQLite database connection
# db = sqlite3.connect('chat.db')
# cursor = db.cursor()

# # Create a table to store messages
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS messages (
#         id INTEGER PRIMARY KEY,
#         sender TEXT,
#         receiver TEXT,
#         message TEXT
#     )
# ''')
# db.commit()

# print('Server started. Waiting for messages...')

# while True:
#     # Receive a message from a client
#     data, address = sock.recvfrom(1024)
#     message = data.decode('utf-8')
#     sender, receiver, message = message.split(':')

#     # Store the message in the database
#     cursor.execute('''
#         INSERT INTO messages (sender, receiver, message)
#         VALUES (?, ?, ?)
#     ''', (sender, receiver, message))
#     db.commit()

#     # Send the message to the receiver
#     sock.sendto(message.encode('utf-8'), address)

#     print(f'Received message from {sender}: {message}')

import socket
import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading


class ChatServer:
    def __init__(self, master):
        self.master = master
        self.master.title('Chat Server')
        self.master.geometry('300x400')

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to an address and port
        self.server_address = ('localhost', 10000)
        self.sock.bind(self.server_address)

        # Create a SQLite database connection
        self.db = sqlite3.connect('chat.db')
        self.cursor = self.db.cursor()

        # Create a table to store messages
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                receiver TEXT,
                message TEXT
            )
        ''')
        self.db.commit()

        # Create GUI components
        self.sender_label = tk.Label(master, text='Sender:')
        self.sender_label.pack()

        self.sender_entry = tk.Entry(master, width=20)
        self.sender_entry.pack()

        self.receiver_label = tk.Label(master, text='Receiver:')
        self.receiver_label.pack()

        self.receiver_entry = tk.Entry(master, width=20)
        self.receiver_entry.pack()

        self.message_label = tk.Label(master, text='Message:')
        self.message_label.pack()

        self.message_text = tk.Text(master, width=20, height=10)
        self.message_text.pack()

        self.send_button = tk.Button(master, text='Send', command=self.send_message)
        self.send_button.pack()

        self.clients_label = tk.Label(master, text='Clients:')
        self.clients_label.pack()

        self.clients_list = tk.Listbox(master, width=20)
        self.clients_list.pack(fill=tk.BOTH, expand=True)

        self.clients = {}

        self.start_receiving_thread()

    def send_message(self):
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        message = self.message_text.get('1.0', 'end-1c')

        # Send the message to the receiver
        self.sock.sendto(f'{sender}:{message}'.encode('utf-8'), self.clients[receiver])

        # Clear the message text
        self.message_text.delete('1.0', 'end')

    def receive_message(self):
        db = sqlite3.connect('chat.db')
        cursor = db.cursor()

        while True:
            # Receive a message from a client
            data, address = self.sock.recvfrom(1024)
            message = data.decode('utf-8')
            sender,receiver, message = message.split(':')
            
            
            # # Display the received message
            # self.messages_list.insert(tk.END, f'{sender}: {received_message}')


            # Store the message in the database
            cursor.execute('''
                INSERT INTO messages (sender, receiver, message)
                VALUES (?, ?, ?)
            ''', (sender, receiver, message))
            db.commit()

            # Register clients
            if sender not in self.clients:
                self.clients[sender] = address
            if receiver in self.clients:
                # Send the message to the receiver
                self.sock.sendto(f'{sender}:{message}'.encode('utf-8'), self.clients[receiver])

            # Update the clients list
            self.clients_list.delete(0, tk.END)
            for client in self.clients.keys():
                self.clients_list.insert(tk.END, client)

            print(f'Received message from {sender} to {receiver}: {message}')

    def start_receiving_thread(self):
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.daemon = True
        receive_thread.start()

root = tk.Tk()
server = ChatServer(root)
root.mainloop()