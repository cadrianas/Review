import os
import csv
import pathlib
import time
import re  # Ensure regex is imported for pattern matching
import ollama
from requests.exceptions import RequestException

# Function to check if the SIR model is mentioned
def mentions_SIR(content):
    return "SIR" in content or "susceptible-infected-recovered" in content

# Function to analyze a given prompt using Ollama
def analyze_with_ollama(ollama_client, prompt, max_retries=5, backoff_factor=1, timeout=10):
    for attempt in range(max_retries):
        try:
            # Directly call the Ollama API
            response = ollama_client.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': prompt}]
            )
            response_text = response['message']['content'].strip()
            return response_text  # Return the full descriptive response
        except (RequestException, TimeoutError) as e:
            print(f"Request error: {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds...")
            time.sleep(backoff_factor * (2 ** attempt))
            continue
        except Exception as e:
            print(f"Unexpected error: {e}.")
            return None
    print("Max retries reached. Unable to generate score.")
    return None  # Return None if maximum retries are reached

# Function to generate scoring using Ollama
def generate_scoring(text_content, max_retries=5, backoff_factor=1, timeout=10):
    try:
        ollama_client = ollama.Client()

        # Define the prompts for scoring
        relevance_prompt = f"Assess the relevance of the following text:\n\n{text_content}"
        relevance_response = analyze_with_ollama(ollama_client, relevance_prompt, max_retries, backoff_factor, timeout)
        if relevance_response is None:
            return None, None, None, None  # Return None if scoring fails

        clarity_prompt = f"Assess the clarity of the following text on a scale from 0 to 10:\n\n{text_content}"
        clarity_response = analyze_with_ollama(ollama_client, clarity_prompt, max_retries, backoff_factor, timeout)
        if clarity_response is None:
            return None, None, None, None  # Return None if scoring fails

        depth_prompt = f"Assess the depth of analysis of the following text on a scale from 0 to 10:\n\n{text_content}"
        depth_response = analyze_with_ollama(ollama_client, depth_prompt, max_retries, backoff_factor, timeout)
        if depth_response is None:
            return None, None, None, None  # Return None if scoring fails

        novelty_prompt = f"Assess the novelty of the following text on a scale from 0 to 10:\n\n{text_content}"
        novelty_response = analyze_with_ollama(ollama_client, novelty_prompt, max_retries, backoff_factor, timeout)
        if novelty_response is None:
            return None, None, None, None  # Return None if scoring fails

        return relevance_response, clarity_response, depth_response, novelty_response

    except Exception as e:
        print(f"Error generating scoring: {e}")
        return None, None, None, None

# Function to identify the model based on the text content
def identify_model(text):
    # Define patterns or keywords to search for
    model_patterns = [
        ('Logistic Regression', r'Logistic\s*Regression'),
        ('Random Forest', r'Random\s*Forest'),
        ('Support Vector Machine', r'Support\s*Vector\s*Machine'),
        ('SIR-Type/deterministic', r'SIR|SIRD|SEIR|SLIR|deterministic\s*model|compartmental'),
        ('ARIMA', r'ARIMA'),
        ('Stochastic', r'stochastic'),
        ('Agent Based', r'Agent\s*Based')
        # Add more patterns if needed
    ]

    # Search for patterns in the text
    for model, pattern in model_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return model

    return "Model not identified"

# Ensure these variables are initialized
text_files = os.listdir('pdfs')  # Replace with your folder path
files_processed = 0
# Set the maximum number of files to process to the total number of files in the directory
max_files_to_process = len(text_files)
folder_path = pathlib.Path('pdfs')  # Replace with your folder path
output_csv_path = 'outputs/scoring.csv'  # Define your output CSV file

# Main processing loop
for file_name in text_files:
    if files_processed >= max_files_to_process:
        break  # Exit the loop after processing the desired number of files

    # Read text content from the file
    with open(folder_path / file_name, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Generate scoring
    relevance_response, clarity_response, depth_response, novelty_response = generate_scoring(text_content)

    # Handle the case where scoring could not be generated
    if relevance_response is None:
        print(f"Skipping file {file_name} due to scoring errors.")
        continue

    # Identify the model in the text
    identified_model = identify_model(text_content)

    # Save results to the CSV immediately
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Relevance Response', 'Clarity Response', 'Depth Response', 'Novelty Response', 'Identified Model']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'File Name': file_name,
            'Relevance Response': relevance_response,
            'Clarity Response': clarity_response,
            'Depth Response': depth_response,
            'Novelty Response': novelty_response,
            'Identified Model': identified_model  # Add the identified model
        })

    # Increment the processed files counter
    files_processed += 1

    print(f"Processed file {files_processed}/{max_files_to_process}: {file_name}")

print(f"Processing complete. Total files processed: {files_processed}")
