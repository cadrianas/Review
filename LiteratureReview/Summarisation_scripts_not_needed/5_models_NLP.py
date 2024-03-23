import pandas as pd
from summarizer import Summarizer
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration, \
    PegasusTokenizer, PegasusForConditionalGeneration, BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Step 1: Load the data
data = pd.read_csv('papers.csv')

# Step 2: Prepare the data (if needed)
# We'll focus on the 'abstract' column
documents = data['abstract'].head(2).tolist()

# Step 3: Define model names
model_names = ["t5-large", "t5-base", "facebook/bart-large-cnn", "google/pegasus-large"]

# Step 4: Create a DataFrame to store results
results_df = pd.DataFrame(columns=['Model', 'Title', 'CitationCount', 'PublicationDate', 'Extractive_Summary', 'Abstractive_Summary'])

# Step 5: Loop through models and generate summaries
for model_name in model_names:
    print(f"Generating summaries for {model_name}...")

    if "t5" in model_name:
        extractive_model = Summarizer()
        abstractive_tokenizer = T5Tokenizer.from_pretrained(model_name)
        abstractive_model = T5ForConditionalGeneration.from_pretrained(model_name)
    elif "bart" in model_name:
        extractive_model = Summarizer()
        abstractive_tokenizer = BartTokenizer.from_pretrained(model_name)
        abstractive_model = BartForConditionalGeneration.from_pretrained(model_name)
    elif "pegasus" in model_name:
        extractive_model = Summarizer()
        abstractive_tokenizer = PegasusTokenizer.from_pretrained(model_name)
        abstractive_model = PegasusForConditionalGeneration.from_pretrained(model_name)
    elif "blenderbot" in model_name:
        extractive_model = Summarizer()
        abstractive_tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
        abstractive_model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    # Generate summaries for each document
    extractive_summaries = [extractive_model(document, num_sentences=10) for document in documents]

    abstractive_summaries = []
    for document in documents:
        input_ids = abstractive_tokenizer.encode("summarize: " + str(document), return_tensors="pt", max_length=512,
                                                truncation=True)
        summary_ids = abstractive_model.generate(input_ids, max_length=350, length_penalty=1.5, num_beams=7,
                                                 early_stopping=False)
        summary = abstractive_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        abstractive_summaries.append(summary)

    # Add results to the DataFrame
    model_results_df = pd.DataFrame({'Model': [model_name] * len(documents),
                                     'Title': data['title'],
                                     'CitationCount': data['citationCount'],
                                     'PublicationDate': data['publicationDate'],
                                     'Extractive_Summary': extractive_summaries,
                                     'Abstractive_Summary': abstractive_summaries})
    results_df = pd.concat([results_df, model_results_df], ignore_index=True)

# Step 6: Save results to a CSV file
#results_df.to_csv('summaries_results.csv', index=False)
#print("Summaries saved to 'summaries_results.csv'.")

# Step 5: Generate summaries for the first 2 documents
data['summary'] = data['abstract'].head(2).apply(combined_summarization)

# Step 6: Display results for the first 2 rows
print(data[['summary']].head(2))