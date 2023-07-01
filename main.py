# This is a sample Python script.
import sqlite3, requests
from flask import Flask, request, render_template

app = Flask(__name__)

conn = sqlite3.connect("usingdb.db")
cursor = conn.cursor()

@app.route('/', methods = ['POST', 'GET'])
def sending():
    if request.method == 'POST':
        print(request.form.get('entr'))
    return render_template("test.html")

@app.route('/send', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form.get('entr'))
    return render_template("index.html")

if __name__ == '__main__':
    cursor.execute("""CREATE TABLE IF NOT EXISTS myStrings1
    (string_id UNIQUE, string_body, time_of_sending)
    """)
    conn.commit()
    app.run(debug=True)
    print("!")
