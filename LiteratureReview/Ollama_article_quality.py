import os
import csv
import pathlib
import time
import ollama
from requests.exceptions import RequestException

# Function to check if the SIR model is mentioned
def mentions_SIR(content):
    return "SIR" in content or "susceptible-infected-recovered" in content

# Function to analyze a given prompt using Ollama
def analyze_with_ollama(ollama_client, prompt, max_retries=5, backoff_factor=1):
    for attempt in range(max_retries):
        try:
            response = ollama_client.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}]
            )
            score = int(response['message']['content'].strip())
            return score
        except RequestException as e:
            print(f"Request error: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
            time.sleep(backoff_factor * (2 ** attempt))
            continue
    print("Max retries reached. Unable to generate score.")
    return 0

# Function to generate scoring using Ollama
def generate_scoring(text_content, max_retries=5, backoff_factor=1):
    try:
        ollama_client = ollama.Client()

        # Check for SIR model usage
        sir_score = 30 if mentions_SIR(text_content) else 0

        # Define the prompts for scoring
        relevance_prompt = f"Assess the relevance of the following text on a scale from 1 to 100:\n\n{text_content}"
        relevance_score = analyze_with_ollama(ollama_client, relevance_prompt)

        clarity_prompt = f"Assess the clarity of the following text on a scale from 1 to 100:\n\n{text_content}"
        clarity_score = analyze_with_ollama(ollama_client, clarity_prompt)

        depth_prompt = f"Assess the depth of analysis of the following text on a scale from 1 to 100:\n\n{text_content}"
        depth_score = analyze_with_ollama(ollama_client, depth_prompt)

        novelty_prompt = f"Assess the novelty of the following text on a scale from 1 to 100:\n\n{text_content}"
        novelty_score = analyze_with_ollama(ollama_client, novelty_prompt)

        # Calculate the overall scoring as the weighted average
        overall_score = (relevance_score + clarity_score + depth_score + novelty_score) / 4
        final_score = (sir_score * 0.3) + (overall_score * 0.7)

        return final_score

    except Exception as e:
        print(f"Error generating scoring: {e}")
        return 0

# Define folder name containing text files
folder_name = 'pdfs'

# Define output folder and CSV file
output_folder = 'outputs'
output_csv_filename = 'scoring_articles_txt_Ollama.csv'

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)
output_csv_path = pathlib.Path(output_folder) / output_csv_filename

# Initialize the CSV file if it doesn't exist
if not os.path.exists(output_csv_path):
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Final Score']
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

    # Generate scoring
    final_score = generate_scoring(text_content)

    # Append results to the list
    results.append({'File Name': file_name, 'Final Score': final_score})

    # Increment the batch counter
    batch_counter += 1

    # Write to CSV every 100 files
    if batch_counter >= batch_size:
        with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['File Name', 'Final Score']
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
        fieldnames = ['File Name', 'Final Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for result in results:
            writer.writerow(result)

print("Scoring for text files has been written to:", output_csv_path)
