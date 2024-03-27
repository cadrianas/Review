import os
import csv
import re
import ollama

def summarize_bib_file(ollama_client, file_path, output_dir):
    """Summarizes a bib file using Ollama and writes the data to a CSV file.

    Args:
        ollama_client: An Ollama client instance.
        file_path: Path to the bib file.
        output_dir: Directory to write the CSV file.
    """
    with open(file_path, 'r') as bib_file:
        content = bib_file.read()

    # Summarize using Ollama
    summary_response = ollama_client.chat(
        model='llama2:13b',
        messages=[{'role': 'user', 'content': f'Summarize the following text in 200 words or less; include author names, do not say anything but the summary: {content}'}]
    )
    summary = summary_response['message']['content']

    # Write data to CSV
    output_file = os.path.join(output_dir, "output_ollama.csv")
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([summary, content])

def main():
    """Main function to process bib files."""
    # Replace with your desired output directory
    output_dir = "outputs"

    # Create the CSV file with header
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    with open(os.path.join(output_dir, "output_ollama.csv"), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Summary", "Content"])

    # Connect to Ollama server
    ollama_client = ollama.Client()

    # Find bib files in all subdirectories
    for root, dirs, files in os.walk("Bib-files"):
        for file in files:
            if file.endswith(".bib"):
                file_path = os.path.join(root, file)
                summarize_bib_file(ollama_client, file_path, output_dir)

if __name__ == "__main__":
    main()


