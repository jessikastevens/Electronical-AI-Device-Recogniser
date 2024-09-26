import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the first 1000 rows of the CSV file into a DataFrame
df = pd.read_csv(r'c:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/data managment/acs-f2-dataset.csv', nrows=500)

# Plot Current against Time
plt.figure(figsize=(10, 6))
plt.scatter(df.iloc[:, 1], df.iloc[:, 5], color='orange',edgecolors='black', linewidth=0.5)
plt.title('volt vs Time')
plt.xlabel('Time')
plt.ylabel('Current')
plt.grid(True)
plt.show()
