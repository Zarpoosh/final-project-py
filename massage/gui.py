import tkinter as tk
class MessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message App")

        # Create input fields
        self.sender_label = tk.Label(root, text="Sender:")
        self.sender_label.pack()
        self.sender_entry = tk.Entry(root)
        self.sender_entry.pack()

        self.recipient_label = tk.Label(root, text="Recipient:")
        self.recipient_label.pack()
        self.recipient_entry = tk.Entry(root)
        self.recipient_entry.pack()

        self.message_label = tk.Label(root, text="Message:")
        self.message_label.pack()
        self.message_entry = tk.Text(root)
        self.message_entry.pack()

        # Create send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()

        # Create display area
        self.display_area = tk.Text(root)
        self.display_area.pack()

    # def send_message(self):
    #     # Get the input values
    #     sender = self.sender_entry.get()
    #     recipient = self.recipient_entry.get()
    #     message = self.message_entry.get("1.0", "end-1c")

    #     # Send the message using UDP client
    #     udp_client.send_message(sender, recipient, message)

    #     # Clear the input fields
    #     self.sender_entry.delete(0, "end")
    #     self.recipient_entry.delete(0, "end")
    #     self.message_entry.delete("1.0", "end")
    def send_message(self):
        sender = self.sender_entry.get()
        recipient = self.recipient_entry.get()
        message = self.message_entry.get("1.0", "end-1c")
        udp_client.send_message(sender, recipient, message)

root = tk.Tk()
app = MessageApp(root)
root.mainloop()