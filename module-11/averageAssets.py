import mysql.connector
import pandas as pd

# Connect to MySQL server
cnx = mysql.connector.connect(user="root", password="popcorn", host="127.0.0.1", database="willson")
cursor = cnx.cursor()

# Query to calculate the average assets
query = """
SELECT AVG(balance) as average_assets
FROM account;
"""

# Execute the query and fetch the results
cursor.execute(query)
results = cursor.fetchall()

# Create a DataFrame for better visualization
df_avg_assets = pd.DataFrame(results, columns=['Average Assets'])
print(df_avg_assets)

# Close the cursor and connection
cursor.close()
cnx.close()
