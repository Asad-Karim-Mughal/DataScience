import pandas as pd

emp = pd.read_excel('employee.xlsx')

print(emp)




##Working with pandas using function


# def bonus(sal):
#     if sal > 200000:
#         return sal *.5
#     elif sal > 150000:
#         return sal*.3
#     elif sal > 100000:
#         return sal*.25
#     elif sal > 75000:
#         return sal*.15
#     else:
#         return sal*0.1
    

# emp["bonus"] = emp.Salary.apply(bonus) 


# # emp['Bonus2'] = emp.Salary.apply(lambda sal:sal*.5 if sal >=)


# print(emp)


emp['Bonus3'] = emp.apply(lambda row: 
                          row['Salary']*.5 if row['Age']>50
                          else row['Salary']*.4 if row['Age'] >=40
                          else row['Salary']*.1, axis=1)


print(emp)    
    


print(emp.tail())


##slicing

## loc / iloc 2 method


print(emp.iloc[5:13 , 0:6])





print(emp.loc[5:12,'Serial':'Salary'])