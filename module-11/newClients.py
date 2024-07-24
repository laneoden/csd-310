import mysql.connector
import pandas as pd

# Connect to MySQL server
cnx = mysql.connector.connect(user="root", password="popcorn", host="127.0.0.1", database="willson")
cursor = cnx.cursor()

# Query to get the count of new clients added in each of the past six months
query = """
SELECT DATE_FORMAT(client_DOR, '%Y-%m') as month, COUNT(*) as new_clients
FROM client
WHERE client_DOR >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY DATE_FORMAT(client_DOR, '%Y-%m')
ORDER BY month;
"""

# Execute the query and fetch the results
cursor.execute(query)
results = cursor.fetchall()

# Create a DataFrame for better visualization
df_new_clients = pd.DataFrame(results, columns=['Month', 'New Clients'])
print(df_new_clients)

# Close the cursor and connection
cursor.close()
cnx.close()