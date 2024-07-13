import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_seller_panel():
    seller_panel = tk.Tk()
    seller_panel.title("Seller Panel")
    seller_panel.geometry("400x600")
    seller_panel.configure(bg="#f0f0f0")

    entry_bg = "#e0e0e0"
    button_bg = "#007bff"
    button_fg = "#ffffff"
    border_width = 2
    padding = 10

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

    def update_listbox():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT * FROM books")
        for row in c.fetchall():
            listbox.insert(tk.END, row)
        conn.close()

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

    update_listbox()

    seller_panel.mainloop()
