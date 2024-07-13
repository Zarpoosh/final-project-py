import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import socket

class Server:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server")
        self.root.geometry("300x400")

        self.text_area = tk.Text(self.root, width=40, height=20)
        self.text_area.pack(pady=10)

        self.entry_field = tk.Entry(self.root, width=30)
        self.entry_field.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.conn = sqlite3.connect("chat.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT)")
        self.conn.commit()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", 12345))
        self.socket.listen(1)

        self.client_socket, self.address = self.socket.accept()
        print("Client connected.")

        self.root.after(1000, self.check_for_messages)

        self.root.mainloop()

    def send_message(self):
        message = self.entry_field.get()
        if message:
            self.client_socket.send(message.encode())
            self.text_area.insert(tk.END, "Server: " + message + "\n")
            self.entry_field.delete(0, tk.END)

    def check_for_messages(self):
        try:
            message = self.client_socket.recv(1024).decode()
            if message:
                self.text_area.insert(tk.END, "Client: " + message + "\n")
                self.cursor.execute("INSERT INTO messages VALUES (?)", (message,))
                self.conn.commit()
        except:
            pass
        self.root.after(1000, self.check_for_messages)

if __name__ == "__main__":
    server = Server()