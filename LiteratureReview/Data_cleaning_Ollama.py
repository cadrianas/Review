import pandas as pd
import re

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist


# Load the CSV file
df = pd.read_csv('/home/cadrianas/github/Review/LiteratureReview/outputs/output_ollama.csv')

# Define a function to extract citation from "Content" column
def extract_citation(content):
    match = re.search(r'\{(\w+)\d+', content)
    if match:
        return match.group(1)
    else:
        return None

# Apply the function to create the "citation" column
df['citation'] = df['Content'].apply(extract_citation)

# Remove the unnecessary text from "Summary" column
pattern = r'^(Sure! Here is a summary of the text|No problem; here is a summary of the text|Sure, here\'s the summary you requested|Sure! Here is the summary of the text you provided|Sure! Here is the summary of the text in 200 words or less|Sure! Here is the summary of the text in 200 words or less, including author names but not saying anything):'
df['Summary'] = df['Summary'].str.replace(pattern, '', regex=True)
# Save the cleaned DataFrame into a new CSV file in the output directory
cleaned_file_path = os.path.join(output_dir, 'Ollama_outputs_cleaned.csv')
df.to_csv(cleaned_file_path, index=False)



print(f"Cleaned data saved to {cleaned_file_path}")