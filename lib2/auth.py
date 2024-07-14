import tkinter as tk
from tkinter import messagebox
import sqlite3
from customer import open_customer_page
from seller import open_seller_panel

def login(entry_username, entry_password, user_type_var, login_window):
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
        login_window.destroy()
    else:
        messagebox.showerror("Login Error", "Invalid username, password, or user type")
    conn.close()

def signup(login_window):
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Sign Up")
    signup_window.geometry("600x600")

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
             # Check if the user already exists
            c.execute("SELECT * FROM users WHERE username=? AND usertype=?", (username, user_type))
            if c.fetchone():
                messagebox.showerror("Sign Up Error", "A user with this username and user type already exists.")
            else:
                c.execute("INSERT INTO users (username, password, usertype) VALUES (?, ?, ?)", (username, password, user_type))
                conn.commit()
                messagebox.showinfo("Sign Up", "User registered successfully")
                signup_window.destroy()
            conn.close()
        else:
            messagebox.showwarning("Input Error", "Please enter both username and password.")

    tk.Button(signup_window, text="Sign Up", command=save_signup, font=("Arial", 14)).grid(row=3, column=0, columnspan=3, pady=20)