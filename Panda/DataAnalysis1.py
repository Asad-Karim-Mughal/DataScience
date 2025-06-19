import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt





df = pd.read_excel('employee.xlsx')
# print(emp)

# print(emp.info)

# print(emp.head(3))


# emp.describe()

# print(df.describe())

# print(emp.Age.max())



print(df.Age.median())
sns.boxplot(y=df['Age'])  # or x=df['Age'] for horizontal
plt.title("Age Distribution with Median")
plt.show()
print(df.describe())
print(df.isna().sum())


df.fillna({'Department':df.Department.mode()[0],
           'Age':df.Age.mean(),
           'Salary':df.Salary.median()}, inplace=True)
           

print(df.isna())         
