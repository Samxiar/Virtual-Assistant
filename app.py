from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
from IPython.display import Markdown
import textwrap
import sqlite3
import smtplib

app = Flask(__name__)
genai.configure(api_key="AIzaSyDAzepZoPJP4US2Lwhj_WcXi1YFqhCoAMA")
model = genai.GenerativeModel('gemini-pro')
responses = []

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Function to create the users table in the SQLite database
def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new user into the database
def insert_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Function to authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Create the users table on startup
create_table()

@app.route('/')
def index():
    return render_template('index.html', responses=responses)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            return redirect(url_for('assistant'))
    return render_template('login.html')

@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        if user_input.lower() == 'exit':
            responses.append("Goodbye!")
        else:
            try:
                response = model.generate_content(user_input)
                bot_reply = response.text.strip()
                responses.append(bot_reply)
            except ValueError as e:
                responses.append("Please use appropriate words.")
    
    return render_template('assist.html', responses=responses)

@app.route('/clear', methods=['POST'])
def clear():
    responses.clear()  # Clear the chat history
    return redirect(url_for('assistant'))

@app.route('/view-history', methods=['GET'])
def view_history():
    return render_template('assist.html', responses=responses)


@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        send_email(name, email, message)

        # You can add additional logic here, such as redirecting to a thank you page

    return render_template('/')

def send_email(name, email, message):
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'
    sender_email = 'your_email@example.com'
    receiver_email = 'samxiar@gmail.com'

    subject = 'New Contact Form Submission'
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

    # Simplest way to send an email using smtplib
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [receiver_email], f'Subject: {subject}\n\n{body}')

if __name__ == '__main__':

    app.run(debug=True)