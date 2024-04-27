from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os.path
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(BASE_DIR, 'users.db')
    conn = sqlite3.connect(db_dir)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    password_hash = generate_password_hash(password)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cur.fetchone():
            flash("Username already exists. Please choose a different username.", 'error')
            return redirect(url_for('register_form'))
        elif not username:
            flash("Username is required.", 'error')
            return redirect(url_for('register_form'))
        elif not password:
            flash("Password is required.", 'error')
            return redirect(url_for('register_form'))
        
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        flash("User created successfully", 'success')
    except sqlite3.Error as e:
        flash("An error occurred: " + str(e), 'error')
    finally:
        conn.close()
    
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/test')
def test():
    return "Test page"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
