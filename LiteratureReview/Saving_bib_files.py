# the BibTeX files will be organized within a single folder named "Bib files"
# We iterate over each row of the CSV file.
# For each row, we extract the BibTeX content from the
# citation_bibtex column and the citation_key.
# We also extract the Model_final and the year of publication.
# We organize the BibTeX files into folders based on the
# Model_final and then further categorize them based on the year.
# We write each BibTeX content into a separate file named
# after the citation_key within the appropriate year folder.

import csv
import os
import re

def save_citation_bib_files(csv_file):
    # Read the CSV file and process each row
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            citation_bibtex = row['citation_bibtex']
            citation_key = row['citation_key']
            model_final = row['Model_final']
            year_match = re.search(r'year\s*=\s*{(\d+)}', citation_bibtex)
            if year_match:
                year = year_match.group(1)
                folder_path = os.path.join('Bib files', model_final, year)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                bib_file_path = os.path.join(folder_path, f"{citation_key}.bib")
                with open(bib_file_path, 'w') as bib_file:
                    # Add URL entry only if it's not empty
                    if row['openAccessPdf'].strip():  # Check if URL is not empty
                        modified_bibtex = re.sub(r'year\s*=\s*{\d+}', f'year = {{{year}}},\nurl = {{{row["openAccessPdf"].rstrip(",")}}},', citation_bibtex)
                        # Add abstract if available
                        if row['abstract'].strip():  # Check if abstract is not empty
                            modified_bibtex = modified_bibtex[:-2] + f',\n  abstract = {{{row["abstract"]}}}\n}}'
                    else:
                        modified_bibtex = citation_bibtex  # Keep the original BibTeX if URL is empty
                    bib_file.write(modified_bibtex)

# Usage
csv_file = 'classification_results_bibtex.csv'
save_citation_bib_files(csv_file)













