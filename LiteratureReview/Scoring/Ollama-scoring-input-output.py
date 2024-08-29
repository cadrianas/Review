import os
import csv
import pathlib
import time
import re
import ollama
import random
from requests.exceptions import RequestException

# Function to check if the SIR model is mentioned
def mentions_SIR(content):
    return "SIR" in content or "susceptible-infected-recovered" in content

# Function to analyze a given prompt using Ollama
def analyze_with_ollama(ollama_client, prompt, max_retries=5, backoff_factor=1, timeout=10):
    for attempt in range(max_retries):
        try:
            response = ollama_client.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}]
            )
            response_text = response['message']['content'].strip()
            return response_text
        except (RequestException, TimeoutError) as e:
            print(f"Request error: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
            time.sleep(backoff_factor * (2 ** attempt))
            continue
        except Exception as e:
            print(f"Unexpected error: {e}.")
            return None
    print("Max retries reached. Unable to generate score.")
    return None

# Function to generate scoring and summary using Ollama
def generate_scoring(text_content, max_retries=5, backoff_factor=1, timeout=10):
    try:
        ollama_client = ollama.Client()

        relevance_prompt = f"Assess the relevance of the following text:\n\n{text_content}"
        relevance_response = analyze_with_ollama(ollama_client, relevance_prompt, max_retries, backoff_factor, timeout)

        clarity_prompt = f"Assess the clarity of the following text on a scale from 0 to 10:\n\n{text_content}"
        clarity_response = analyze_with_ollama(ollama_client, clarity_prompt, max_retries, backoff_factor, timeout)

        depth_prompt = f"Assess the depth of analysis of the following text on a scale from 0 to 10:\n\n{text_content}"
        depth_response = analyze_with_ollama(ollama_client, depth_prompt, max_retries, backoff_factor, timeout)

        novelty_prompt = f"Assess the novelty of the following text on a scale from 0 to 10:\n\n{text_content}"
        novelty_response = analyze_with_ollama(ollama_client, novelty_prompt, max_retries, backoff_factor, timeout)

        summary_prompt = f"Summarize the following abstract in 200 words or less; do not say anything but the summary:\n\n{text_content}"
        summary_response = analyze_with_ollama(ollama_client, summary_prompt, max_retries, backoff_factor, timeout)

        return relevance_response, clarity_response, depth_response, novelty_response, summary_response

    except Exception as e:
        print(f"Error generating scoring: {e}")
        return None, None, None, None, None

# Function to identify the model based on the text content
def identify_model(text):
    model_patterns = [
        ('Logistic Regression', r'Logistic\s*Regression'),
        ('Random Forest', r'Random\s*Forest'),
        ('Support Vector Machine', r'Support\s*Vector\s*Machine'),
        ('SIR-Type/deterministic', r'SIR|SIRD|SEIR|SLIR|deterministic\s*model|compartmental'),
        ('ARIMA', r'ARIMA'),
        ('Stochastic', r'stochastic'),
        ('Agent Based', r'Agent\s*Based')
    ]

    for model, pattern in model_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return model

    return "Model not identified"

# Set input and output directories
input_folder_path = pathlib.Path('/home/cadrianas/NAS-small-DATA/adriana-llm-reviews/pdfs/')
output_folder_path = pathlib.Path('/home/cadrianas/NAS-small-OUTPUT/adriana-llm-reviews/pdfs/')
log_file_path = output_folder_path / 'processed_files.log'

# Ensure output folder exists
output_folder_path.mkdir(parents=True, exist_ok=True)

# Load processed files from the log file
if log_file_path.exists():
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        processed_files = set(line.strip() for line in log_file)
else:
    processed_files = set()

# List all files in the input directory
text_files = [f for f in os.listdir(input_folder_path) if f.endswith('.txt')]
files_processed = 0

# Process files
while files_processed < len(text_files):
    random_file = random.choice(text_files)
    text_files.remove(random_file)  # Ensure the file is not picked again

    if random_file in processed_files:
        continue  # Skip already processed files

    file_path = input_folder_path / random_file
    file_stem = file_path.stem

    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Generate scoring
    relevance_response, clarity_response, depth_response, novelty_response, summary_response = generate_scoring(text_content)

    # Identify the model in the text
    identified_model = identify_model(text_content)

    # Define output CSV path per file
    output_csv_path = output_folder_path / f'scoring_{file_stem}.csv'

    # Determine if both scoring and summary failed
    if relevance_response is None and summary_response is None:
        # Write a CSV indicating that both scoring and summary failed
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['File Name', 'Relevance Response', 'Clarity Response', 'Depth Response', 'Novelty Response', 'Summary', 'Identified Model']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'File Name': file_stem,
                'Relevance Response': 'Scoring and summary failed',
                'Clarity Response': 'Scoring and summary failed',
                'Depth Response': 'Scoring and summary failed',
                'Novelty Response': 'Scoring and summary failed',
                'Summary': 'Scoring and summary failed',
                'Identified Model': identified_model
            })
    else:
        # Save the results to a CSV file, including partial results
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['File Name', 'Relevance Response', 'Clarity Response', 'Depth Response', 'Novelty Response', 'Summary', 'Identified Model']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'File Name': file_stem,
                'Relevance Response': relevance_response if relevance_response is not None else 'Scoring failed',
                'Clarity Response': clarity_response if clarity_response is not None else 'Scoring failed',
                'Depth Response': depth_response if depth_response is not None else 'Scoring failed',
                'Novelty Response': novelty_response if novelty_response is not None else 'Scoring failed',
                'Summary': summary_response if summary_response is not None else 'Summary failed',
                'Identified Model': identified_model
            })

    # Log the processed file
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{random_file}\n")

    files_processed += 1
    print(f"Processed {files_processed}/{len(text_files)}: {file_stem}")

print(f"Processing complete. Total files processed: {files_processed}")

