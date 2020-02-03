import requests
import pandas as pd
from bs4 import BeautifulSoup

#define URLs
url = 'https://raw.githubusercontent.com/dunkelweizen/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv'
#define dataframe
df = pd.DataFrame(columns = ['survived', 'pclass', 'name', 'age', 'siblings', 'parents', 'fare'])

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
soup = str(soup)
lines = soup.splitlines()
lines.pop(0)
df = pd.DataFrame()
for line in lines:
    survived, pclass, name, sex, age, siblings, parents, fare = line.split(',')
    df = df.append(pd.DataFrame([[survived, pclass, name, sex, age, siblings, parents, fare]], columns=['survived', 'pclass', 'name', 'sex', 'age', 'siblings', 'parents', 'fare']),ignore_index=True)

df.to_csv('titanic_from_raw.csv')
