import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)

    print("Server started. Waiting for client...")

    client_socket, address = server_socket.accept()
    print("Client connected.")

    while True:
        message = client_socket.recv(1024).decode()
        if message:
            client_socket.send(message.encode())

if __name__ == "__main__":
    start_server()