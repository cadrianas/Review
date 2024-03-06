import pandas as pd

# Read the CSV files
data_papers = pd.read_csv('processed_papers_V3.csv')
data_time = pd.read_csv('processed_time_dependent.csv')

# Sort the papers DataFrame by citation count
data_papers.sort_values(by=["citationCount"], axis=0, ascending=False, inplace=True)

# Sort the time-dependent DataFrame by citation count
data_time.sort_values(by=["citationCount"], axis=0, ascending=False, inplace=True)

# Select the top 20 rows from sorted papers DataFrame
top_20_papers = data_papers.head(20)

# Select the top 5 rows from sorted time-dependent DataFrame
top_5_time = data_time.head(5)

# Save the selected rows to new CSV files
top_20_papers.to_csv('top_20_papers.csv', index=False)
top_5_time.to_csv('top_5_papers.csv', index=False)

# Concatenate the DataFrames
merged_df = pd.concat([top_20_papers, top_5_time])

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('top_25_papers.csv', index=False)
