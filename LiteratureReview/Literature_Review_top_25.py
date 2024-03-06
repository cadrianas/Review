import requests
from PyPDF2 import PdfReader
from transformers import T5Tokenizer, T5ForConditionalGeneration
from summarizer import Summarizer
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
    return text

# Function to extract text from PDF given a URL
def extract_text_from_pdf_url(pdf_url):
    response = requests.get(pdf_url)
    with open("document.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    return extract_text_from_pdf("document.pdf")

# Function for combined summarization
def combined_summarization(document, top_n=10):
    if pd.isna(document):
        return "No content to summarize."
    document = str(document)
    extractive_summary = extractive_model(document, num_sentences=top_n)
    input_ids = tokenizer.encode("summarize: " + extractive_summary, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=350, length_penalty=1.5, num_beams=7, early_stopping=False)
    abstractive_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return abstractive_summary

# Load pre-trained models and tokenizers
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
extractive_model = Summarizer()

# Read the CSV file containing URLs
url_data = pd.read_csv('top_25_papers.csv')

# Initialize a list to store summaries
summaries = []

# Iterate over each URL in the DataFrame
# Iterate over each URL in the DataFrame
for index, row in url_data.iterrows():
    # Check if the URL is not missing or empty
    if pd.notnull(row['openAccessPdf']) and row['openAccessPdf'] != '':
        # Extract text from PDF URL
        document_text = extract_text_from_pdf_url(row['openAccessPdf'])
        # Generate summary
        summary = combined_summarization(document_text)
        # Append summary along with other relevant information to the list
        summaries.append({
            'URL': row['openAccessPdf'],
            'Summary': summary
        })
    else:
        logging.warning(f"Skipping row {index + 1}: Missing or empty URL")


# Convert the list of summaries to a DataFrame
summary_df = pd.DataFrame(summaries)

# Save the DataFrame to a new CSV file
summary_df.to_csv('document_summaries.csv', index=False)
