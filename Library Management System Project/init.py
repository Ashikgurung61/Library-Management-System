import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",       # 👈 Replace with your MySQL username
    password="2020Bca01"    # 👈 Replace with your MySQL password
)

cursor = conn.cursor()

# 1. Create Library database
cursor.execute("CREATE DATABASE IF NOT EXISTS Library")
cursor.execute("USE Library")

# 2. Create users table with VARCHAR user_id
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    role ENUM('student', 'faculty', 'admin'),
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# 3. Create books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(50),
    publisher VARCHAR(100),
    quantity INT DEFAULT 1,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# 4. Create transactions table with updated foreign keys
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(20),
    book_id INT,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL(6,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
)
''')

# 5. Create fines table
cursor.execute('''
CREATE TABLE IF NOT EXISTS fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    amount DECIMAL(6,2),
    paid_status BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
)
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS admin (username varchar(25) primary key, password varchar(12))''')

print("✅ All tables created successfully in 'Library' database.")

cursor.close()
conn.close()
