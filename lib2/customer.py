import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_customer_page():
    customer_page = tk.Tk()
    customer_page.title("Customer Page")
    customer_page.geometry("400x600")

    cart = []
    total_price = 0.0

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

    def update_cart_display():
        cart_listbox.delete(0, tk.END)
        for book in cart:
            cart_listbox.insert(tk.END, f"{book[1]} - ${book[2]:.2f}")
        total_label.config(text=f"Total: ${total_price:.2f}")

    def update_book_listbox():
        book_listbox.delete(0, tk.END)
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        for row in c.fetchall():
            book_listbox.insert(tk.END, row)
        conn.close()

    def purchase():
        messagebox.showinfo("Purchase", f"Purchase successful!\nTotal: ${total_price:.2f}")
        cart.clear()
        update_cart_display()

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
