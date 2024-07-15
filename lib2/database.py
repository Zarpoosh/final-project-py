# import sqlite3

# def setup_database():
#     conn = sqlite3.connect('library.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS users
#                  (id INTEGER PRIMARY KEY, username TEXT, password TEXT, usertype TEXT)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS books
#                  (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)''')
#     # Add a default user
#     c.execute("INSERT OR IGNORE INTO users (username, password, usertype) VALUES ('admin', 'password', 'Seller')")
#     conn.commit()
#     conn.close()




import sqlite3

def setup_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, usertype TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                  (id INTEGER PRIMARY KEY, user_id INTEGER, order_date DATE, total REAL,
                   FOREIGN KEY (user_id) REFERENCES users (id))''')
    # Add a default user
    c.execute("INSERT OR IGNORE INTO users (username, password, usertype) VALUES ('admin', 'password', 'Seller')")
    conn.commit()
    conn.close()