import os

import pandas as pd
from nltk.tokenize import sent_tokenize

# Load the CSV file into a DataFrame
df = pd.read_csv("outputs/Results.csv")
# Function for post-processing and coherence improvement
def improve_coherence(row):
    abstract = row['abstract']
    pegasus_summary = row['summary_Pegasus-XSUM']
    #t5_large_summary = row['summary_T5-Small']
    #t5_small_summary = row['summary_T5-Large']
    t5_base_summary = row['summary_T5-Base']

    # Check if abstract is empty
    if pd.isna(abstract) or abstract.strip() == '':
        return "No abstract provided."

    # Sentence reordering
    summaries = [summary for summary in [pegasus_summary, t5_base_summary] if not pd.isna(summary) and summary.strip() != "No content to summarize"]

    if not summaries:
        return "No content to summarize."

    reordered_sentences = []
    for summary in summaries:
        sentences = sent_tokenize(summary)
        reordered_sentences.extend(sentences)

    # Reorder sentences using some logic (e.g., based on length, position)
    reordered_sentences.sort(key=len, reverse=True)  # Example: Sort by sentence length

    # Combine reordered sentences into a single string
    improved_summary = ' '.join(reordered_sentences)

    return improved_summary

# Apply the function to each row in the DataFrame
df['improved_summary'] = df.apply(improve_coherence, axis=1)
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_csv = os.path.join(output_folder, 'processed_file.csv')
df.to_csv(output_csv, index=False)
