import sqlite3

db_path  = "database.db"


def create_users_table():
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            admin BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def create_items_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image TEXT NOT NULL,
            details TEXT NOT NULL,
            price_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def create_cart_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER NOT NULL,
            itemid INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (uid) REFERENCES users(id),
            FOREIGN KEY (itemid) REFERENCES items(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_ordered_items_table():
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordered_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER NOT NULL,
            itemid INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (uid) REFERENCES users(id),
            FOREIGN KEY (itemid) REFERENCES items(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users
        WHERE id = ?
    ''', (user_id,))

    user = cursor.fetchone()
    conn.close()

    return user

def confirm_email(user_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET email_confirmed = 1
        WHERE id = ?
    ''', (user_id,))

    conn.commit()
    conn.close()

def add_to_cart_db(user_id, item_id, quantity):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO cart (uid, itemid, quantity)
        VALUES (?, ?, ?)
    ''', (user_id, item_id, quantity))

    conn.commit()
    conn.close()

def remove_from_cart_by_id(cart_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    cursor.execute('''
        DELETE FROM cart
        WHERE id = ?
    ''', (cart_id,))

    conn.commit()
    conn.close()

def insert_item(name, price, category, image, details, price_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, price, category, image, details, price_id) VALUES (?, ?, ?, ?, ?, ?)',
                   (name, price, category, image, details, price_id))
    conn.commit()
    conn.close()

def insert_ordered_item(uid,item_id , quantity):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ordered_items (uid, itemid, quantity) VALUES (?, ?, ?)',
                   (uid, item_id , quantity))
    conn.commit()
    conn.close()



def get_all_items():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items

def get_item_by_id(item_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def update_item_by_id(item_id, new_name, new_price, new_category, new_image, new_details, new_price_id):
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE items
        SET name = ?, price = ?, category = ?, image = ?, details = ?, price_id = ?
        WHERE id = ?
    ''', (new_name, new_price, new_category, new_image, new_details, new_price_id, item_id))

    conn.commit()
    conn.close()

def delete_item_by_id(item_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM items
        WHERE id = ?
    ''', (item_id,))

    conn.commit()
    conn.close()


def register_user(name,email, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email,password,admin) VALUES (?, ?, ?,0)', (name, email, password))
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_cart_items(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart WHERE uid = ?', (id,))
    items = cursor.fetchall()
    conn.close()
    return items

def search_in_items(query):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM items
        WHERE name LIKE ?
    ''', (query,))

    # Fetch the results
    items = cursor.fetchall()

    conn.close()

    return items

def get_user_items(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT cart.id, items.name, items.price, cart.quantity, items.price_id , items.image
        FROM cart
        JOIN items ON cart.itemid = items.id
        WHERE cart.uid = ?
    ''', (user_id,))

    results = cursor.fetchall()

    conn.close()
    return results



create_users_table()
create_items_table()
create_cart_table()


