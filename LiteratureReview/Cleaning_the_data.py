import requests
from PyPDF2 import PdfReader
from transformers import T5Tokenizer, T5ForConditionalGeneration
from summarizer import Summarizer
import pandas as pd

# Load CSV file
papers = pd.read_csv("papers_V3.csv")

# Perform URL cleaning
# Perform string replacements
# Assuming 'openAccessPdf' is the name of your DataFrame column
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("\\{'url':", "", regex=True)
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("', 'status': 'HYBRID'}", "", regex=True)
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("', 'status': 'GOLD'}", "", regex=True)
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("', 'status': 'GREEN'}", "", regex=True)
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("', 'status': 'CLOSED'}", "", regex=True)
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("', 'status': 'BRONZE'}", "", regex=True)
papers['openAccessPdf'] = papers['openAccessPdf'].str.replace("'", "", regex=True)
# Save the updated DataFrame to a new CSV file
papers.to_csv("processed_papers_V3.csv", index=False)