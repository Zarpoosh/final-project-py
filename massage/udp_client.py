import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message(sender, recipient, message):
    print(f"Sending message from {sender} to {recipient}: {message}")
    # Create a UDP packet with the message
    data = {"sender": sender, "recipient": recipient, "message": message}
    sock.sendto(data.encode("utf-8"), ("localhost", 12345))

    # Receive the message from the UDP server
    data, addr = sock.recvfrom(1024)
    message = data.decode("utf-8")

    # Display the message in the GUI
    gui.display_area.insert("end", f"{sender} -> {recipient}: {message}\n")