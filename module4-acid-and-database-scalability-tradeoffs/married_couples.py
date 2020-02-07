import pandas as pd

titanic = pd.read_csv(
    'https://raw.githubusercontent.com/dunkelweizen/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv')

titanic['Mr_Mrs'] = titanic['Name'].apply(lambda x: True if 'Mr' in x else False)


def common_substring(column):
    array = column.to_numpy(dtype=str)
    n = len(array)
    s = array[0]
    l = len(s)
    res = ''
    for i in range(l):
        for j in range(i + 1, l + 1):
            stem = s[i:j]
            k = 1
            for k in range(1, n):
                if stem not in array[k]:
                    break
            if (k + 1 == n and len(res) < len(stem)):
                res = stem
    return stem


print(common_substring(titanic['Mr_Mrs']))
#  that is not what I wanted...
#  more sprint practice on SQL and databases and I'll come back to this
