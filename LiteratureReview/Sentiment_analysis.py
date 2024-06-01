# there are several transformer models that support more than 512 tokens.
# Some notable ones include Longformer, BigBird, and LED (Longformer Encoder-Decoder).
# These models are specifically designed to handle longer sequences.
#
# Longformer model for both sentiment analysis
# and question answering, as it supports longer sequences. The maximum token length for
# Longformer can be up to 4096 tokens, which should be sufficient for most abstracts.


import pandas as pd
from transformers import LongformerTokenizer, LongformerForSequenceClassification, LongformerForQuestionAnswering, \
    pipeline
import torch

# Load Longformer tokenizer and models
tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")
sentiment_model = LongformerForSequenceClassification.from_pretrained("allenai/longformer-base-4096")
qa_model = LongformerForQuestionAnswering.from_pretrained("allenai/longformer-base-4096")

# Sentiment analysis pipeline using Longformer
sentiment_analysis_pipeline = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=tokenizer)

# Question answering pipeline using Longformer
question_answering_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)


# Function to score an article based on its abstract
def score_article(abstract):
    if not abstract or pd.isna(abstract):
        return None

    # Convert abstract to string
    abstract = str(abstract)

    # Tokenize the abstract using Longformer
    inputs = tokenizer(abstract, return_tensors="pt", truncation=True, max_length=4096)

    # Analyze sentiment (optional)
    sentiment = sentiment_analysis_pipeline(abstract)[0]['label']

    # Ask questions to extract specific information
    questions = [
        "How relevant is the content to the main topic?",
        "How clear is the writing and presentation?",
        "How deep is the analysis provided?",
        "How novel are the insights or findings?",
        "How effectively is a compartmental mathematical model used?"
    ]
    answers = [question_answering_pipeline(question=q, context=abstract)['answer'] for q in questions]

    # Convert answers to scores (assuming answers are on a scale of 1 to 10)
    try:
        relevance_score = float(answers[0])
        clarity_score = float(answers[1])
        depth_score = float(answers[2])
        novelty_score = float(answers[3])
        model_usage_score = float(answers[4])
    except ValueError:
        # If the answers are not directly convertible to float, set them to a default score (e.g., 5)
        relevance_score = clarity_score = depth_score = novelty_score = model_usage_score = 5.0

    # Weight each criterion based on importance
    weights = {
        "relevance": 2,
        "clarity": 2,
        "depth": 2,
        "novelty": 2,
        "model_usage": 2
    }

    # Calculate overall score
    overall_score = (relevance_score * weights["relevance"] +
                     clarity_score * weights["clarity"] +
                     depth_score * weights["depth"] +
                     novelty_score * weights["novelty"] +
                     model_usage_score * weights["model_usage"]) / sum(weights.values())

    return overall_score


# Load the CSV with the abstracts
input_csv = 'papers_V4.csv'
df = pd.read_csv(input_csv, low_memory=False)

# Convert the 'abstract' column to strings
df['abstract'] = df['abstract'].astype(str)

# Score each article based on the abstract, skipping rows without abstracts
df['score'] = df['abstract'].apply(lambda x: score_article(x) if pd.notna(x) and x.strip() != '' else None)

# Select the desired columns
output_df = df[['title', 'abstract', 'publicationDate', 'openAccessPdf_url', 'citation_bibtex', 'score']]

# Save the result to a new CSV file
output_csv = 'sentiment_score.csv'
output_df.to_csv(output_csv, index=False)

print(f"Sentiment scores have been saved to {output_csv}")
