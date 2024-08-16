import os
import pandas as pd

# Directory containing the CSV files
directory = 'outputs'

# Get a sorted list of all CSV files in the directory
csv_files = sorted([f for f in os.listdir(directory) if f.startswith('output_chunk_') and f.endswith('.csv')])

# Initialize an empty list to hold the dataframes
df_list = []

# Loop through the CSV files and read them into a list of dataframes
for file in csv_files:
    df = pd.read_csv(os.path.join(directory, file))
    df_list.append(df)

# Concatenate all the dataframes in the list into a single dataframe
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('/outputs/summary_merge/merged_output_summary.csv', index=False)

print("Files merged successfully!")
