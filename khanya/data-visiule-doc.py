import pandas as pd
import numpy as np

# Sample DataFrame creation from your data
data = {
    "Column1": [0.0] * 100,  # Assuming first column is fixed
    "Column2": [0.0] * 100,
    "Column3": [0.0] * 100,
    "Column4": [0.0] * 100,
    "Column5": [0.0] * 100,
    "Value": [
        227.996, 227.263, 226.679, 226.882, 228.256, 227.825,
        # ... (complete with the rest of your values)
        226.081, 226.183, 226.757, 228.699, 228.962
    ],
    "Date": ["2012-01-22 10:55:08"] * 100  # Sample timestamp
}

# Read data from 'coffee.csv'
df = pd.read_csv('coffee.csv')

# Calculate Q1, Q3 and IQR
Q1 = df['Value'].quantile(0.25)
Q3 = df['Value'].quantile(0.75)
IQR = Q3 - Q1

# Determine outlier thresholds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = df[(df['Value'] < lower_bound) | (df['Value'] > upper_bound)]

print("Outliers:")
print(outliers)
