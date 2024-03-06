# pip install pdfplumber
import os
import pdfplumber
import re
import csv

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None
# Function to identify the model used
def identify_model(text):
    # Define patterns or keywords to search for
    model_patterns = [
        # 1st part indicates the model being referred to in the context of this rule
        # r'XXX\s*yyy': This regular expression pattern matches the phrase "xxx yyy" with optional whitespace between the words.
        ('Logistic Regression', r'Logistic\s*Regression'),
        ('Random Forest', r'Random\s*Forest'),
        ('Support Vector Machine', r'Support\s*Vector\s*Machine'),
        ('SIR-Type/deterministic', r'SIR'),
        ('SIR-Type/deterministic', r'SIRD'),
        ('SIR-Type/deterministic', r'SEIR'),
        ('SIR-Type/deterministic', r'SLIR'),
        ('SIR-Type/deterministic', r'deterministic\s*model'),
        ('ARIMA', r'ARIMA'),
        ('stochastic', r'stochastic'),
        ('Agent Based', r'Agent\s*Based')
        # we need more, but I cannot think of more
    ]

    # Search for patterns in the text
    for model, pattern in model_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return model

    return "Model not identified "


# Directory containing the PDF files
pdf_directory = "Review Top 25"

# Output CSV file path
csv_file_path = "review_top_25_classification.csv"

# Open CSV file for writing
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['PDF Name', 'Model Used'])

    # Iterate over PDF files in the directory
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            model = identify_model(text)
            csv_writer.writerow([pdf_file, model])

print("CSV file created successfully!")