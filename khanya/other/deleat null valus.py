import pandas as pd

# Load the CSV file
input_file = r'C:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/data managment/alt-acs-f2-dataset.csv'
output_file = r'C:/Users/honey/Documents/placment work/Electronical-AI-Device-Recogniser/khanya/data managment/no-null.csv'
df = pd.read_csv(input_file)

# Define the condition for rows to be deleted
condition = (df.iloc[:, 1] == 0) & (df.iloc[:, 2] == 0.0) & (df.iloc[:, 3] == 0.0) & (df.iloc[:, 4] == 0.0)

# Remove rows that meet the condition
df_cleaned = df[~condition]

# Save the cleaned data to a new CSV file
df_cleaned.to_csv(output_file, index=False)