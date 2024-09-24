import pandas as pd

import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('acs-f2-dataset 1.csv')

# Assuming the dataset has columns named 'x' and 'y'
x = data['equipment']
y = data['power']

# Create the scatter plot
plt.scatter(x, y)

# Add title and labels
plt.title('datagraph')
plt.xlabel('equipment')
plt.ylabel('power')

# Show the plot
plt.show()