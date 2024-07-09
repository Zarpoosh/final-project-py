import socket
import sqlite3

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific port
sock.bind(("localhost", 12345))

# Create a SQLite database connection
conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

while True:
    # Receive a UDP packet
    data, addr = sock.recvfrom(1024)

    # Extract the message from the UDP packet
    message = data.decode("utf-8")

    # Store the message in the SQLite database
    cursor.execute("INSERT INTO messages (sender, recipient, message) VALUES (?,?,?)",
                   (message["sender"], message["recipient"], message["message"]))
    conn.commit()

    # Send the message to the recipient's UDP client
    sock.sendto(message.encode("utf-8"), addr)