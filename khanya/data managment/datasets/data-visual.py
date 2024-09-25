import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv(r'c:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/data managment/acs-f2-dataset.csv', nrows=100)

# Plot the first column as a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df.index, df.iloc[:, 1], color='skyblue', edgecolor='black')
plt.title('Scatter Plot of First Column')
plt.xlabel('Index')
plt.ylabel('Value')
plt.grid(True)
plt.show()
