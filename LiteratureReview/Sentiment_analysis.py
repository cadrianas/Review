import pandas as pd
from transformers import pipeline
import spacy
import textstat

# Load the sentiment analysis pipeline
sentiment_analysis_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Example questions for extracting specific information
questions = [
    "How relevant is the content to the main topic?",
    "How clear is the writing and presentation?",
    "How deep is the analysis provided?",
    "How novel are the insights or findings?",
    "How effectively is a compartmental mathematical model used?"
]

# Sliding window function for long texts
def sliding_window(text, tokenizer, window_size, overlap):
    tokens = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokens), window_size - overlap):
        chunk = tokens[i:i + window_size]
        if len(chunk) > window_size:
            chunk = chunk[:window_size]
        chunks.append(tokenizer.convert_tokens_to_string(chunk))
    return chunks

# Function to evaluate relevance based on keywords
def evaluate_relevance(abstract, keywords):
    tokens = abstract.split()
    keyword_count = sum(1 for token in tokens if token.lower() in keywords)
    relevance_score = keyword_count / len(tokens)
    return relevance_score

# Function to evaluate clarity
def evaluate_clarity(abstract):
    doc = nlp(abstract)
    sentence_lengths = [len(sent) for sent in doc.sents]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

    readability_score = textstat.flesch_reading_ease(abstract)
    clarity_score = (readability_score + avg_sentence_length) / 2
    return clarity_score

# Function to score articles
def score_article(abstract, questions):
    if not abstract or abstract.strip() == '':
        return None

    # Perform sentiment analysis
    sentiment_scores = []
    chunks = sliding_window(abstract, sentiment_analysis_pipeline.tokenizer, window_size=512, overlap=50)
    for chunk in chunks:
        sentiment = sentiment_analysis_pipeline(chunk[:512])
        sentiment_scores.extend([score['label'] for score in sentiment])

    positive_score = sentiment_scores.count('POSITIVE') / len(sentiment_scores) if sentiment_scores else 0

    # Evaluate each criterion
    relevance_score = evaluate_relevance(abstract, keywords)
    clarity_score = evaluate_clarity(abstract)
    depth_score = 0.5  # Placeholder
    novelty_score = 0.5  # Placeholder
    model_usage_score = 0.5  # Placeholder

    # Weight each criterion based on importance
    weights = {
        "relevance": 2,
        "clarity": 2,
        "depth": 2,
        "novelty": 2,
        "model_usage": 2
    }

    overall_score = (relevance_score * weights["relevance"] +
                     clarity_score * weights["clarity"] +
                     depth_score * weights["depth"] +
                     novelty_score * weights["novelty"] +
                     model_usage_score * weights["model_usage"]) / sum(weights.values())

    return overall_score

# Load your CSV file
input_csv = "papers_V4.csv"
df = pd.read_csv(input_csv, low_memory=False)

keywords = ["coronavirus", "COVID-19", "SIR", "SEIR", "SLIR", "compartmental model", "deterministic model", "SIRC"]

# Apply the scoring function to each abstract
df['score'] = df['abstract'].apply(lambda x: score_article(x, questions) if pd.notna(x) and x.strip() != '' else None)

# Select the required columns and create the output CSV file
output_columns = ['title', 'abstract', 'publicationDate', 'openAccessPdf_url', 'citation_bibtex', 'score']
output_df = df[output_columns]
output_csv = "sentiment_score.csv"
output_df.to_csv(output_csv, index=False)
