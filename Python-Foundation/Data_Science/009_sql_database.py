import sqlite3
import pandas as pd

# Connect to your existing database
conn = sqlite3.connect("Data_Science/datasets/client_data.db")
cursor = conn.cursor()

# 1. INSERT (Add a brand new row)
cursor.execute(
    "INSERT INTO quotes_table (Quote, Author) VALUES ('Talk is cheap. Show me the code.', 'Linus Torvalds')"
)
conn.commit()  # You must commit changes to save them

# 2. UPDATE (Edit an existing row)
cursor.execute(
    "UPDATE quotes_table SET Author = 'Mr. Einstein' WHERE Author = 'Albert Einstein'"
)
conn.commit()

# 3. DELETE (Remove a row entirely)
cursor.execute("DELETE FROM quotes_table WHERE Author = 'Thomas Edison'")
conn.commit()

# 4. SELECT (Read the entire table to see your modifications)
final_data = pd.read_sql_query("SELECT * FROM quotes_table", conn)

print("--- Final Database State ---")
print(final_data)

conn.close()
