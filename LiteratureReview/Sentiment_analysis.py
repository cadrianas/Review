import pandas as pd
from transformers import pipeline

# Initialize the sentiment analysis and question answering pipelines
sentiment_analysis_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
question_answering_pipeline = pipeline("question-answering", model="allenai/longformer-base-4096")

# Questions for extracting specific information
questions = [
    "How relevant is the content to the main topic?",
    "How clear is the writing and presentation?",
    "How deep is the analysis provided?",
    "How novel are the insights or findings?",
    "How effectively is a compartmental mathematical model used?"
]

# Sliding window function for long texts
def sliding_window(text, window_size=4096, overlap=512):
    tokens = text.split()
    for start in range(0, len(tokens), window_size - overlap):
        yield ' '.join(tokens[start:start + window_size])

# Function to score each article
def score_article(abstract):
    if not abstract or abstract.strip() == '':
        return None
    
    # Perform sentiment analysis
    sentiment_scores = []
    for chunk in sliding_window(abstract):
        sentiment = sentiment_analysis_pipeline(chunk)
        sentiment_scores.extend([score['label'] for score in sentiment])
    
    # Assuming sentiment labels are 'POSITIVE' and 'NEGATIVE'
    positive_score = sentiment_scores.count('POSITIVE') / len(sentiment_scores) if sentiment_scores else 0

    # Perform question answering
    answers = []
    for chunk in sliding_window(abstract):
        for question in questions:
            answer = question_answering_pipeline(question=question, context=chunk)['answer']
            try:
                answers.append(float(answer))
            except ValueError:
                answers.append(0)

    # Calculate the final score
    if answers:
        relevance_score = sum(answers[0::5]) / len(answers[0::5])
        clarity_score = sum(answers[1::5]) / len(answers[1::5])
        depth_score = sum(answers[2::5]) / len(answers[2::5])
        novelty_score = sum(answers[3::5]) / len(answers[3::5])
        model_usage_score = sum(answers[4::5]) / len(answers[4::5])

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
    else:
        overall_score = 0

    return overall_score

# Load your CSV file
input_csv = "papers_V4.csv"
df = pd.read_csv(input_csv)

# Apply the scoring function to each abstract
df['score'] = df['abstract'].apply(lambda x: score_article(x) if pd.notna(x) and x.strip() != '' else None)

# Select the required columns and create the output CSV file
output_columns = ['title', 'abstract', 'publicationDate', 'openAccessPdf_url', 'citation_bibtex', 'score']
output_df = df[output_columns]
output_csv = "sentiment_score.csv"
output_df.to_csv(output_csv, index=False)
