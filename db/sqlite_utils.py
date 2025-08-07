import sqlite3

def create_connection(db_path="DataLinken.db"):
    return sqlite3.connect(db_path)

def create_table():
    with create_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT)''')
        conn.commit()

def insert_account(email,password,recover):
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Account (email, password,recover) VALUES (?, ?,?)", (email,password,recover))
        conn.commit()

def select_account(where_clause="1=1"):
    with create_connection() as conn:
        c = conn.cursor()
        c.execute(f"SELECT email,password,recover,uuid FROM Account WHERE {where_clause}")
        rows = c.fetchall()
        return rows

def update_live_account(username, live):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Account SET live = ? WHERE email = ?
        ''', (live, username))
        conn.commit()

def delete_account(email=None):
    with create_connection() as conn:
        cursor = conn.cursor()
        if email:
            # Xóa 1 account theo email
            cursor.execute("DELETE FROM Account WHERE email = ?", (email,))
        else:
            # Xóa toàn bộ bảng
            cursor.execute("DELETE FROM Account")
        conn.commit()
    

def update_uuid_account(username, uuid):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Account SET uuid = ? WHERE email = ?
        ''', (uuid, username))
        conn.commit()
        
    
