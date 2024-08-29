import csv
import os
import re

def save_citation_bib_files(csv_file):
    # Define the base folder path
    base_folder_path = 'Bib-files-V2'
    
    # Create the base folder if it does not exist
    if not os.path.exists(base_folder_path):
        os.makedirs(base_folder_path)
    
    # Read the CSV file and process each row
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            citation_bibtex = row['citation_bibtex']
            citation_key = row['citation_key']
            bib_file_path = os.path.join(base_folder_path, f"{citation_key}.bib")
            with open(bib_file_path, 'w') as bib_file:
                # Add URL entry only if it's not empty
                if row['openAccessPdf'].strip():  # Check if URL is not empty
                    modified_bibtex = re.sub(r'year\s*=\s*{\d+}', f'year = {{{row["year"]}}},\nurl = {{{row["openAccessPdf"].rstrip(",")}}},', citation_bibtex)
                    # Add abstract if available
                    if row['abstract'].strip():  # Check if abstract is not empty
                        modified_bibtex = modified_bibtex[:-2] + f',\n  abstract = {{{row["abstract"]}}}\n}}'
                else:
                    modified_bibtex = citation_bibtex  # Keep the original BibTeX if URL is empty
                bib_file.write(modified_bibtex)

# Usage
csv_file = 'papers_V4.csv'
save_citation_bib_files(csv_file)
