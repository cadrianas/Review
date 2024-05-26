import pandas as pd
import re
import os

# Define the output directory
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Load the CSV file
input_file_path = os.path.join(output_dir, 'output_ollama.csv')
df = pd.read_csv(input_file_path)

# Define a function to extract citation from "Content" column
def extract_citation(content):
    match = re.search(r'@\w+\{([^,\s]+)', content)
    if match:
        return match.group(1)
    else:
        return None

# Define a function to extract URLs from "Content" column
def extract_url(content):
    url_pattern = r'(https?://[^\s]+)'
    match = re.search(url_pattern, content)
    if match:
        # Strip trailing punctuation if any
        url = match.group(1).rstrip('.,;}')
        return url
    else:
        return None

# Apply the function to create the "citation" column
df['citation'] = df['Content'].apply(extract_citation)

# Apply the function to create the "URL" column
df['URL'] = df['Content'].apply(extract_url)

# Apply the text cleaning to remove unnecessary text from "Summary" column
df['Summary'] = df['Summary'].str.replace(r'^.*?:', '', regex=True)

# Create a new column by concatenating "Summary" and citation with \cite{}
df['Summary_with_citation'] = df['Summary'] + r' \cite{' + df['citation'] + '}'

# Save the DataFrame with the new column into the same CSV file
output_file_path = os.path.join(output_dir, 'combined_output_ollama.csv')
df.to_csv(output_file_path, index=False)
print(f"\nCombined data saved to {output_file_path}")
