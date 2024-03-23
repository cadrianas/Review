# using T5 large
import pandas as pd
from summarizer import Summarizer
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

# Set display options
pd.set_option('display.max_colwidth', None)

# Step 1: Load the data
data = pd.read_csv('outputs/classification_results.csv')

# Step 2: Prepare the data (if needed)
# We'll focus on the 'abstract' column
documents = data['abstract'].tolist()

# Step 3: Load pre-trained models and tokenizers
extractive_model = Summarizer()
abstractive_model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
abstractive_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")

# Step 4: Combined Extractive and Abstractive Summarization function
def combined_summarization_pegasus(document, top_n=10):
    # Handle NaN values
    if pd.isna(document):
        return "No content to summarize."

    # Convert abstract to string
    document = str(document)

    # Extractive summarization
    extractive_summary = extractive_model(document, num_sentences=top_n)

    # Abstractive summarization based on the top N sentences from extractive summary
    input_ids = abstractive_tokenizer.encode("summarize: " + extractive_summary, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = abstractive_model.generate(input_ids, max_length=350, length_penalty=1.5, num_beams=7, early_stopping=False)
    abstractive_summary = abstractive_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return abstractive_summary

# Step 5: Generate summaries for each document
data['summary_pegasus'] = data['abstract'].apply(combined_summarization_pegasus)

# Step 6: Display or save the results
data.to_csv('time_dependent_pegasus_summary.csv', index=False)
print("Summaries saved to 'time_dependent_pegasus_summary.csv'.")