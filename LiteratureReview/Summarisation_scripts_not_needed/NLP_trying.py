import requests
from PyPDF2 import PdfReader
from transformers import T5Tokenizer, T5ForConditionalGeneration
from summarizer import Summarizer  # Add import for the extractive summarizer
import pandas as pd  # Add import for pandas

# Step 1: Load pre-trained models and tokenizers
model_name = "t5-large"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load the extractive summarizer model
extractive_model = Summarizer()

# Step 2: Abstractive Summarization function
def combined_summarization(document, top_n=20):
    # Handle NaN values
    if pd.isna(document):
        return "No content to summarize."

    # Convert abstract to string
    document = str(document)

    # Extractive summarization
   # extractive_summary = extractive_model(document, num_sentences=top_n)

    # Abstractive summarization based on the top N sentences from extractive summary
    #input_ids = tokenizer.encode("summarize: " + extractive_summary, return_tensors="pt", max_length=512, truncation=True)
    input_ids = tokenizer.encode("summarize: " +document, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(input_ids, max_length=512, length_penalty=1.5, num_beams=7, early_stopping=False)
    abstractive_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return abstractive_summary

# Step 3: Apply summarization to the provided abstract
provided_abstract = """
The study by Cooper et al. \cite{cooper2020sir} introduced a novel susceptible-infected-removed (SIR) model, where the susceptible population is treated as a dynamic variable rather than a fixed parameter. This adaptation allows for adjustments in the susceptible population over time to accommodate the influx of newly infected individuals within a community. Utilising data spanning from January to June 2020, the researchers made predictions concerning various parameters related to COVID-19 transmission dynamics, including projections for susceptible, infected, and removed populations up to September 2020. Through a comparative analysis of observed data and model-derived outcomes, the study concludes that effective control measures, implemented early and rigorously, can potentially mitigate the spread of COVID-19 across diverse communities."""

summary_result = combined_summarization(provided_abstract)

# Step 4: Display the original abstract and the generated summary
print("Original Abstract:")
print(provided_abstract)
print("\nGenerated Summary:")
print(summary_result)
