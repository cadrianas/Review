import requests
from PyPDF2 import PdfReader
from transformers import T5Tokenizer, T5ForConditionalGeneration
from summarizer import Summarizer  # Add import for the extractive summarizer
import pandas as pd  # Add import for pandas

# Step 1: Download the PDF and extract text
pdf_url = "https://journals.itb.ac.id/index.php/cbms/article/download/21177/6429"
response = requests.get(pdf_url)
with open("document.pdf", "wb") as pdf_file:
    pdf_file.write(response.content)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

document_text = extract_text_from_pdf("document.pdf")

# Step 2: Load pre-trained models and tokenizers
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load the extractive summarizer model
extractive_model = Summarizer()

# Step 3: Abstractive Summarization function
def combined_summarization(document, top_n=10):
    # Handle NaN values
    if pd.isna(document):
        return "No content to summarize."

    # Convert abstract to string
    document = str(document)

    # Extractive summarization
    extractive_summary = extractive_model(document, num_sentences=top_n)

    # Abstractive summarization based on the top N sentences from extractive summary
    input_ids = tokenizer.encode("summarize: " + extractive_summary, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=350, length_penalty=1.5, num_beams=7, early_stopping=False)
    abstractive_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return abstractive_summary

# Step 4: Apply summarization to the extracted text
summary_result = combined_summarization(document_text)

# Step 5: Display the generated summary
print("\nGenerated Summary:")
print(summary_result)
