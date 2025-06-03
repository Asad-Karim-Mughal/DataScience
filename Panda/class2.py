#Creating Dataframe
import pandas as pd

# result = {
#     'roll' : [11, 22, 33 , 44 , 55, 66],
#     'name' : ['ali ', 'danish','faisal', ' asad', 'umair', ' waqas'],
#     'python' : [ 90,98,89,78,76,45],
#     'numpy' : [ 78,67,76,78,89,90],
#     'pandas' : [78, 56 , 45, 67, 65, 78 ] 
#     

# df = pd.DataFrame(result)
# print(df)


# df = pd.read_csv('salary_dataset.csv')
# print(df)


df2 = pd.read_excel("employee.xlsx", engine="openpyxl")# print(df)
# print(df2)


df2['Bonus1'] = [50000  if ((des == 'Manager')  or (des == 'Engineer'))  else 40000 if des == 'Accountant'else 30000 if des == 'officer' else 2000 for des in df2.Designation  ]

print(df2)



emp = pd.read_excel("employee.xlsx", engine="openpyxl")# print(df)


emp['Bonus'] = [50000 if age >=60
                   else 40000 if age >= 50
                   else 30000 if age >= 40
                   else 20000 if age >= 30
                   else 10000 if age>20
                   else 5000 for age in emp.Age]


print(emp)


emp['Bonus1'] = [sal* .5 if sal >= 200000
                 else sal *.25 if sal >= 150000
                 else sal *.15 if sal >= 75000
                 else sal*.1 
                 for sal in emp.Salary
                 ]

print(emp)