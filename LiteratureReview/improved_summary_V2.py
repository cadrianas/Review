import os
import pandas as pd
import spacy
from nltk import ne_chunk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
# Load the CSV file into a DataFrame
df = pd.read_csv("outputs/SIR_type.csv")

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")


# Function to extract entities using SpaCy
def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities


# Function to extract named entities using NLTK
def extract_named_entities(text):
    sentences = sent_tokenize(text)
    named_entities = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        chunked = ne_chunk(tagged_words)
        for subtree in chunked:
            if isinstance(subtree, nltk.Tree):
                entity = " ".join([word for word, tag in subtree.leaves()])
                named_entities.append(entity)
    return named_entities


# Function to extract keyphrases using TF-IDF
def extract_keyphrases(text):
    # Tokenize text into words
    words = text.split()

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=10)  # Extract top 10 keyphrases

    # Fit vectorizer to the text and transform it to obtain TF-IDF weights
    tfidf_matrix = vectorizer.fit_transform([text])

    # Get feature names (keyphrases) from the vectorizer
    feature_names = vectorizer.get_feature_names_out()

    # Sort feature names by TF-IDF weights and return top keyphrases
    sorted_indices = tfidf_matrix.toarray()[0].argsort()[::-1]
    keyphrases = [feature_names[idx] for idx in sorted_indices[:10]]

    return keyphrases


# Function to improve coherence of summary
def improve_coherence(row):
    abstract = row['abstract']
    pegasus_summary = row['summary_Pegasus-XSUM']
    t5_large_summary = row['summary_T5-Small']
    t5_small_summary = row['summary_T5-Large']
    t5_base_summary = row['summary_T5-Base']

    # Check if abstract is empty
    if pd.isna(abstract) or abstract.strip() == '':
        return "No abstract provided."

    # Combine all summaries into a single text
    summaries = [summary for summary in [pegasus_summary, t5_large_summary, t5_small_summary, t5_base_summary] if
                 not pd.isna(summary) and summary.strip() != "No content to summarize"]
    combined_summary = ' '.join(summaries)

    # Extract entities, named entities, and keyphrases from the abstract
    entities = extract_entities(abstract)
    named_entities = extract_named_entities(abstract)
    keyphrases = extract_keyphrases(abstract)

    # Construct improved summary by combining original summaries with extracted entities, named entities, and keyphrases
    improved_summary = combined_summary + ' '.join(entities) + ' '.join(named_entities) + ' '.join(keyphrases)

    return improved_summary


# Apply the function to each row in the DataFrame
df['improved_summary_V2'] = df.apply(improve_coherence, axis=1)

# Save the processed DataFrame back to a CSV file
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_csv = os.path.join(output_folder, 'SIR_type_improved.csv')
df.to_csv(output_csv, index=False)
