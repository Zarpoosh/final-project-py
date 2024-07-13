# import socket
# import tkinter as tk
# from tkinter import messagebox
# import sqlite3

# class ChatClient:
#     def __init__(self, master):
#         self.master = master
#         self.master.title('Chat Client')
#         self.master.geometry('300x400')

#         # Create a UDP socket
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#         # Create a SQLite database connection
#         self.conn = sqlite3.connect('chat.db')
#         self.cursor = self.conn.cursor()

#         # Create a table to store messages
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS messages (
#                 id INTEGER PRIMARY KEY,
#                 sender TEXT,
#                 receiver TEXT,
#                 message TEXT
#             )
#         ''')
#         self.conn.commit()

#         # Create GUI components
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

#         self.receive_button = tk.Button(master, text='Receive', command=self.receive_message)
#         self.receive_button.pack()

#     def send_message(self):
#         sender = self.sender_entry.get()
#         receiver = self.receiver_entry.get()
#         message = self.message_text.get('1.0', 'end-1c')

#         # Send the message to the server
#         self.sock.sendto(f'{sender}:{receiver}:{message}'.encode('utf-8'), ('localhost', 10000))

#         # Clear the message text
#         self.message_text.delete('1.0', 'end')

#     def receive_message(self):
#         # Receive messages from the server
#         data, address = self.sock.recvfrom(1024)
#         message = data.decode('utf-8')

#         # Display the received message
#         messagebox.showinfo('Received Message', message)

# root = tk.Tk()
# client = ChatClient(root)
# root.mainloop()

