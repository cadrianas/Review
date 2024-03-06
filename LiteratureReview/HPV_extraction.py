import requests
import pdfplumber

def extract_tables_from_pdf_url(pdf_url):
    try:
        # Download the PDF content
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Initialize a pdfplumber PDF reader
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            # Extract tables from each page
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)

        return tables

    except Exception as e:
        print(f"Error extracting tables from {pdf_url}: {e}")
        return None

# Sample URL for testing
sample_pdf_url = 'https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0072088&type=printable'

# Extract tables from the PDF linked in the URL
extracted_tables = extract_tables_from_pdf_url(sample_pdf_url)

if extracted_tables:
    # Do something with the extracted tables (e.g., print them)
    for i, table in enumerate(extracted_tables):
        print(f"Extracted Table {i + 1}:")
        print(table)
else:
    print("No tables found in the PDF.")
