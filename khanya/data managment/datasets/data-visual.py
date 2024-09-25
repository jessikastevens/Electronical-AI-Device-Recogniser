import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv(r'c:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/data managment/acs-f2-dataset.csv')


# Plot Current against Time
plt.figure(figsize=(10, 6))
plt.plot(df.iloc[:, 6], df.iloc[:, 5], color='orange', marker='x', linestyle='-')
plt.title('Current vs Time')
plt.xlabel('Time')
plt.ylabel('Current')
plt.grid(True)
plt.show()