import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/sharmaroshan/Heart-UCI-Dataset/master/heart.csv")

df.columns = ['Age', 'Sex', "ChestPainType", 'RestBP','Cholesterol', 'FBS', 'RestECG','MaxHR'," ExerciseAngina ", 'Oldpeak', 'ST_Slope',"NumVesselsFluoro",'Thal','Target']


print(df.head(2))

df_encoded = pd.get_dummies(df, columns=['ChestPainType'], drop_first=True)

print(df_encoded.head())


corr_matrix = df.corr()

# Plot the heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Heart Disease Dataset")
plt.tight_layout()
plt.show()


df_encoded = pd.get_dummies(df, columns=['ChestPainType', 'Thal'], drop_first=True)
print(df_encoded.head())


corr = df_encoded.corr()

# Plot the heatmap
plt.figure(figsize=(15, 12))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Heart Disease Dataset (Encoded)", fontsize=16)
plt.tight_layout()
plt.show()