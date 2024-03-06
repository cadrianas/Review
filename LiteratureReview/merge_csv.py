import csv
import pandas as pd
import re

def merge_and_add_citation_key(papers_csv, citations_csv, output_csv):
    citations_data = {}  # Dictionary to store citations data with titles as keys

    # Read citations CSV file and store data in dictionary
    with open(citations_csv, 'r') as citations_file:
        reader = csv.DictReader(citations_file)
        for row in reader:
            citations_data[row['title']] = row['citation_bibtex']  # Updated column names

    # Merge data with papers CSV file and add citation key column
    with open(papers_csv, 'r') as papers_file, open(output_csv, 'w', newline='') as output_file:
        reader = csv.DictReader(papers_file)
        fieldnames = reader.fieldnames + ['citation_bibtex', 'citation_key']  # Add columns for citations and citation key
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            title = row['title']  # Updated column name
            if title in citations_data:
                row['citation_bibtex'] = citations_data[title]
                row['citation_key'] = extract_citation_key(citations_data[title])
            else:
                row['citation_bibtex'] = 'N/A'  # Or handle the case where citations are not available
                row['citation_key'] = 'N/A'
            writer.writerow(row)

def extract_citation_key(bibtex_entry):
    if isinstance(bibtex_entry, str):
        match = re.search(r'@\w+\{(.*?),', bibtex_entry)
        if match:
            return match.group(1)
    return None

# Usage
citations_csv = 'papers_V4.csv'
papers_csv = 'outputs/classification_results.csv'
output_csv = 'classification_results_bibtex.csv'
merge_and_add_citation_key(papers_csv, citations_csv, output_csv)


#def extract_citation_key(bibtex_entry):
 #   if isinstance(bibtex_entry, str):
#        match = re.search(r'@\w+\{(.*?),', bibtex_entry)
#        if match:
#            return match.group(1)
#    return None

# Load the CSV file
#df = pd.read_csv('outputs/SIR_improved_final.csv')

# Extract citation keys from BibTeX entries
#df['Citation Key'] = df['citation_bibtex'].apply(extract_citation_key)

# Fill any potential None values in the Citation Key column with an empty string
#df['Citation Key'] = df['Citation Key'].fillna('')

# Print some debugging information
#print("Unique Citation Keys:")
#print(df['Citation Key'].unique())
#print("\nRows with Empty Citation Key:")
##df['New Column'] = df.apply(lambda row: "\\cite{" + row['Citation Key'] + "} " + row['improved_summary_V2'] if row['Citation Key'] else row['improved_summary_V2'], axis=1)

# Save the modified DataFrame back to a CSV file
#df.to_csv('SIR_improved_final_v2.csv', index=False)