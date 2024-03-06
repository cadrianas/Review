import os
import re
import requests
import pdfplumber
import io
import time
import csv

# Function to identify the model used
def identify_model(text):
    # Define patterns or keywords to search for
    model_patterns = [
        ('Logistic Regression', r'Logistic\s*Regression'),
        ('Random Forest', r'Random\s*Forest'),
        ('Support Vector Machine', r'Support\s*Vector\s*Machine'),
        ('SIR-Type/deterministic', r'SIR|SIRD|SEIR|SLIR|deterministic\s*model'),
        ('ARIMA', r'ARIMA'),
        ('stochastic', r'stochastic'),
        ('Agent Based', r'Agent\s*Based')
        # Add more patterns if needed
    ]

    # Search for patterns in the text
    for model, pattern in model_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return model

    return "Model not identified"


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_content):
    try:
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF content: {e}")
        return None


# Function to classify URLs and update CSV file
def classify_urls(csv_file_path):
    start_time = time.time()  # Start runtime measurement

    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        fieldnames = csv_reader.fieldnames + ['Model']  # Add 'Model' column header
        rows = []

        processing = True  # Flag to indicate whether to process the rows or not

        for idx, row in enumerate(csv_reader, start=1):
            print(f"Current row number: {idx}")

            # Skip processing row 7536
            if idx == 7536:
                continue

            url = row['openAccessPdf']
            if url.strip() == '':
                row['Model'] = 'URL does not exist'
            else:
                try:
                    response = requests.get(url)
                    pdf_content = response.content
                    text = extract_text_from_pdf(pdf_content)
                    if text is not None:
                        row['Model'] = identify_model(text)
                    else:
                        row['Model'] = 'PDF cannot be read'
                except Exception as e:
                    print(f"Error processing URL {url} in row {idx}: {e}")
                    row['Model'] = 'Error processing PDF'
                    print(f"Current row number: {idx}")

            rows.append(row)

        # Write results back to a new CSV file
        new_csv_file_path = "classification_pdf_results.csv"
        with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    end_time = time.time()  # End runtime measurement
    runtime = end_time - start_time  # Calculate total runtime
    print(f"Classification complete. Total runtime: {runtime:.2f} seconds")


# Example usage:
csv_file_path = "processed_papers_V3.csv"
classify_urls(csv_file_path)
