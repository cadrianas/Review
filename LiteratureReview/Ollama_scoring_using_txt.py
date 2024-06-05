import os
import csv
import pathlib
import time
import ollama
from requests.exceptions import RequestException

# Function to generate summary and quality assessment using Ollama
def generate_summary_and_quality(text_content, max_retries=5, backoff_factor=1):
    try:
        # Prepare the input for the generative model
        textbook = f'## Entire Text Content ##\n\n{text_content}'

        # Define the prompt for the Ollama model
        summary_prompt = (
            f"Please summarize the following text in under 200 words:\n\n{textbook}\n\n[END]\n\n"
            "Please assess the quality of the article on a scale from 1 to 10 based on the following criteria: "
            "relevance, clarity, depth of analysis, novelty, and usage of a compartmental mathematical model, the scientific content, methodology, data. "
            "Provide only the overall grade."
        )

        # Generate the summary and quality assessment using the Ollama client
        ollama_client = ollama.Client()

        for attempt in range(max_retries):
            try:
                response = ollama_client.chat(
                    model='llama3',
                    messages=[{'role': 'user', 'content': summary_prompt}]
                )

                # Extract and process the response
                response_content = response['message']['content'].strip()

                # Split the response content to separate summary and quality assessment
                response_lines = response_content.split('\n')

                summary = '\n'.join(response_lines[:-1])  # Assuming the summary is all lines except the last
                quality_assessment = response_lines[-1]  # Assuming the last line is the quality assessment

                return summary, quality_assessment

            except RequestException as e:
                print(f"Request error: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
                time.sleep(backoff_factor * (2 ** attempt))
                continue

        print("Max retries reached. Unable to generate summary and quality assessment.")
        return "Error", "Error"

    except Exception as e:
        print(f"Error generating summary or quality assessment: {e}")
        return "Error", "Error"

# Define folder name containing text files
folder_name = 'pdfs'

# Define output folder and CSV file
output_folder = 'outputs'
output_csv_filename = 'summary_and_quality.csv'

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)
output_csv_path = pathlib.Path(output_folder) / output_csv_filename

# Initialize the CSV file if it doesn't exist
if not os.path.exists(output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Summary', 'Quality Assessment']
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

    # Generate summary and quality assessment
    summary, quality_assessment = generate_summary_and_quality(text_content)

    # Append results to the list
    results.append({'File Name': file_name, 'Summary': summary, 'Quality Assessment': quality_assessment})

    # Increment the batch counter
    batch_counter += 1

    # Write to CSV every 100 files
    if batch_counter >= batch_size:
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['File Name', 'Summary', 'Quality Assessment']
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
        fieldnames = ['File Name', 'Summary', 'Quality Assessment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for result in results:
            writer.writerow(result)

print("Summary and quality assessments for test files have been written to:", output_csv_path)
