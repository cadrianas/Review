import csv
import json
import re

def extract_bibtex_from_citation_styles(citation_styles_str):
    # Extract JSON data from the string
    json_data_match = re.search(r'{.*?}', citation_styles_str)
    if json_data_match:
        json_data = json_data_match.group()
        print("Extracted JSON data:", json_data)  # Debugging: Print extracted JSON data
        try:
            citation_styles = json.loads(json_data)
            print("Parsed JSON data:", citation_styles)  # Debugging: Print parsed JSON data
            if 'bibtex' in citation_styles:
                return citation_styles['bibtex']
        except json.JSONDecodeError as e:
            print("JSON decoding error:", e)  # Debugging: Print JSON decoding error
            pass
    return None

def add_bibtex_column(input_csv, output_csv):
    with open(input_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['BibTeX']  # Add a new column for BibTeX

        with open(output_csv, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                citation_styles_str = row.get('citationStyles')
                print("Citation styles data:", citation_styles_str)  # Debugging: Print citation styles data
                if citation_styles_str:
                    bibtex = extract_bibtex_from_citation_styles(citation_styles_str)
                    if bibtex:
                        row['BibTeX'] = bibtex
                    else:
                        row['BibTeX'] = 'N/A'  # Or handle the case where BibTeX is not available
                else:
                    row['BibTeX'] = 'N/A'  # Or handle the case where citation styles are not available
                writer.writerow(row)

def main():
    input_csv = 'outputs/SIR_type_improved copy.csv'  # Replace with your input CSV file
    output_csv = 'output.csv'  # Replace with the desired output CSV file

    add_bibtex_column(input_csv, output_csv)

if __name__ == "__main__":
    main()



