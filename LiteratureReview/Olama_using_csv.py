import os
import csv
import ollama
import time
from httpx import RemoteProtocolError

def summarize_bib_entry(ollama_client, bib_entry, abstract, max_retries=3, delay=5):
    """Summarizes a bib entry using Ollama.

    Args:
        ollama_client: An Ollama client instance.
        bib_entry: The BibTeX entry to summarize.
        abstract: The abstract of the BibTeX entry.
        max_retries: Maximum number of retries in case of failure.
        delay: Delay between retries in seconds.

    Returns:
        A summary of the BibTeX entry and abstract.
    """
    combined_content = f"{bib_entry}\n\nAbstract:\n{abstract}"

    for attempt in range(max_retries):
        try:
            summary_response = ollama_client.chat(
                model='llama2:13b',
                messages=[{'role': 'user', 'content': f'Summarize the following text in 200 words or less; include author names, do not say anything but the summary: {combined_content}'}]
            )
            summary = summary_response['message']['content']
            return summary
        except RemoteProtocolError as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return "Error: Could not get summary after multiple attempts."

def process_csv_file(ollama_client, input_csv_path, output_csv_path, batch_size=100):
    """Processes a CSV file containing BibTeX entries and abstracts, and writes the summaries to another CSV file.

    Args:
        ollama_client: An Ollama client instance.
        input_csv_path: Path to the input CSV file.
        output_csv_path: Path to the output CSV file.
        batch_size: Number of rows to process before saving to CSV.
    """
    with open(input_csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the header row

        # Check if required columns exist
        if 'citation_bibtex' not in headers or 'abstract' not in headers:
            raise ValueError("Input CSV file must contain 'citation_bibtex' and 'abstract' columns.")

        bibtex_index = headers.index('citation_bibtex')
        abstract_index = headers.index('abstract')
        
        # Prepare output CSV
        with open(output_csv_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Summary", "citation_bibtex", "abstract"])  # Write header

            batch = []
            row_count = 0

            # Process each row
            for row in reader:
                bib_entry = row[bibtex_index]
                abstract = row[abstract_index]
                summary = summarize_bib_entry(ollama_client, bib_entry, abstract)
                batch.append([summary, bib_entry, abstract])
                row_count += 1

                # Write batch to CSV file every `batch_size` rows
                if row_count % batch_size == 0:
                    writer.writerows(batch)
                    batch.clear()  # Clear the batch after writing to file
                    print(f"{row_count} rows processed and saved to {output_csv_path}")

            # Write any remaining rows in the batch
            if batch:
                writer.writerows(batch)
                print(f"Final batch of {len(batch)} rows processed and saved to {output_csv_path}")

def main():
    """Main function to process BibTeX entries and abstracts from a CSV file."""
    # Input CSV file path containing BibTeX entries and abstracts
    input_csv_path = "papers_V4.csv"

    # Output directory and CSV file path
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    output_csv_path = os.path.join(output_dir, "output_ollama_csv.csv")

    # Connect to Ollama server
    ollama_client = ollama.Client()

    # Process the CSV file
    process_csv_file(ollama_client, input_csv_path, output_csv_path)

if __name__ == "__main__":
    main()
