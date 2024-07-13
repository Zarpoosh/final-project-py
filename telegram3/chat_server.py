import socket
import tkinter as tk
import sqlite3
import threading
from queue import Queue
import ttkbootstrap as tb

class ChatServer:
    def __init__(self, master):
        self.master = master
        self.master.title('Chat Server')
        self.master.geometry('400x600')
        self.master.configure(padx=20, pady=20)

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

        self.font = ('Helvetica', 12)
        self.message_font = ('Arial', 10)

        self.style = tb.Style()
        self.style.configure("TEntry", borderwidth=0)
        
        self.sender_label = tb.Label(master, text='Sender:', font=self.font)
        self.sender_label.pack(pady=5)

        self.sender_frame = tb.Frame(master, style="TFrame")
        self.sender_frame.pack(pady=5, fill=tk.X)
        self.sender_entry = tb.Entry(self.sender_frame, width=20, font=self.font, style="TEntry")
        self.sender_entry.pack(padx=5, pady=5, fill=tk.X)

        self.receiver_label = tb.Label(master, text='Receiver:', font=self.font)
        self.receiver_label.pack(pady=5)

        self.receiver_frame = tb.Frame(master, style="TFrame")
        self.receiver_frame.pack(pady=5, fill=tk.X)
        self.receiver_entry = tb.Entry(self.receiver_frame, width=20, font=self.font, style="TEntry")
        self.receiver_entry.pack(padx=5, pady=5, fill=tk.X)

        self.message_label = tb.Label(master, text='Message:', font=self.font)
        self.message_label.pack(pady=5)

        self.message_frame = tb.Frame(master, style="TFrame")
        self.message_frame.pack(pady=5, fill=tk.X)
        self.message_text = tk.Text(self.message_frame, width=30, height=5, font=self.font, bd=0)
        self.message_text.pack(padx=5, pady=5, fill=tk.X)

        self.send_button = tb.Button(master, text='Send', command=self.send_message, style="Primary.TButton")
        self.send_button.pack(pady=10)

        self.messages_label = tb.Label(master, text='Chat Page', font=self.font)
        self.messages_label.pack(pady=5)

        self.messages_frame = tb.Frame(master)
        self.messages_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.messages_list = tk.Listbox(self.messages_frame, font=self.message_font)
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

    def display_message(self, sender, message):
        self.messages_list.insert(tk.END, f'{sender}:>> {message}')

    def start_receiving_thread(self):
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.daemon = True
        receive_thread.start()

root = tb.Window(themename="litera")
server = ChatServer(root)
root.mainloop()
