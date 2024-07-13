import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + '\n')
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)
        except:
            break

def send_message(client_socket, entry, sender):
    message = entry.get()
    if message:
        client_socket.send(message.encode())
        entry.delete(0, tk.END)

def setup_gui():
    window = tk.Tk()
    window.title("Chat Client")

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(window)
    entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

    send_button = tk.Button(window, text="Send", command=lambda: send_message(client_socket, entry, "Client"))
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    return window, text_area

def main():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 9999))

    window, text_area = setup_gui()

    threading.Thread(target=receive_messages, args=(client_socket, text_area)).start()
    window.mainloop()

if __name__ == "__main__":
    main()
