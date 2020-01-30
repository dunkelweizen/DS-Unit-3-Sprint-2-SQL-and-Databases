import sqlite3
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

data = pd.read_csv('buddymove_holidayiq.csv')

conn = sqlite3.connect("buddymove_holidayiq.sqlite3")
data.to_sql('review', conn, if_exists = 'replace')
curs = conn.cursor()
query = "SELECT * FROM review"

results = curs.execute(query).fetchall()
print("There are", len(results), "rows")

query = """
SELECT COUNT('User Id') FROM review
WHERE Nature >= 100
AND Shopping >= 100;
"""

results = curs.execute(query).fetchall()
print('There are', results[0][0], 'users who rated both Nature and Shopping over 100')


categories = ['Sports', 'Religious', 'Nature', 'Theatre', 'Shopping', 'Picnic']
for item in categories:
    query = f"SELECT SUM({item}) FROM review"
    results = curs.execute(query).fetchall()
    print(f'Average number of reviews for {item} column:', round(results[0][0] / 249))