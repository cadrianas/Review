import os
import pandas as pd
from summarizer import Summarizer
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration

# Set display options
pd.set_option('display.max_colwidth', None)

# Load data
data = pd.read_csv('outputs/classification_results.csv')

# Define summarization function, we use top_n to be 5, so we only want to take
# the 5 most important sentences
def combined_summarization(document, model_name, model_type, top_n=4):
    # Handle NaN values
    if pd.isna(document):
        return "No content to summarize."

    # Convert abstract to string
    document = str(document)

    # Load pre-trained models and tokenizers
    extractive_model = Summarizer()
    if model_type == 'Pegasus':
        abstractive_model = PegasusForConditionalGeneration.from_pretrained(model_name)
        abstractive_tokenizer = PegasusTokenizer.from_pretrained(model_name)
    elif model_type == 'T5':
        abstractive_model = T5ForConditionalGeneration.from_pretrained(model_name)
        abstractive_tokenizer = T5Tokenizer.from_pretrained(model_name)
    else:
        raise ValueError("Invalid model type. Choose 'Pegasus' or 'T5'.")

    # Extractive summarization
    extractive_summary = extractive_model(document, num_sentences=top_n)

    # Abstractive summarization based on the top N sentences from extractive summary
    input_ids = abstractive_tokenizer.encode("summarize: " + extractive_summary, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = abstractive_model.generate(input_ids, max_length=350, length_penalty=1.5, num_beams=7, early_stopping=False)
    abstractive_summary = abstractive_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return abstractive_summary

# Generate summaries for each document and each model
models = {
    'Pegasus-XSUM': ('google/pegasus-xsum', 'Pegasus'),
    #'T5-Small': ('t5-small', 'T5'),
    #'T5-Large': ('t5-large', 'T5'),
    'T5-Base': ('t5-base', 'T5')
}

output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for model_name, (model_path, model_type) in models.items():
    data[f'summary_{model_name}'] = data['abstract'].apply(lambda x: combined_summarization(x, model_path, model_type))

# Save the results in a single CSV file
output_csv = os.path.join(output_folder, 'Results.csv')
data.to_csv(output_csv, index=False)
print(f"Summaries saved to '{output_csv}'.")
