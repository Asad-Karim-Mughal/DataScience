import pandas as pd

df = pd.read_csv('data.csv')
## Tip: use to_string() to print the entire DataFrame.
print(df.to_string())

## If you have a large DataFrame with many rows, Pandas will only return the first 5 rows, and the last 5 rows:
print(df) 