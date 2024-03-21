import os
import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification, PegasusTokenizer, PegasusForConditionalGeneration
from summarizer import Summarizer
from multiprocessing import Pool

# Set display options
pd.set_option('display.max_colwidth', None)

# Load data
data = pd.read_csv('LiteratureReview/classification_results_bibtex.csv')

# Define summarization function
def combined_summarization(document, model_name, model_type='BERT', top_n=3):
    # Handle NaN values
    if document.isna().any():
        return "No content to summarize."

    # Convert abstract to string
    document = str(document)

    # Load pre-trained models and tokenizers
    extractive_model = Summarizer()
    if model_type == 'BERT':
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)
    elif model_type == 'Pegasus':
        tokenizer = PegasusTokenizer.from_pretrained(model_name)
        model = PegasusForConditionalGeneration.from_pretrained(model_name)
    else:
        raise ValueError("Invalid model type. Choose 'BERT' or 'Pegasus'.")

    # Extractive summarization
    extractive_summary = extractive_model(document, num_sentences=top_n)

    # Tokenize input for model
    inputs = tokenizer(extractive_summary, return_tensors="pt", truncation=True, max_length=512)

    # Perform sequence classification or conditional generation
    if model_type == 'BERT':
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = logits.softmax(dim=-1)
        summary_class = probabilities.argmax().item()
        summary_label = model.config.id2label[summary_class]
        return summary_label
    elif model_type == 'Pegasus':
        summary_ids = model.generate(inputs['input_ids'], max_length=100, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

# Define a function to process each row in parallel
def process_row(row):
    row['summary_BERT'] = combined_summarization(row['abstract'], 'bert-base-uncased', 'BERT')
    row['summary_Pegasus'] = combined_summarization(row['abstract'], 'google/pegasus-xsum', 'Pegasus')
    return row

if __name__ == '__main__':
    # Determine number of processes to use
    num_processes = os.cpu_count() - 1

    # Split the data into chunks for parallel processing
    data_split = np.array_split(data, num_processes)

    # Create a pool of worker processes
    with Pool(num_processes) as pool:
        # Process each chunk of data in parallel
        processed_data = pool.map(process_row, data_split)

    # Concatenate the processed chunks back into a single DataFrame
    processed_data = pd.concat(processed_data)

    # Save the results in a single CSV file
    output_csv = 'outputs/classification_results_bibtex_sum.csv'
    processed_data.to_csv(output_csv, index=False)
    print(f"Summaries saved to '{output_csv}'.")
