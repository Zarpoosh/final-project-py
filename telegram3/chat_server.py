
import socket
import tkinter as tk
import sqlite3
import threading
from queue import Queue

class ChatServer:
    def __init__(self, master):
        self.master = master
        self.master.title('Chat Server')
        self.master.geometry('400x600')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 10000)
        self.sock.bind(self.server_address)

        self.db = sqlite3.connect('chat.db', check_same_thread=False)
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                receiver TEXT,
                message TEXT
            )
        ''')
        self.db.commit()

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
        self.message_text = tk.Text(master, width=30, height=5)
        self.message_text.pack()

        self.send_button = tk.Button(master, text='Send', command=self.send_message)
        self.send_button.pack()

        self.clients_label = tk.Label(master, text='Chat Page')
        self.clients_label.pack()
        # self.clients_list = tk.Listbox(master, width=30)
        # self.clients_list.pack(fill=tk.BOTH, expand=True)

        # self.messages_label = tk.Label(master, text='Messages:')
        # self.messages_label.pack()
        self.messages_list = tk.Listbox(master, width=30)
        self.messages_list.pack(fill=tk.BOTH, expand=True)

        self.clients = {}
        self.queue = Queue()

        self.start_receiving_thread()
        self.process_queue()

    def send_message(self):
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        message = self.message_text.get('1.0', 'end-1c')

        if receiver in self.clients:
            self.sock.sendto(f'{sender}:{receiver}:{message}'.encode('utf-8'), self.clients[receiver])
            self.save_message(sender, receiver, message)
            self.message_text.delete('1.0', 'end')
        else:
            # Broadcast the message to all clients if no specific receiver
            for client_addr in self.clients.values():
                self.sock.sendto(f'{sender}:{receiver}:{message}'.encode('utf-8'), client_addr)
            self.save_message(sender, receiver, message)
            self.message_text.delete('1.0', 'end')
            self.display_message(sender, message)

    def receive_message(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            message = data.decode('utf-8')
            self.queue.put((message, address))

    def process_queue(self):
        try:
            while not self.queue.empty():
                message, address = self.queue.get()
                sender, receiver, message = message.split(':', 2)
                self.save_message(sender, receiver, message)

                if sender not in self.clients:
                    self.clients[sender] = address

                # Broadcast the message to all clients
                for client_addr in self.clients.values():
                    self.sock.sendto(f'{sender}:{message}'.encode('utf-8'), client_addr)

                # self.update_clients_list()
                self.display_message(sender, message)

            self.master.after(100, self.process_queue)
        except Exception as e:
            print(f"Error processing queue: {e}")

    def save_message(self, sender, receiver, message):
        try:
            self.cursor.execute('''
                INSERT INTO messages (sender, receiver, message)
                VALUES (?, ?, ?)
            ''', (sender, receiver, message))
            self.db.commit()
        except Exception as e:
            print(f"Error saving message: {e}")

    # def update_clients_list(self):
    #     self.clients_list.delete(0, tk.END)
    #     for client in self.clients.keys():
    #         self.clients_list.insert(tk.END, client)

    def display_message(self, sender, message):
        self.messages_list.insert(tk.END, f'{sender}:>> {message}')

    def start_receiving_thread(self):
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.daemon = True
        receive_thread.start()

root = tk.Tk()
server = ChatServer(root)
root.mainloop()
