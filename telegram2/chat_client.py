
# import socket
# import threading
# import tkinter as tk
# import sqlite3
# from queue import Queue

# class ChatClient:
#     def __init__(self, master):
#         self.master = master
#         self.master.title('Chat Client')
#         self.master.geometry('300x400')

#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#         self.conn = sqlite3.connect('chat.db', check_same_thread=False)
#         self.cursor = self.conn.cursor()
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS messages (
#                 id INTEGER PRIMARY KEY,
#                 sender TEXT,
#                 receiver TEXT,
#                 message TEXT
#             )
#         ''')
#         self.conn.commit()

#         self.sender_label = tk.Label(master, text='Sender:')
#         self.sender_label.pack()
#         self.sender_entry = tk.Entry(master, width=20)
#         self.sender_entry.pack()

#         self.receiver_label = tk.Label(master, text='Receiver:')
#         self.receiver_label.pack()
#         self.receiver_entry = tk.Entry(master, width=20)
#         self.receiver_entry.pack()

#         self.message_label = tk.Label(master, text='Message:')
#         self.message_label.pack()
#         self.message_text = tk.Text(master, width=20, height=10)
#         self.message_text.pack()

#         self.send_button = tk.Button(master, text='Send', command=self.send_message)
#         self.send_button.pack()

#         self.messages_frame = tk.Frame(master)
#         self.messages_frame.pack(fill=tk.BOTH, expand=True)

#         self.messages_list = tk.Listbox(self.messages_frame)
#         self.messages_list.pack(fill=tk.BOTH, expand=True)

#         self.queue = Queue()

#         self.start_receiving_thread()
#         self.process_queue()

#     def send_message(self):
#         sender = self.sender_entry.get()
#         receiver = self.receiver_entry.get()
#         message = self.message_text.get('1.0', 'end-1c')

#         self.sock.sendto(f'{sender}:{receiver}:{message}'.encode('utf-8'), ('localhost', 10000))
#         self.message_text.delete('1.0', 'end')

#     def receive_message(self):
#         while True:
#             data, address = self.sock.recvfrom(1024)
#             message = data.decode('utf-8')
#             self.queue.put(message, address)

#     def process_queue(self):
#         try:
#             while not self.queue.empty():
#                 message = self.queue.get()
#                 sender, received_message = message.split(':', 1)
#                 self.display_message(sender, received_message)

#             self.master.after(100, self.process_queue)
#         except Exception as e:
#             print(f"Error processing queue: {e}")

#     def display_message(self, sender, message):
#         self.messages_list.insert(tk.END, f'{sender}:>> {message}')

#     def start_receiving_thread(self):
#         receive_thread = threading.Thread(target=self.receive_message)
#         receive_thread.daemon = True
#         receive_thread.start()

# root = tk.Tk()
# client = ChatClient(root)
# root.mainloop()

