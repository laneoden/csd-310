import mysql.connector

# Connect to MySQL server
cnx = mysql.connector.connect(user="root", password="popcorn", host="127.0.0.1")
cursor = cnx.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS willson")
cursor.execute("USE willson")

# Create tables
tables = {}

tables['client'] = (
    "CREATE TABLE IF NOT EXISTS client ("
    "client_id INT NOT NULL AUTO_INCREMENT, "
    "client_name VARCHAR(75) NOT NULL, "
    "client_contact VARCHAR(75) NOT NULL, "
    "client_DOR DATE NOT NULL, "
    "PRIMARY KEY (client_id))"
)

tables['account'] = (
    "CREATE TABLE IF NOT EXISTS account ("
    "account_id INT NOT NULL AUTO_INCREMENT, "
    "account_type VARCHAR(75) NOT NULL, "
    "client_id INT NOT NULL, "
    "balance DECIMAL(10, 2) NOT NULL, "
    "date_opened DATE NOT NULL, "
    "PRIMARY KEY (account_id), "
    "FOREIGN KEY (client_id) REFERENCES client(client_id))"
)

tables['transaction'] = (
    "CREATE TABLE IF NOT EXISTS transaction ("
    "transaction_id INT NOT NULL AUTO_INCREMENT, "
    "account_id INT NOT NULL, "
    "date DATE NOT NULL, "
    "amount DECIMAL(10, 2) NOT NULL, "
    "type VARCHAR(50) NOT NULL, "
    "description VARCHAR(255), "
    "PRIMARY KEY (transaction_id), "
    "FOREIGN KEY (account_id) REFERENCES account(account_id))"
)

tables['employee'] = (
    "CREATE TABLE IF NOT EXISTS employee ("
    "employee_id INT NOT NULL AUTO_INCREMENT, "
    "employee_name VARCHAR(75) NOT NULL, "
    "employee_role VARCHAR(75) NOT NULL, "
    "employee_contact VARCHAR(75) NOT NULL, "
    "employee_doh DATE NOT NULL, "
    "PRIMARY KEY (employee_id))"
)

tables['appointment'] = (
    "CREATE TABLE IF NOT EXISTS appointment ("
    "appointment_id INT NOT NULL AUTO_INCREMENT, "
    "client_id INT NOT NULL, "
    "employee_id INT NOT NULL, "
    "date DATE NOT NULL, "
    "time TIME NOT NULL, "
    "purpose VARCHAR(255) NOT NULL, "
    "outcome VARCHAR(255), "
    "PRIMARY KEY (appointment_id), "
    "FOREIGN KEY (client_id) REFERENCES client(client_id), "
    "FOREIGN KEY (employee_id) REFERENCES employee(employee_id))"
)

tables['compliance'] = (
    "CREATE TABLE IF NOT EXISTS compliance ("
    "compliance_id INT NOT NULL AUTO_INCREMENT, "
    "employee_id INT NOT NULL, "
    "date DATE NOT NULL, "
    "type VARCHAR(75) NOT NULL, "
    "description VARCHAR(255), "
    "PRIMARY KEY (compliance_id), "
    "FOREIGN KEY (employee_id) REFERENCES employee(employee_id))"
)

tables['billing'] = (
    "CREATE TABLE IF NOT EXISTS billing ("
    "billing_id INT NOT NULL AUTO_INCREMENT, "
    "client_id INT NOT NULL, "
    "date DATE NOT NULL, "
    "amount DECIMAL(10, 2) NOT NULL, "
    "status VARCHAR(50) NOT NULL, "
    "PRIMARY KEY (billing_id), "
    "FOREIGN KEY (client_id) REFERENCES client(client_id))"
)

# Execute table creation statements
for table_name in tables:
    table_description = tables[table_name]
    try:
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        print(f"Error: {err.msg}")

# Insert sample data into the tables
clients = [
    ('Rancher Bob', '123-456-7890', '2024-01-01'),
    ('Farmer Joe', '987-654-3210', '2024-02-01'),
    ('Retiree Sue', '555-555-5555', '2024-03-01'),
    ('Investor Mary', '111-111-1111', '2024-04-01'),
    ('Developer John', '222-222-2222', '2024-05-01'),
    ('Businessman Chris', '333-333-3333', '2024-06-01')
]

cursor.executemany("INSERT INTO client (client_name, client_contact, client_DOR) VALUES (%s, %s, %s)", clients)
cnx.commit()

employees = [
    ('Jake Wilson', 'Co-Founder', 'jake.wilson@example.com', '2020-01-01'),
    ('Ned Wilson', 'Co-Founder', 'ned.wilson@example.com', '2020-02-01'),
    ('Phoenix Two Star', 'Office Manager', 'phoenix.twostar@example.com', '2020-03-01'),
    ('June Santos', 'Compliance Manager', 'june.santos@example.com', '2020-04-01')
]

cursor.executemany("INSERT INTO employee (employee_name, employee_role, employee_contact, employee_doh) VALUES (%s, %s, %s, %s)", employees)
cnx.commit()

# Fetch the ids to use in foreign keys
cursor.execute("SELECT client_id FROM client")
client_ids = cursor.fetchall()

cursor.execute("SELECT employee_id FROM employee")
employee_ids = cursor.fetchall()

# Insert accounts using client_ids
accounts = [
    ('Savings', client_ids[0][0], 10000.00, '2024-01-01'),
    ('Checking', client_ids[1][0], 15000.00, '2024-02-01'),
    ('Investment', client_ids[2][0], 20000.00, '2024-03-01'),
    ('Savings', client_ids[3][0], 25000.00, '2024-04-01'),
    ('Checking', client_ids[4][0], 30000.00, '2024-05-01'),
    ('Investment', client_ids[5][0], 35000.00, '2024-06-01')
]

cursor.executemany("INSERT INTO account (account_type, client_id, balance, date_opened) VALUES (%s, %s, %s, %s)", accounts)
cnx.commit()

# Fetch account_ids to use in transactions
cursor.execute("SELECT account_id FROM account")
account_ids = cursor.fetchall()

# Insert transactions with dates between April 21, 2024 and July 25, 2024 on weekdays
transactions = [
    (account_ids[0][0], '2024-04-22', 1000.00, 'Deposit', 'Initial deposit'),
    (account_ids[0][0], '2024-04-23', 500.00, 'Withdrawal', 'Bill payment'),
    (account_ids[0][0], '2024-05-10', 1500.00, 'Deposit', 'Salary deposit'),
    (account_ids[1][0], '2024-05-11', 2000.00, 'Deposit', 'Initial deposit'),
    (account_ids[1][0], '2024-05-12', 1000.00, 'Withdrawal', 'Bill payment'),
    (account_ids[1][0], '2024-05-13', 2500.00, 'Deposit', 'Salary deposit'),
    (account_ids[2][0], '2024-05-14', 3000.00, 'Deposit', 'Initial deposit'),
    (account_ids[2][0], '2024-05-15', 1500.00, 'Withdrawal', 'Bill payment'),
    (account_ids[2][0], '2024-06-10', 3500.00, 'Deposit', 'Salary deposit'),
    (account_ids[3][0], '2024-06-11', 4000.00, 'Deposit', 'Initial deposit'),
    (account_ids[3][0], '2024-06-12', 2000.00, 'Withdrawal', 'Bill payment'),
    (account_ids[3][0], '2024-06-13', 4500.00, 'Deposit', 'Salary deposit'),
    (account_ids[4][0], '2024-06-14', 5000.00, 'Deposit', 'Initial deposit'),
    (account_ids[4][0], '2024-06-17', 2500.00, 'Withdrawal', 'Bill payment'),
    (account_ids[4][0], '2024-06-18', 5500.00, 'Deposit', 'Salary deposit'),
    (account_ids[5][0], '2024-07-08', 6000.00, 'Deposit', 'Initial deposit'),
    (account_ids[5][0], '2024-07-09', 3000.00, 'Withdrawal', 'Bill payment'),
    (account_ids[5][0], '2024-07-10', 6500.00, 'Deposit', 'Salary deposit')
]

cursor.executemany("INSERT INTO transaction (account_id, date, amount, type, description) VALUES (%s, %s, %s, %s, %s)", transactions)
cnx.commit()

# Insert future appointments with dates after July 21, 2024 on weekdays
appointments = [
    (client_ids[0][0], employee_ids[2][0], '2024-07-22', '10:00:00', 'Consultation', 'Discussed investment options'),
    (client_ids[1][0], employee_ids[2][0], '2024-07-23', '11:00:00', 'Review', 'Reviewed financial goals'),
    (client_ids[2][0], employee_ids[2][0], '2024-07-24', '12:00:00', 'Consultation', 'Discussed retirement plan'),
    (client_ids[3][0], employee_ids[2][0], '2024-07-25', '13:00:00', 'Review', 'Reviewed investment portfolio'),
    (client_ids[4][0], employee_ids[2][0], '2024-07-26', '14:00:00', 'Consultation', 'Discussed business expansion'),
    (client_ids[5][0], employee_ids[2][0], '2024-07-29', '15:00:00', 'Review', 'Reviewed financial statements')
]

cursor.executemany("INSERT INTO appointment (client_id, employee_id, date, time, purpose, outcome) VALUES (%s, %s, %s, %s, %s, %s)", appointments)
cnx.commit()

# Insert compliance records using employee_ids
compliance = [
    (employee_ids[3][0], '2024-01-20', 'Audit', 'Audit of client accounts'),
    (employee_ids[3][0], '2024-02-20', 'Training', 'Employee compliance training'),
    (employee_ids[3][0], '2024-03-20', 'Audit', 'Audit of client transactions'),
    (employee_ids[3][0], '2024-04-20', 'Inspection', 'SEC compliance inspection'),
    (employee_ids[3][0], '2024-05-20', 'Report', 'Filed quarterly compliance report'),
    (employee_ids[3][0], '2024-06-20', 'Review', 'Review of internal compliance policies')
]

cursor.executemany("INSERT INTO compliance (employee_id, date, type, description) VALUES (%s, %s, %s, %s)", compliance)
cnx.commit()

# Insert billing records using client_ids
billings = [
    (client_ids[0][0], '2024-01-25', 500.00, 'Paid'),
    (client_ids[1][0], '2024-02-25', 700.00, 'Pending'),
    (client_ids[2][0], '2024-03-25', 800.00, 'Paid'),
    (client_ids[3][0], '2024-04-25', 600.00, 'Pending'),
    (client_ids[4][0], '2024-05-25', 900.00, 'Paid'),
    (client_ids[5][0], '2024-06-25', 1000.00, 'Pending')
]

cursor.executemany("INSERT INTO billing (client_id, date, amount, status) VALUES (%s, %s, %s, %s)", billings)
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
