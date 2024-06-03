
import os
import csv
import ollama

def summarize_bib_entry(ollama_client, bib_entry):
    """Summarizes a bib entry using Ollama.

    Args:
        ollama_client: An Ollama client instance.
        bib_entry: The BibTeX entry to summarize.

    Returns:
        A summary of the BibTeX entry.
    """
    # Summarize using Ollama
    summary_response = ollama_client.chat(
        model='llama2:13b',
        messages=[{'role': 'user', 'content': f'Summarize the following text in 200 words or less; include author names, do not say anything but the summary: {bib_entry}'}]
    )
    summary = summary_response['message']['content']
    return summary

def process_csv_file(ollama_client, input_csv_path, output_csv_path):
    """Processes a CSV file containing BibTeX entries and writes the summaries to another CSV file.

    Args:
        ollama_client: An Ollama client instance.
        input_csv_path: Path to the input CSV file.
        output_csv_path: Path to the output CSV file.
    """
    with open(input_csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the header row

        # Check if 'BibTeX' column exists
        if 'BibTeX' not in headers:
            raise ValueError("Input CSV file must contain a 'BibTeX' column.")

        bibtex_index = headers.index('BibTeX')
        
        # Prepare output CSV
        with open(output_csv_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Summary", "BibTeX"])  # Write header

            # Process each row
            for row in reader:
                bib_entry = row[bibtex_index]
                summary = summarize_bib_entry(ollama_client, bib_entry)
                writer.writerow([summary, bib_entry])

def main():
    """Main function to process BibTeX entries from a CSV file."""
    # Input CSV file path containing BibTeX entries
    input_csv_path = "papers_V4.csv"

    # Output directory and CSV file path
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    output_csv_path = os.path.join(output_dir, "output_ollama_using_csv.csv")

    # Connect to Ollama server
    ollama_client = ollama.Client()

    # Process the CSV file
    process_csv_file(ollama_client, input_csv_path, output_csv_path)

if __name__ == "__main__":
    main()
