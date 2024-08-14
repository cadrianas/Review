import os
import csv
import pathlib
import time
import ollama
from requests.exceptions import RequestException

# Function to generate summary using Ollama
def generate_summary(text_content, max_retries=5, backoff_factor=1):
    try:
        # Prepare the input for the generative model
        textbook = f'## Entire Text Content ##\n\n{text_content}'

        # Define the prompt for the Ollama model
        summary_prompt = (
            f"Please summarize the following text in under 150 words:\n\n{textbook}\n\n[END]"
        )

        # Generate the summary using the Ollama client
        ollama_client = ollama.Client()

        for attempt in range(max_retries):
            try:
                response = ollama_client.chat(
                    model='llama3',
                    messages=[{'role': 'user', 'content': summary_prompt}]
                )

                # Extract and process the response
                summary = response['message']['content'].strip()

                return summary

            except RequestException as e:
                print(f"Request error: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
                time.sleep(backoff_factor * (2 ** attempt))
                continue

        print("Max retries reached. Unable to generate summary.")
        return "Error"

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error"

# Define folder name containing text files
folder_name = 'pdfs'

# Define output folder and CSV file
output_folder = 'outputs'
output_csv_filename = 'summaries_using_txt.csv'

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)
output_csv_path = pathlib.Path(output_folder) / output_csv_filename

# Initialize the CSV file if it doesn't exist
if not os.path.exists(output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Iterate over text files in the folder
folder_path = pathlib.Path(folder_name)
text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Process each file
batch_size = 100
batch_counter = 0
results = []

for file_name in text_files:
    # Read text content from the file
    with open(folder_path / file_name, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Generate summary
    summary = generate_summary(text_content)

    # Append results to the list
    results.append({'File Name': file_name, 'Summary': summary})

    # Increment the batch counter
    batch_counter += 1

    # Write to CSV every 100 files
    if batch_counter >= batch_size:
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['File Name', 'Summary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for result in results:
                writer.writerow(result)
        # Reset the batch counter and results list
        batch_counter = 0
        results = []

        print(f"Processed and saved {batch_size} files. Continuing...")

# Write any remaining results to the CSV file
if results:
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for result in results:
            writer.writerow(result)

print("Summaries for text files have been written to:", output_csv_path)
