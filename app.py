from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('cmdb.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            model_version TEXT NOT NULL,
            owner TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('cmdb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assets')
    assets = cursor.fetchall()
    conn.close()
    return render_template('index.html', assets=assets)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    purchase_date = request.form['purchase_date']
    model_version = request.form['model_version']
    owner = request.form['owner']

    conn = sqlite3.connect('cmdb.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO assets (name, purchase_date, model_version, owner) VALUES (?, ?, ?, ?)',
                   (name, purchase_date, model_version, owner))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
