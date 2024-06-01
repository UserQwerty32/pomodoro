import sqlite3

connect = sqlite3.connect('code_versions.db')
c = connect.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS code_versions (
             id INTEGER PRIMARY KEY,
             author TEXT,
             code TEXT
             )''')

def save_version(author, code):
    c.execute('INSERT INTO code_versions (author, code) VALUES (?, ?)', (author, code))
    connect.commit()

def get_versions():
    c.execute('SELECT * FROM code_versions')
    return c.fetchall()

def get_previous_version():
    c.execute('SELECT * FROM code_versions ORDER BY id DESC LIMIT 2')
    rows = c.fetchall()
    if len(rows) >= 2:
        _, author, code = rows[1]
        return author, code
    return None, None