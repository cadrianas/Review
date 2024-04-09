import pandas as pd
import re
import os

# Define the output directory
output_dir = "/home/cadrianas/github/Review/LiteratureReview/outputs"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Load the CSV file
input_file_path = os.path.join(output_dir, 'output_ollama.csv')
df = pd.read_csv(input_file_path)

# Define a function to extract citation from "Content" column
def extract_citation(content):
    match = re.search(r'\{(\w+)\d+', content)
    if match:
        return match.group(1)
    else:
        return None

# Apply the function to create the "citation" column
df['citation'] = df['Content'].apply(extract_citation)

# Apply the text cleaning to remove unnecessary text from "Summary" column
df['Summary'] = df['Summary'].str.replace(r'^.*?:', '', regex=True)

# Save the cleaned DataFrame into a new CSV file in the output directory
cleaned_file_path = os.path.join(output_dir, 'cleaned_output_ollama.csv')
df.to_csv(cleaned_file_path, index=False)

print(f"\nCleaned data saved to {cleaned_file_path}")
