import socket
import threading
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import sqlite3
from queue import Queue

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title('Chat Client')
        self.master.geometry('400x600')
        self.master.configure(padx=20, pady=20)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.conn = sqlite3.connect('chat.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                receiver TEXT,
                message TEXT
            )
        ''')
        self.conn.commit()

        self.font = ('Helvetica', 12)
        self.message_font = ('Arial', 10)

        self.style = tb.Style()
        self.style.configure("TEntry", borderwidth=0)
        
        self.sender_label = ttk.Label(master, text='Sender:', font=self.font)
        self.sender_label.pack(pady=5)

        self.sender_frame = ttk.Frame(master, style="TFrame")
        self.sender_frame.pack(pady=5, fill=tk.X)
        self.sender_entry = ttk.Entry(self.sender_frame, width=20, font=self.font, style="TEntry")
        self.sender_entry.pack(padx=5, pady=5, fill=tk.X)

        self.receiver_label = ttk.Label(master, text='Receiver:', font=self.font)
        self.receiver_label.pack(pady=5)

        self.receiver_frame = ttk.Frame(master, style="TFrame")
        self.receiver_frame.pack(pady=5, fill=tk.X)
        self.receiver_entry = ttk.Entry(self.receiver_frame, width=20, font=self.font, style="TEntry")
        self.receiver_entry.pack(padx=5, pady=5, fill=tk.X)

        self.message_label = ttk.Label(master, text='Message:', font=self.font)
        self.message_label.pack(pady=5)

        self.message_frame = ttk.Frame(master, style="TFrame")
        self.message_frame.pack(pady=5, fill=tk.X)
        self.message_text = tk.Text(self.message_frame, width=30, height=5, font=self.font, bd=0)
        self.message_text.pack(padx=5, pady=5, fill=tk.X)

        self.send_button = ttk.Button(master, text='Send', command=self.send_message, style="Primary.TButton")
        self.send_button.pack(pady=10)

        self.messages_label = ttk.Label(master, text='Chat Page', font=self.font)
        self.messages_label.pack(pady=5)

        self.messages_frame = ttk.Frame(master)
        self.messages_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.messages_list = tk.Listbox(self.messages_frame, font=self.message_font)
        self.messages_list.pack(fill=tk.BOTH, expand=True)

        self.queue = Queue()

        self.start_receiving_thread()
        self.process_queue()

    def send_message(self):
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        message = self.message_text.get('1.0', 'end-1c')

        self.sock.sendto(f'{sender}:{receiver}:{message}'.encode('utf-8'), ('localhost', 10000))
        self.message_text.delete('1.0', 'end')

    def receive_message(self):
        while True:
            data, address = self.sock.recvfrom(1024)
            message = data.decode('utf-8')
            self.queue.put(message, address)

    def process_queue(self):
        try:
            while not self.queue.empty():
                message = self.queue.get()
                sender, received_message = message.split(':', 1)
                self.display_message(sender, received_message)

            self.master.after(100, self.process_queue)
        except Exception as e:
            print(f"Error processing queue: {e}")

    def display_message(self, sender, message):
        self.messages_list.insert(tk.END, f'{sender}:>> {message}')

    def start_receiving_thread(self):
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.daemon = True
        receive_thread.start()

root = tb.Window(themename="litera")
client = ChatClient(root)
root.mainloop()
