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
        chunk = chunk[:window_size]  # Ensure chunk does not exceed window_size
        chunks.append(tokenizer.convert_tokens_to_string(chunk))
    return chunks

# Function to evaluate relevance based on keywords
def evaluate_relevance(abstract, keywords):
    tokens = abstract.lower().split()
    keyword_count = sum(1 for token in tokens if any(kw in token for kw in keywords))
    relevance_score = keyword_count / len(tokens) if tokens else 0
    return relevance_score

# Function to evaluate clarity
def evaluate_clarity(abstract):
    doc = nlp(abstract)
    sentence_lengths = [len(sent) for sent in doc.sents]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
    readability_score = textstat.flesch_reading_ease(abstract)
    clarity_score = (readability_score + avg_sentence_length) / 2
    return clarity_score

# Function to evaluate depth based on length and detail
def evaluate_depth(abstract):
    depth_score = len(abstract.split()) / 100  # Simplistic measure: words per 100 words
    return depth_score if depth_score <= 1 else 1

# Function to evaluate novelty based on unique keywords
def evaluate_novelty(abstract, common_keywords):
    tokens = set(abstract.lower().split())
    unique_keywords = tokens - set(common_keywords)
    novelty_score = len(unique_keywords) / len(tokens) if tokens else 0
    return novelty_score

# Function to evaluate model usage based on keywords
def evaluate_model_usage(abstract, model_keywords):
    tokens = abstract.lower().split()
    keyword_count = sum(1 for token in tokens if any(kw in token for kw in model_keywords))
    model_usage_score = keyword_count / len(tokens) if tokens else 0
    return model_usage_score

# Function to score articles
def score_article(abstract, questions, keywords, common_keywords, model_keywords):
    if not abstract or abstract.strip() == '':
        return None

    # Perform sentiment analysis
    sentiment_scores = []
    chunks = sliding_window(abstract, sentiment_analysis_pipeline.tokenizer, window_size=512, overlap=50)
    for chunk in chunks:
        try:
            sentiment = sentiment_analysis_pipeline(chunk[:512])  # Ensure chunk is within max length
            sentiment_scores.extend([score['label'] for score in sentiment])
        except Exception as e:
            print(f"Error processing chunk: {e}")
            continue

    positive_score = sentiment_scores.count('POSITIVE') / len(sentiment_scores) if sentiment_scores else 0

    # Evaluate each criterion
    relevance_score = evaluate_relevance(abstract, keywords)
    clarity_score = evaluate_clarity(abstract)
    depth_score = evaluate_depth(abstract)
    novelty_score = evaluate_novelty(abstract, common_keywords)
    model_usage_score = evaluate_model_usage(abstract, model_keywords)

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

keywords = ["model", "modelling", "mathematical model", "statistical model"]
common_keywords = ["study", "research", "data", "analysis"]
model_keywords = ["compartmental model", "deterministic model", "SIR", "SEIR", "SLIR", "SIRC"]

# Apply the scoring function to each abstract
df['score'] = df['abstract'].apply(lambda x: score_article(x, questions, keywords, common_keywords, model_keywords) if pd.notna(x) and x.strip() != '' else None)

# Select the required columns and create the output CSV file
output_columns = ['title', 'abstract', 'publicationDate', 'openAccessPdf_url', 'citation_bibtex', 'score']
output_df = df[output_columns]
output_csv = "sentiment_score.csv"
output_df.to_csv(output_csv, index=False)
