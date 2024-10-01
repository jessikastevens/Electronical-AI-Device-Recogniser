import pandas as pd

# Read the CSV files into DataFrames
df1 = pd.read_csv(r'khanya\data managment\outlier_data.csv')  # First CSV file
df2 = pd.read_csv(r'khanya\data managment\acs-f2-dataset.csv')  # Second CSV file

# Extract the values from the 'originalindexvalue' column in df1
values_to_delete = df1['originalIndex'].tolist()

# Delete the corresponding rows in df2
df2 = df2.drop(values_to_delete)  # Drop rows by index in df2

# Save the updated df2 back to a CSV file
df2.to_csv(r'khanya\data managment\acs-f2-dataset.csv', index=False)
if len(df2) < len(pd.read_csv(r'khanya\data managment\acs-f2-dataset.csv')):
    print("success")
else:
    print("oh no something went wrong")
print(df2)
