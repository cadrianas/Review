import csv
from fpdf import FPDF  # For PDF generation

def filter_and_write_to_file(csv_file, column_name, output_file):
    filtered_entries = []

    # Read the CSV file and filter the entries
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            entry = row[column_name]  # Assuming column_name is the column containing entries
            if not ('\\cite{' in entry and 'No abstract provided' in entry):
                filtered_entries.append(entry)

    # Write the filtered entries to a PDF or TXT file
    if output_file.endswith('.pdf'):
        write_to_pdf(filtered_entries, output_file)
    elif output_file.endswith('.txt'):
        write_to_txt(filtered_entries, output_file)
    else:
        print("Unsupported output format. Please provide a .pdf or .txt file.")

def write_to_pdf(entries, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for entry in entries:
        lines = pdf.multi_cell(0, 10, txt=entry.encode('latin-1', 'replace').decode('latin-1'))  # Use 'replace' to replace unsupported characters
        remaining_lines = len(lines) - pdf.page_break_trigger
        if remaining_lines > 0:
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt='\n'.join(lines[-remaining_lines:]))
    pdf.output(output_file, 'F')

def write_to_txt(entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for entry in entries:
            file.write(entry + '\n')
# Usage example
csv_file = 'SIR_improved_final_v2.csv'
column_name = 'New Column'
output_file = 'summary.txt'  # Change to 'output.txt' if you want to generate a TXT file
filter_and_write_to_file(csv_file, column_name, output_file)