import pandas as pd
from transformers import BartTokenizer, BartForConditionalGeneration, PegasusTokenizer, PegasusForConditionalGeneration

# Load data
data = pd.read_csv('LiteratureReview/classification_results_bibtex.csv')

# Load Pegasus tokenizer and model for summarization
pegasus_tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-xsum')
pegasus_model = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum')

# Load BART tokenizer and model for summarization
bart_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
bart_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')


def bart_summarization(document):
    if pd.isna(document):
        return "No content to summarize."

    inputs = bart_tokenizer(document, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = bart_model.generate(inputs['input_ids'], max_length=150, min_length=40, length_penalty=2.0,
                                      num_beams=4, early_stopping=True)
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


def pegasus_summarization(document):
    if pd.isna(document):
        return "No content to summarize."

    inputs = pegasus_tokenizer(document, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
    summary_ids = pegasus_model.generate(inputs['input_ids'], max_length=100, min_length=50, length_penalty=2.0,
                                         num_beams=4, early_stopping=True)
    summary = pegasus_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


# Generate summaries for each document using BERT
data['summary_BART'] = data['abstract'].apply(bart_summarization)

# Generate summaries for each document using Pegasus
data['summary_Pegasus'] = data['abstract'].apply(pegasus_summarization)

# Save the results in a single CSV file
output_csv = 'LiteratureReview/outputs/classification_results_bibtex_sum.csv'
data.to_csv(output_csv, index=False)
print(f"Summaries saved to '{output_csv}'.")
