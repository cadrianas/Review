import os
import csv
import pathlib
import time
import ollama
from requests.exceptions import RequestException, Timeout

# Function to check if the SIR model is mentioned
def mentions_SIR(content):
    return "SIR" in content or "susceptible-infected-recovered" in content

# Function to analyze a given prompt using Ollama with a timeout
def analyze_with_ollama(ollama_client, prompt, max_retries=5, backoff_factor=1, timeout=10):
    for attempt in range(max_retries):
        try:
            response = ollama_client.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}],
                timeout=timeout  # Set the timeout for the request
            )
            score = int(response['message']['content'].strip())
            return score
        except (RequestException, Timeout) as e:
            print(f"Request error: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
            time.sleep(backoff_factor * (2 ** attempt))
            continue
    print("Max retries reached. Unable to generate score.")
    return 0

# Function to generate scoring using Ollama
def generate_scoring(text_content, max_retries=5, backoff_factor=1, timeout=10):
    try:
        ollama_client = ollama.Client()

        # Check for SIR model usage
        sir_score = 30 if mentions_SIR(text_content) else 0

        # Define the prompts for scoring
        relevance_prompt = f"Assess the relevance of the following text on a scale from 1 to 100:\n\n{text_content}"
        relevance_score = analyze_with_ollama(ollama_client, relevance_prompt, max_retries, backoff_factor, timeout)

        clarity_prompt = f"Assess the clarity of the following text on a scale from 1 to 100:\n\n{text_content}"
        clarity_score = analyze_with_ollama(ollama_client, clarity_prompt, max_retries, backoff_factor, timeout)

        depth_prompt = f"Assess the depth of analysis of the following text on a scale from 1 to 100:\n\n{text_content}"
        depth_score = analyze_with_ollama(ollama_client, depth_prompt, max_retries, backoff_factor, timeout)

        novelty_prompt = f"Assess the novelty of the following text on a scale from 1 to 100:\n\n{text_content}"
        novelty_score = analyze_with_ollama(ollama_client, novelty_prompt, max_retries, backoff_factor, timeout)

        # Calculate the overall scoring as the weighted average
        overall_score = (relevance_score + clarity_score + depth_score + novelty_score) / 4
        final_score = (sir_score * 0.3) + (overall_score * 0.7)

        return relevance_score, clarity_score, depth_score, novelty_score, final_score

    except Exception as e:
        print(f"Error generating scoring: {e}")
        return 0, 0, 0, 0, 0

# Define folder name containing text files
folder_name = '~/pdfs'

# Define output folder and CSV file
output_folder = '~/Scoring'
output_csv_filename = 'scoring.csv'

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)
output_csv_path = pathlib.Path(output_folder) / output_csv_filename

# Initialize the CSV file if it doesn't exist
if not os.path.exists(output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Relevance Score', 'Clarity Score', 'Depth Score', 'Novelty Score', 'Final Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Define the maximum number of files to process for testing
max_files_to_process = 3
files_processed = 0

# Iterate over text files in the folder
folder_path = pathlib.Path(folder_name)
text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Process each file
for file_name in text_files:
    if files_processed >= max_files_to_process:
        break  # Exit the loop after processing the desired number of files

    # Read text content from the file
    with open(folder_path / file_name, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Generate scoring
    relevance_score, clarity_score, depth_score, novelty_score, final_score = generate_scoring(text_content)

    # Save results to the CSV immediately
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Relevance Score', 'Clarity Score', 'Depth Score', 'Novelty Score', 'Final Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'File Name': file_name,
            'Relevance Score': relevance_score,
            'Clarity Score': clarity_score,
            'Depth Score': depth_score,
            'Novelty Score': novelty_score,
            'Final Score': final_score
        })

    # Increment the processed files counter
    files_processed += 1

    print(f"Processed file {files_processed}/{max_files_to_process}: {file_name}")

print(f"Test complete. Processed {files_processed} files.")
