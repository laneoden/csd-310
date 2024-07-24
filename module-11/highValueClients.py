import mysql.connector
import pandas as pd

# Connect to MySQL server
cnx = mysql.connector.connect(user="root", password="popcorn", host="127.0.0.1", database="willson")
cursor = cnx.cursor()

# Query to find clients with more than 2 transactions in any month
query = """
SELECT client.client_name, DATE_FORMAT(transaction.date, '%Y-%m') as month, COUNT(*) as transaction_count
FROM transaction
JOIN account ON transaction.account_id = account.account_id
JOIN client ON account.client_id = client.client_id
GROUP BY client.client_name, DATE_FORMAT(transaction.date, '%Y-%m')
HAVING transaction_count > 2;
"""

# Execute the query and fetch the results
cursor.execute(query)
results = cursor.fetchall()

# Create a DataFrame for better visualization
df_high_trans_clients = pd.DataFrame(results, columns=['Client Name', 'Month', 'Transaction Count'])
print(df_high_trans_clients)

# Close the cursor and connection
cursor.close()
cnx.close()
