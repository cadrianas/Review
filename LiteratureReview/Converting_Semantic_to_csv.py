import pandas as pd
import json
import argparse


def convert_jsonl_to_csv(jsonl_file, csv_file):
    """Converts a JSONL file to a CSV file with progress display.

    Args:
        jsonl_file (str): Path to the input JSONL file.
        csv_file (str): Path to the output CSV file.
    """
    with open(jsonl_file, 'r') as input_file:
        data = []
        total_lines = sum(1 for _ in input_file)
        input_file.seek(0)

        for line_num, line in enumerate(input_file, start=1):
            entry = json.loads(line)

            # Flatten authors into separate columns
            for i, author in enumerate(entry.get('authors', [])):
                entry[f'author_name_{i + 1}'] = author.get('name', '')
                entry[f'author_id_{i + 1}'] = author.get('authorId', '')

            # Remove the original 'authors' list
            del entry['authors']

            # Add journal, publicationVenue, publicationTypes, and openAccessPdf fields
            if entry.get('journal'):
                entry['journal_name'] = entry['journal'].get('name', '')
                del entry['journal']
            else:
                entry['journal_name'] = ''

            if entry.get('publicationVenue'):
                entry['publicationVenue_id'] = entry['publicationVenue'].get('id', '')
                entry['publicationVenue_name'] = entry['publicationVenue'].get('name', '')
                entry['publicationVenue_type'] = entry['publicationVenue'].get('type', '')
                entry['publicationVenue_issn'] = entry['publicationVenue'].get('issn', '')
                entry['publicationVenue_url'] = entry['publicationVenue'].get('url', '')
                del entry['publicationVenue']
            else:
                entry['publicationVenue_id'] = ''
                entry['publicationVenue_name'] = ''
                entry['publicationVenue_type'] = ''
                entry['publicationVenue_issn'] = ''
                entry['publicationVenue_url'] = ''

            publication_types = entry.get('publicationTypes', [])
            if isinstance(publication_types, list):
                entry['publicationTypes'] = ', '.join(publication_types)
            else:
                entry['publicationTypes'] = publication_types

            if entry.get('openAccessPdf'):
                entry['openAccessPdf_url'] = entry['openAccessPdf'].get('url', '')
                entry['openAccessPdf_status'] = entry['openAccessPdf'].get('status', '')
                del entry['openAccessPdf']
            else:
                entry['openAccessPdf_url'] = ''
                entry['openAccessPdf_status'] = ''

            # Handle citationStyles
            citation_styles = entry.get('citationStyles', {})
            for style, citation in citation_styles.items():
                entry[f'citation_{style}'] = citation

            del entry['citationStyles']

            data.append(entry)

            if line_num % 1000 == 0:
                print(f"Progress: {(line_num / total_lines) * 100:.1f}%")

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Convert a JSONL file to CSV")
    parser.add_argument("input_file", help="Path to the input JSONL file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    args = parser.parse_args()

    # Call the conversion function with command-line arguments
    convert_jsonl_to_csv(args.input_file, args.output_file)
#  python Converting_Semantic_to_csv.py papers_V4.jsonl papers_V4.csv