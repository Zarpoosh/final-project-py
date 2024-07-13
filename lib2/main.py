import tkinter as tk
from database import setup_database
from auth import login, signup

def main():
    login_window = tk.Tk()
    login_window.title("Log to Account")
    login_window.geometry("400x600")

    setup_database()

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

    tk.Button(login_window, text="SIGN IN", command=lambda: login(entry_username, entry_password, user_type_var, login_window), font=("Arial", 14)).grid(row=4, column=0, columnspan=2, pady=20)
    tk.Button(login_window, text="SIGN UP", command=lambda: signup(login_window), font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=10)

    login_window.mainloop()

if __name__ == "__main__":
    main()
