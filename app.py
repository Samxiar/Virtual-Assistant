from flask import Flask, render_template, request, redirect, url_for,session
import google.generativeai as genai
from IPython.display import Markdown
import textwrap
import sqlite3
import re

app = Flask(__name__)
app.secret_key = '123456789'
genai.configure(api_key="AIzaSyDAzepZoPJP4US2Lwhj_WcXi1YFqhCoAMA")
model = genai.GenerativeModel('gemini-pro')
responses = []

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '  ', predicate=lambda _: True))

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

# Function to set the user in the session
def set_user_in_session(user):
    session['user_id'] = user[0]  # Assuming the user ID is the first column in your 'users' table

# Function to check if a user is logged in
def is_user_logged_in():
    return 'user_id' in session

# Function to get the current user from the session
def get_current_user():
    if is_user_logged_in():
        user_id = session['user_id']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            set_user_in_session(user)
            return redirect(url_for('assistant'))
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('index'))  # Redirect to the home page or any other page

def interpret_double_stars_as_bold(text):
    # Use regular expression to find double stars and replace with bold tags
    bold_text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', text)
    return bold_text 


# Modify the 'assistant' route to check if the user is logged in
def format_and_print(response):
    """
    Formats and prints a multiline string response, preserving indentation.

    Args:
    response (str): Multiline string to be formatted and printed.
    """
    lines = response.split('\n')
    formatted_lines = [line.strip() for line in lines]
    formatted_response = '\n'.join(formatted_lines)
    return formatted_response

@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    if not is_user_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_input = request.form['user_input']
        
        if user_input.lower() == 'exit':
            responses.append("Goodbye!")
        else:
            try:
                response = model.generate_content(user_input)
                bot_reply = response.text.strip()
                bot_reply_with_bold = interpret_double_stars_as_bold(bot_reply)
                bot_reply_markdown = to_markdown(bot_reply_with_bold).data  # Extracting the content from Markdown object
                formatted_bot_reply = format_and_print(bot_reply_markdown)
                responses.append(formatted_bot_reply)
            except ValueError as e:
                responses.append("Please use appropriate words.")
    
    formatted_responses = [format_and_print(response) for response in responses]
    return render_template('assist.html', responses=formatted_responses)

@app.route('/clear', methods=['POST'])
def clear():
    responses.clear()  # Clear the chat history
    return redirect(url_for('assistant'))

@app.route('/view-history', methods=['GET'])
def view_history():
    return render_template('assist.html', responses=responses, view_history=True)

if __name__ == '__main__':

    app.run(debug=True)