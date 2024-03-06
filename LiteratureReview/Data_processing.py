import csv
import json

# Function to extract author names
def extract_authors(author_json):
    try:
        authors = json.loads(author_json.replace("'", "\""))
        return [author['name'] for author in authors]
    except json.JSONDecodeError:
        print(f"Error decoding JSON data: {author_json}")
        return []

# Function to extract publication venue details
def extract_publication_details(publication_json):
    try:
        publication_dict = json.loads(publication_json.replace("'", "\""))
        return {
            'publication_name': publication_dict.get('name', ''),
            'publication_url': publication_dict.get('url', ''),
            'journal_name': publication_dict.get('name', ''),  # Extract journal name
        }
    except json.JSONDecodeError:
        print(f"Error decoding JSON data: {publication_json}")
        return {
            'publication_name': '',
            'publication_url': '',
            'journal_name': '',  # Set journal name to empty string
        }

# Function to process the CSV file
def process_csv(input_csv_file, output_csv_file):
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = ['paperId', 'title', 'abstract','citationCount', 'openAccessPdf','journal', 'publicationDate','Model','publicationVenue', 'author1', 'authors', 'author2', 'author3', 'author4', 'author5', 'publication_url', 'publication_name','publicationTypes', 'journal_name']

        rows = []
        for row in reader:
            author_json = row.get('authors', '')
            if author_json:
                authors = extract_authors(author_json)
                for i, author in enumerate(authors, start=1):
                    if i <= 5:  # Ensure only up to 5 authors are added
                        row[f'author{i}'] = author
            else:
                for i in range(1, 6):
                    row[f'author{i}'] = ''

            publication_json = row.get('publicationVenue', '')
            if publication_json:
                publication_details = extract_publication_details(publication_json)
                for key, value in publication_details.items():
                    row[key] = value
            else:
                row['publication_name'] = ''
                row['publication_url'] = ''
                row['journal'] = ''  # Set journal name to empty string

            publication_type_json = row.get('publicationType', '')
            if publication_type_json:
                publication_type = json.loads(publication_type_json.replace("'", "\""))[0]
            else:
                publication_type = ''
            row['publicationTypes'] = publication_type

            rows.append(row)

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# Example usage:
input_csv_file = 'processed_papers_V3_result.csv'
output_csv_file = 'processed_papers_V3_classification.csv'
process_csv(input_csv_file, output_csv_file)
