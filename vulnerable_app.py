from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "vulnerable.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute('INSERT INTO users (username, password) VALUES ("admin", "secret_admin_pass")')
    cursor.execute('INSERT INTO users (username, password) VALUES ("user", "userpass")')
    
    cursor.execute('CREATE TABLE comments (id INTEGER PRIMARY KEY, content TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
    <h1>Vulnerable App</h1>
    <ul>
        <li><a href="/login">Login (SQL Injection)</a></li>
        <li><a href="/search">Search (Reflected XSS)</a></li>
        <li><a href="/comments">Comments (Stored XSS)</a></li>
        <li><a href="/db_init">Reset Database</a></li>
    </ul>
    '''

@app.route('/db_init')
def db_init():
    init_db()
    return "Database initialized! <a href='/'>Go Home</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # VULNERABLE: SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing Query: {query}")
        
        conn = get_db_connection()
        try:
            user = conn.execute(query).fetchone()
            conn.close()
            
            if user:
                return f"Welcome, {user['username']}! <a href='/'>Go Home</a>"
            else:
                return "Invalid credentials. <a href='/login'>Try again</a>"
        except Exception as e:
            return f"Database Error: {e} <a href='/login'>Try again</a>"

    return '''
    <h2>Login</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="text" name="password"><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # VULNERABLE: Reflected XSS
    return f'''
    <h2>Search</h2>
    <form>
        Search: <input type="text" name="q" value="{query}">
        <input type="submit" value="Search">
    </form>
    <p>You searched for: {query}</p>
    <a href="/">Go Home</a>
    '''

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    conn = get_db_connection()
    if request.method == 'POST':
        content = request.form.get('content')
        # VULNERABLE: Stored XSS
        conn.execute(f"INSERT INTO comments (content) VALUES ('{content}')")
        conn.commit()
    
    comments = conn.execute('SELECT * FROM comments').fetchall()
    conn.close()
    
    comments_html = "".join([f"<li>{c['content']}</li>" for c in comments])
    
    return f'''
    <h2>Comments</h2>
    <form method="POST">
        Comment: <input type="text" name="content"><br>
        <input type="submit" value="Post">
    </form>
    <h3>Recent Comments:</h3>
    <ul>
        {comments_html}
    </ul>
    <a href="/">Go Home</a>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
