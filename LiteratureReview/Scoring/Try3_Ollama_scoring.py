import os
import pathlib
import time
import ollama
from requests.exceptions import RequestException, Timeout
import random

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

# Function to process a single text file
def process_text_file(file_path, output_base_dir, input_base_dir):
    try:
        # Read the text content
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        # Generate scores
        relevance_score, clarity_score, depth_score, novelty_score, final_score = generate_scoring(text_content)

        # Determine the output path
        relative_path = file_path.relative_to(input_base_dir)
        output_path = output_base_dir / relative_path.with_suffix('.csv')

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the results to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['File Name', 'Relevance Score', 'Clarity Score', 'Depth Score', 'Novelty Score', 'Final Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'File Name': file_path.name,
                'Relevance Score': relevance_score,
                'Clarity Score': clarity_score,
                'Depth Score': depth_score,
                'Novelty Score': novelty_score,
                'Final Score': final_score
            })

        print(f"Processed and saved results for {file_path}")

    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

# Main function to process all text files
def process_all_files(input_base_dir, output_base_dir):
    input_base_dir = pathlib.Path(input_base_dir)
    output_base_dir = pathlib.Path(output_base_dir)

    # Get list of all input files
    all_input_files = list(input_base_dir.rglob('*.txt'))
    processed_files = set(file.relative_to(output_base_dir).with_suffix('.txt') for file in output_base_dir.rglob('*.csv'))

    # Determine which files need processing
    files_to_process = [file for file in all_input_files if file.relative_to(input_base_dir) not in processed_files]

    while files_to_process:
        # Pick a random file to process
        file_to_process = random.choice(files_to_process)
        process_text_file(file_to_process, output_base_dir, input_base_dir)

        # Update the list of files to process
        files_to_process = [file for file in all_input_files if file.relative_to(input_base_dir) not in processed_files]

    print("All files have been processed.")

# Define input and output directories
INPUT_DIR = '/pdfs'
OUTPUT_DIR = '/Scoring'

# Process all text files
process_all_files(INPUT_DIR, OUTPUT_DIR)

