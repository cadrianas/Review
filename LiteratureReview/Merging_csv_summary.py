import os
import pandas as pd

# Directory containing the CSV files
directory = '/LiteratureRieview/outputs/'

# Directory where the merged file will be saved
output_directory = '/LiteratureRieview/outputs/summary_merge/'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get a sorted list of all CSV files in the directory with the correct extension
csv_files = sorted([f for f in os.listdir(directory) if f.startswith('output_chunk_') and f.endswith('.csv.csv')])

# Debugging: Print the list of found files
print("Found files:", csv_files)

# Initialize an empty list to hold the dataframes
df_list = []

# Loop through the CSV files and read them into a list of dataframes
for file in csv_files:
    print(f"Reading {file}...")
    df = pd.read_csv(os.path.join(directory, file))
    df_list.append(df)

# Check if any dataframes were added
if not df_list:
    print("No dataframes to concatenate. Please check the file paths and names.")
else:
    # Concatenate all the dataframes in the list into a single dataframe
    merged_df = pd.concat(df_list, ignore_index=True)

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(os.path.join(output_directory, 'merged_output_summary.csv'), index=False)

    print("Files merged successfully!")
