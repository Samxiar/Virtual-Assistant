#adding the data to the database manually.
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Execute the ALTER TABLE statement to add the 'email' column
cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')

# Commit the changes and close the connection
conn.commit()
conn.close()