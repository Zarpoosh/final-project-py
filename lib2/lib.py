import tkinter as tk
from tkinter import messagebox
import sqlite3

#! Function to set up the database
def setup_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, usertype TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)''')
    # Add a default user
    c.execute("INSERT OR IGNORE INTO users (username, password, usertype) VALUES ('admin', 'password', 'Seller')")
    conn.commit()
    conn.close()


#! Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    user_type = user_type_var.get()
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=? AND usertype=?", (username, password, user_type))
    if c.fetchone():
        if user_type == "Customer":
            open_customer_page()
        elif user_type == "Seller":
            open_seller_panel()
    else:
        messagebox.showerror("Login Error", "Invalid username, password, or user type")
    conn.close()


#! Function to handle signup
def signup():
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")
    signup_window.geometry("400x600")

    tk.Label(signup_window, text="Username", font=("Arial", 14)).grid(row=0, column=0, padx=20, pady=10)
    entry_signup_username = tk.Entry(signup_window, font=("Arial", 14))
    entry_signup_username.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(signup_window, text="Password", font=("Arial", 14)).grid(row=1, column=0, padx=20, pady=10)
    entry_signup_password = tk.Entry(signup_window, show='*', font=("Arial", 14))
    entry_signup_password.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(signup_window, text="User Type", font=("Arial", 14)).grid(row=2, column=0, padx=20, pady=10)
    user_type_var_signup = tk.StringVar(value="Customer")
    tk.Radiobutton(signup_window, text="Customer", variable=user_type_var_signup, value="Customer", font=("Arial", 14)).grid(row=2, column=1)
    tk.Radiobutton(signup_window, text="Seller", variable=user_type_var_signup, value="Seller", font=("Arial", 14)).grid(row=2, column=2)

    def save_signup():
        username = entry_signup_username.get()
        password = entry_signup_password.get()
        user_type = user_type_var_signup.get()
        if username and password:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, usertype) VALUES (?, ?, ?)", (username, password, user_type))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sign Up", "User registered successfully")
            signup_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    tk.Button(signup_window, text="Sign Up", command=save_signup, font=("Arial", 14)).grid(row=3, column=0, columnspan=3, pady=20)

#! Function to open customer page
# Function to open customer page
def open_customer_page():
    login_window.destroy()
    customer_page = tk.Tk()
    customer_page.title("Customer Page")
    customer_page.geometry("400x600")

    # Initialize cart and total price
    cart = []
    total_price = 0.0

    # Function to add book to cart
    def add_to_cart(book):
        nonlocal total_price
        if book[3] > 0:
            cart.append(book)
            total_price += book[2]
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("UPDATE books SET quantity=? WHERE id=?", (book[3]-1, book[0]))
            conn.commit()
            conn.close()
            update_book_listbox()
            update_cart_display()
        else:
            messagebox.showwarning("Stock Error", "This book is out of stock.")

    # Function to remove book from cart
    def remove_from_cart():
        nonlocal total_price
        selected_book = cart_listbox.curselection()
        if selected_book:
            book = cart.pop(selected_book[0])
            total_price -= book[2]
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("UPDATE books SET quantity=? WHERE id=?", (book[3]+1, book[0]))
            conn.commit()
            conn.close()
            update_book_listbox()
            update_cart_display()
        else:
            messagebox.showwarning("Selection Error", "Please select a book to remove.")

    # Function to update the cart display
    def update_cart_display():
        cart_listbox.delete(0, tk.END)
        for book in cart:
            cart_listbox.insert(tk.END, f"{book[1]} - ${book[2]:.2f}")
        total_label.config(text=f"Total: ${total_price:.2f}")

    # Function to update the listbox with current books from the database
    def update_book_listbox():
        book_listbox.delete(0, tk.END)
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        for row in c.fetchall():
            book_listbox.insert(tk.END, row)
        conn.close()

    # Function to handle purchase action
    def purchase():
        messagebox.showinfo("Purchase", f"Purchase successful!\nTotal: ${total_price:.2f}")
        cart.clear()
        update_cart_display()

    # Create and place widgets in the customer page
    tk.Label(customer_page, text="Available Books:", font=("Arial", 14)).pack(pady=10)

    book_listbox = tk.Listbox(customer_page, font=("Arial", 12))
    book_listbox.pack(pady=10)

    tk.Button(customer_page, text="Add to Cart", command=lambda: add_to_cart(book_listbox.get(book_listbox.curselection())), font=("Arial", 14)).pack(pady=10)

    tk.Label(customer_page, text="Shopping Cart:", font=("Arial", 14)).pack(pady=10)

    cart_listbox = tk.Listbox(customer_page, font=("Arial", 12))
    cart_listbox.pack(pady=10)

    tk.Button(customer_page, text="Remove from Cart", command=remove_from_cart, font=("Arial", 14)).pack(pady=10)

    total_label = tk.Label(customer_page, text=f"Total: ${total_price:.2f}", font=("Arial", 14))
    total_label.pack(pady=10)

    tk.Button(customer_page, text="Purchase", command=purchase, bg="#007bff", fg="#ffffff", font=("Arial", 14)).pack(pady=20)

    update_book_listbox()
    update_cart_display()

    customer_page.mainloop()



#! Function to open seller panel
# Function to open seller panel
def open_seller_panel():
    login_window.destroy()
    seller_panel = tk.Tk()
    seller_panel.title("Seller Panel")
    seller_panel.geometry("400x600")
    seller_panel.configure(bg="#f0f0f0")

    # Style configurations
    entry_bg = "#e0e0e0"
    button_bg = "#007bff"
    button_fg = "#ffffff"
    border_width = 2
    padding = 10

    # Function to add book
    def add_book():
        name = entry_book_name.get()
        price = entry_book_price.get()
        quantity = entry_book_quantity.get()
        if name and price and quantity:
            try:
                price = float(price)
                quantity = int(quantity)
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute("INSERT INTO books (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
                conn.commit()
                conn.close()
                entry_book_name.delete(0, tk.END)
                entry_book_price.delete(0, tk.END)
                entry_book_quantity.delete(0, tk.END)
                update_listbox()
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid price and quantity.")
        else:
            messagebox.showwarning("Input Error", "Please enter book name, price and quantity.")

    # Function to update the listbox with current books from the database
    def update_listbox():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        for row in c.fetchall():
            listbox.insert(tk.END, row)
        conn.close()

    # Function to delete selected book from the database
    def delete_book():
        selected_book = listbox.curselection()
        if selected_book:
            book_id = listbox.get(selected_book)[0]
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            conn.close()
            update_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a book to delete.")

    # Function to edit selected book
    def edit_book():
        selected_book = listbox.curselection()
        if selected_book:
            book_id = listbox.get(selected_book)[0]
            name = entry_book_name.get()
            price = entry_book_price.get()
            quantity = entry_book_quantity.get()
            if name and price and quantity:
                try:
                    price = float(price)
                    quantity = int(quantity)
                    conn = sqlite3.connect('library.db')
                    c = conn.cursor()
                    c.execute("UPDATE books SET name=?, price=?, quantity=? WHERE id=?", (name, price, quantity, book_id))
                    conn.commit()
                    conn.close()
                    entry_book_name.delete(0, tk.END)
                    entry_book_price.delete(0, tk.END)
                    entry_book_quantity.delete(0, tk.END)
                    update_listbox()
                except ValueError:
                    messagebox.showwarning("Input Error", "Please enter a valid price and quantity.")
            else:
                messagebox.showwarning("Input Error", "Please enter book name, price and quantity.")
        else:
            messagebox.showwarning("Selection Error", "Please select a book to edit.")

    # Create and place widgets in the seller panel
    tk.Label(seller_panel, text="Book Name:", bg="#f0f0f0", font=("Arial", 14)).grid(row=0, column=0, padx=padding, pady=padding, sticky="e")
    entry_book_name = tk.Entry(seller_panel, bg=entry_bg, bd=border_width, font=("Arial", 14))
    entry_book_name.grid(row=0, column=1, padx=padding, pady=padding)

    tk.Label(seller_panel, text="Book Price:", bg="#f0f0f0", font=("Arial", 14)).grid(row=1, column=0, padx=padding, pady=padding, sticky="e")
    entry_book_price = tk.Entry(seller_panel, bg=entry_bg, bd=border_width, font=("Arial", 14))
    entry_book_price.grid(row=1, column=1, padx=padding, pady=padding)

    tk.Label(seller_panel, text="Quantity:", bg="#f0f0f0", font=("Arial", 14)).grid(row=2, column=0, padx=padding, pady=padding, sticky="e")
    entry_book_quantity = tk.Entry(seller_panel, bg=entry_bg, bd=border_width, font=("Arial", 14))
    entry_book_quantity.grid(row=2, column=1, padx=padding, pady=padding)

    tk.Button(seller_panel, text="Add Book", command=add_book, bg=button_bg, fg=button_fg, font=("Arial", 14)).grid(row=3, column=0, columnspan=2, padx=padding, pady=padding)

    listbox = tk.Listbox(seller_panel, bd=border_width, font=("Arial", 14))
    listbox.grid(row=4, column=0, columnspan=2, padx=padding, pady=padding)

    tk.Button(seller_panel, text="Delete Book", command=delete_book, bg=button_bg, fg=button_fg, font=("Arial", 14)).grid(row=5, column=0, columnspan=2, padx=padding, pady=padding)
    tk.Button(seller_panel, text="Edit Book", command=edit_book, bg=button_bg, fg=button_fg, font=("Arial", 14)).grid(row=6, column=0, columnspan=2, padx=padding, pady=padding)

    # Update the listbox with current books
    update_listbox()

    seller_panel.mainloop()



# Set up the main login window
login_window = tk.Tk()
login_window.title("Log to Account")
login_window.geometry("400x600")

# Set up the database
setup_database()

# Create and place widgets in the login window
tk.Label(login_window, text="Log to Account", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

tk.Label(login_window, text="Username", font=("Arial", 14)).grid(row=1, column=0, padx=20, pady=10)
entry_username = tk.Entry(login_window, font=("Arial", 14))
entry_username.grid(row=1, column=1, padx=20, pady=10)

tk.Label(login_window, text="Password", font=("Arial", 14)).grid(row=2, column=0, padx=20, pady=10)
entry_password = tk.Entry(login_window, show='*', font=("Arial", 14))
entry_password.grid(row=2, column=1, padx=20, pady=10)

user_type_var = tk.StringVar(value="Customer")
tk.Radiobutton(login_window, text="Customer", variable=user_type_var, value="Customer", font=("Arial", 14)).grid(row=3, column=0, pady=10)
tk.Radiobutton(login_window, text="Seller", variable=user_type_var, value="Seller", font=("Arial", 14)).grid(row=3, column=1, pady=10)

tk.Button(login_window, text="SIGN IN", command=login, font=("Arial", 14)).grid(row=4, column=0, columnspan=2, pady=20)
tk.Button(login_window, text="SIGN UP", command=signup, font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=10)

login_window.mainloop()
