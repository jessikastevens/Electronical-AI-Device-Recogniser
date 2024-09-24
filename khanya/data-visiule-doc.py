import pandas as pd
import numpy as np
import os

# Function to find outliers using IQR
def find_outliers_IQR(df):
    numeric_df = df.select_dtypes(include=[np.number])  # Select only numeric columns
    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[((numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return outliers

# Initialize the row counter
start_row = 0
chunk_size = 100
file_path = r'khanya\acs-f2-dataset 1.csv'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

# Check if the file is empty
if os.path.getsize(file_path) == 0:
    raise ValueError(f"The file {file_path} is empty.")

while True:
    # Read the next chunk of the CSV file
    try:
        df = pd.read_csv(file_path, skiprows=start_row, nrows=chunk_size, header=None)
    except pd.errors.EmptyDataError:
        print(f"No data found in the file {file_path} at rows {start_row} to {start_row + chunk_size}.")
        break
    
    # If the dataframe is empty, break the loop
    if df.empty:
        print(f"Empty dataframe encountered at rows {start_row} to {start_row + chunk_size}.")
        break
    
    # Process the dataframe (e.g., find outliers)
    outliers = find_outliers_IQR(df)
    print(outliers)
    
    # Update the row counter
    start_row += chunk_size
    # Clear the outlier file if it exists
    outlier_file_path = 'khanya\outlier_data.csv'
    if os.path.exists(outlier_file_path):
        os.remove(outlier_file_path)
    
    # Add a column to note the original row numbers of the outliers
    outliers['original_row'] = outliers.index + start_row
    
    # Append the outliers to the outlier_data.csv file
    outliers.to_csv('khanya\outlier_data.csv', mode='a', header=not os.path.exists('khanya\outlier_data.csv'), index=False)