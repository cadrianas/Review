# pip install requests

import csv
import os
import requests
from urllib.parse import urlparse

# Function to check if URL points to a PDF file
def is_pdf(url):
    headers = requests.head(url).headers
    content_type = headers.get('content-type')
    return content_type == 'application/pdf'

# Function to download PDF from URL with specified filename
def download_pdf(url, title, output_dir):
    session = requests.Session()  # Create a session object
    print(f"Downloading PDF from: {url}")
    filename = f"{title}.pdf"
    print(f"Saving PDF as: {filename}")
    response = session.get(url)  # Use the session object to make the request
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded PDF: {filename}")

# Function to process CSV and download accessible PDFs
def process_csv(csv_file, output_dir):
    invalid_rows = []  # Store invalid rows here
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row.get('openAccessPdf')
            title = row.get('title')
            if url and title:
                try:
                    if is_pdf(url):
                        download_pdf(url, title, output_dir)
                    else:
                        invalid_rows.append(row)  # Add invalid rows to the list
                except requests.exceptions.RequestException as e:
                    print(f"Error accessing URL: {url}, {e}")

    # Write invalid rows to a new CSV file
    invalid_csv_file = os.path.join(output_dir, 'invalid_urls.csv')
    if invalid_rows:
        fieldnames = invalid_rows[0].keys()
        with open(invalid_csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(invalid_rows)
        print(f"Invalid URLs written to: {invalid_csv_file}")
    else:
        print("No invalid URLs found.")

if __name__ == "__main__":
    # Define your CSV file and output directory
    csv_file = 'top_25_papers.csv'
    output_directory = 'Review Top 25'

    # Create output directory if not exists
    os.makedirs(output_directory, exist_ok=True)

    # Process CSV and download accessible PDFs
    process_csv(csv_file, output_directory)
