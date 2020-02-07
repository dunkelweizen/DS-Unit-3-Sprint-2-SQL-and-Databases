import pandas as pd
import numpy as np

titanic = pd.read_csv(
    'https://raw.githubusercontent.com/dunkelweizen/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv')

titanic['Mr_Mrs'] = titanic['Name'].apply(lambda x: True if 'Mr' in x else False)
mr_mrs = titanic[titanic['Mr_Mrs']]
paired_names = pd.DataFrame()
for row in mr_mrs['Name']:
    last_5_chars = row[-5:]
    paired_names[last_5_chars] = titanic['Name'].apply(lambda x:x if last_5_chars in x else np.NaN)

for column in paired_names.columns:
    if paired_names['column'].nunique() > 1:
        print(paired_names[column].max())


#  take a break and go study databases and then come back