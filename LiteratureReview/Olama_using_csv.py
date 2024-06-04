import os
import csv
import time
import logging
import ollama
import sys
from httpx import RemoteProtocolError

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def summarize_bib_entry(ollama_client, bib_entry, abstract, max_retries=5, initial_delay=5):
    """Summarize a single BibTeX entry using Ollama with retry logic."""
    attempt = 0
    delay = initial_delay
    while attempt < max_retries:
        try:
            summary_response = ollama_client.chat(
                model='llama2:13b',
                messages=[{'role': 'user', 'content': f'Summarize the following text in 200 words or less; include author names, do not say anything but the summary: {bib_entry} {abstract}'}]
            )
            summary = summary_response['message']['content']
            return summary
        except RemoteProtocolError as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            attempt += 1
            delay *= 2  # Exponential backoff
    raise RuntimeError(f"Failed to summarize after {max_retries} attempts.")

def process_csv_file(ollama_client, input_csv_path, output_csv_path):
    """Process a CSV file with BibTeX entries and abstracts."""
    processed_entries = set()
    if os.path.exists(output_csv_path):
        with open(output_csv_path, mode='r') as outfile:
            reader = csv.reader(outfile)
            next(reader)  # Skip header
            for row in reader:
                processed_entries.add(row[1])  # Assuming Citation_BibTeX is in the second column

    with open(input_csv_path, mode='r') as infile, open(output_csv_path, mode='a', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        for i, row in enumerate(reader):
            bib_entry = row['citation_bibtex']
            abstract = row['abstract']
            if bib_entry in processed_entries:
                logging.info(f"Skipping already processed row {i + 1}")
                continue
            try:
                summary = summarize_bib_entry(ollama_client, bib_entry, abstract)
                writer.writerow([summary, bib_entry, abstract])
                logging.info(f"Processed row {i + 1}")
            except RuntimeError as e:
                logging.error(f"Failed to process row {i + 1}: {e}")

def main():
    """Main function to process the CSV file."""
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_csv_path> <output_csv_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Create the CSV file with header if it does not exist
    if not os.path.exists(output_csv_path):
        with open(output_csv_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Summary", "Citation_BibTeX", "Abstract"])

    # Connect to Ollama server
    ollama_client = ollama.Client()

    # Process the input CSV file
    process_csv_file(ollama_client, input_csv_path, output_csv_path)

if __name__ == "__main__":
    main()
