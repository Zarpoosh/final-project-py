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
import sqlite3

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to an address and port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Create a SQLite database connection
db = sqlite3.connect('chat.db')
cursor = db.cursor()

# Create a table to store messages
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        receiver TEXT,
        message TEXT
    )
''')
db.commit()

print('Server started. Waiting for messages...')

clients = {}

while True:
    # Receive a message from a client
    data, address = sock.recvfrom(1024)
    message = data.decode('utf-8')
    sender, receiver, message = message.split(':')

    # Store the message in the database
    cursor.execute('''
        INSERT INTO messages (sender, receiver, message)
        VALUES (?, ?, ?)
    ''', (sender, receiver, message))
    db.commit()

    # Register clients
    if sender not in clients:
        clients[sender] = address
    if receiver in clients:
        # Send the message to the receiver
        sock.sendto(f'{sender}:{message}'.encode('utf-8'), clients[receiver])

    print(f'Received message from {sender} to {receiver}: {message}')
