from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Insecure database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return 'Welcome to the vulnerable Flask app!'

# SQL Injection vulnerability
@app.route('/user/<username>')
def get_user(username):
    conn = get_db_connection()
    user = conn.execute(f"SELECT * FROM users WHERE username = '{username}'").fetchone()
    conn.close()
    if user:
        return f"Hello, {user['username']}!"
    else:
        return "User not found"

# Cross-Site Scripting (XSS) vulnerability
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return render_template_string(f'<h1>Search Results for {query}</h1>')

# Insecure file upload vulnerability
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f'./uploads/{file.filename}')
    return 'File uploaded successfully!'

# Hardcoded secret key
app.config['SECRET_KEY'] = 'supersecretkey'

if __name__ == '__main__':
    app.run(debug=True)
