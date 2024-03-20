import os
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from multiprocessing import Pool
import nltk

 nltk.download('punkt')

# Set display options
pd.set_option('display.max_colwidth', None)

# Load data
data = pd.read_csv('outputs/classification_results_bibtex.csv')


# Define summarization function
def combined_summarization(document, model_name, max_sentences=4):
    # Handle NaN values
    if pd.isna(document):
        return "No content to summarize."

    # Convert abstract to string
    document = str(document)

    # Initialize summarization pipeline
    summarization_pipeline = pipeline("summarization", model=model_name)

    # Extractive summarization
    parser = PlaintextParser.from_string(document, Tokenizer("english"))
    summarizer = LsaSummarizer()
    extractive_summary = []
    for sentence in summarizer(parser.document, max_sentences):
        extractive_summary.append(sentence.__str__())

    # Combine extractive and abstractive summaries
    extractive_text = ' '.join(extractive_summary)
    abstractive_summary = summarization_pipeline(extractive_text, max_length=100, min_length=50, do_sample=False)

    return abstractive_summary[0]['summary_text']


# Function to apply summarization in parallel
def parallel_summarization(data_chunk):
    for model_name, (model_path, model_type) in models.items():
        if model_type == 'transformers':
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            summarization_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)
        else:
            summarization_pipeline = pipeline("summarization", model=model_path)

        data_chunk[model_name] = data_chunk['abstract'].apply(
            lambda x: combined_summarization(x, summarization_pipeline))
    return data_chunk


# Generate summaries in parallel
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define number of processes
num_processes = os.cpu_count() - 1  # Number of CPU cores minus one

# Split data into chunks for parallel processing
chunk_size = len(data) // num_processes
data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Define summarization models
models = {
    'BART': ('facebook/bart-large-cnn', 'transformers'),
    'Pegasus-XSUM': ('google/pegasus-xsum', 'transformers'),
    'BERT': ('bert-base-uncased', 'transformers')
}

# Create a pool of processes
with Pool(num_processes) as pool:
    # Map the parallel_summarization function to each data chunk
    processed_data = pool.map(parallel_summarization, data_chunks)

# Concatenate the processed data chunks back into a single DataFrame
processed_data = pd.concat(processed_data)

# Save the results in a single CSV file
output_csv = os.path.join(output_folder, 'classification_results_bibtex_sum.csv')
processed_data.to_csv(output_csv, index=False)
print(f"Summaries saved to '{output_csv}'.")
