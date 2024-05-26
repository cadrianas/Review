# using the ollama outupts + pdf of the article to score them
# SIR Model Detection: Uses the mentions_SIR function to check 
# for the presence of SIR-related keywords in the article content.
# Summarization Analysis: Evaluates the summary based on relevance, 
# clarity, depth of analysis, and novelty by sending separate prompts 
# to the Ollama client.
# URL Content Analysis: Fetches the article content from the URL and 
# evaluates it for contribution to understanding disease transmission 
# dynamics and methodological limitations.
# Scoring:
# Summarization + SIR Score: Combines the summarization score and the 
# SIR score with a weight of 30% for the SIR score and 70% for the 
# summarization score.
# URL Score + SIR Score: Similar to the summarization score but applied 
# to the full article content fetched from the URL.
#Limitations: A column detailing the limitations of the methodology 
# used in the article.
#Contribution: A column detailing how the article contributes to 
# our understanding of disease transmission dynamics.

import os
import csv
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from ollama import Client

# Function to check for SIR models in the text
def mentions_SIR(text):
    keywords = ['SIR', 'SIRS', 'SIRC', 'SLIR', 'SEIR', 'SLAIR', 'compartment model']
    return any(re.search(r'\b{}\b'.format(re.escape(keyword)), text, re.IGNORECASE) for keyword in keywords)

# Function to analyze with Ollama and extract numeric score
def analyze_with_ollama(ollama_client, prompt):
    response = ollama_client.chat(
        model='llama2:13b',
        messages=[{'role': 'user', 'content': prompt}]
    )
    content = response['message']['content'].strip()
    # Extract numeric score from the response
    match = re.search(r'\b(\d{1,3})\b', content)
    if match:
        return int(match.group(1))
    else:
        raise ValueError(f"Couldn't extract a numeric score from the response: {content}")

# Function to fetch and analyze the article content from the URL
def analyze_url_content(ollama_client, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ' '.join([p.text for p in soup.find_all('p')])

        contrib_prompt = f"How does this article contribute to our understanding of disease transmission dynamics?\n\n{content}"
        contribution = ollama_client.chat(
            model='llama2:13b',
            messages=[{'role': 'user', 'content': contrib_prompt}]
        )['message']['content'].strip()

        limit_prompt = f"What are the limitations of the methodology used in this article?\n\n{content}"
        limitations = ollama_client.chat(
            model='llama2:13b',
            messages=[{'role': 'user', 'content': limit_prompt}]
        )['message']['content'].strip()

        return contribution, limitations
    except requests.RequestException as e:
        return "Error fetching URL", str(e)

def grade_articles(input_csv, output_csv):
    # Initialize Ollama client
    ollama_client = Client()

    # Load the input CSV
    data = pd.read_csv(input_csv)

    # Prepare the output CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Summary", "Content", "Summarization + SIR Score", "URL Score + SIR Score",
            "Limitations", "Contribution", "URL"
        ])

        for index, row in data.iterrows():
            summary = row['Summary']
            content = row['Content']
            url = row['URL'] if 'URL' in row else None

            # Check for SIR model usage
            sir_score = 30 if mentions_SIR(content) else 0

            # Analyze summary with Ollama
            relevance_prompt = f"Assess the relevance of the following article summary on a scale from 1 to 100:\n\n{summary}"
            relevance_score = analyze_with_ollama(ollama_client, relevance_prompt)

            clarity_prompt = f"Assess the clarity of the following article summary on a scale from 1 to 100:\n\n{summary}"
            clarity_score = analyze_with_ollama(ollama_client, clarity_prompt)

            depth_prompt = f"Assess the depth of analysis of the following article summary on a scale from 1 to 100:\n\n{summary}"
            depth_score = analyze_with_ollama(ollama_client, depth_prompt)

            novelty_prompt = f"Assess the novelty of the following article summary on a scale from 1 to 100:\n\n{summary}"
            novelty_score = analyze_with_ollama(ollama_client, novelty_prompt)

            # Calculate the summarization score as the weighted average of the individual scores
            summarization_score = (relevance_score + clarity_score + depth_score + novelty_score) / 4
            summarization_sir_score = (sir_score * 0.3) + (summarization_score * 0.7)

            # Analyze URL content if available
            if url:
                contribution, limitations = analyze_url_content(ollama_client, url)
                url_relevance_score = analyze_with_ollama(ollama_client, relevance_prompt)
                url_clarity_score = analyze_with_ollama(ollama_client, clarity_prompt)
                url_depth_score = analyze_with_ollama(ollama_client, depth_prompt)
                url_novelty_score = analyze_with_ollama(ollama_client, novelty_prompt)
                url_score = (url_relevance_score + url_clarity_score + url_depth_score + url_novelty_score) / 4
                url_sir_score = (sir_score * 0.3) + (url_score * 0.7)
            else:
                contribution = "N/A"
                limitations = "N/A"
                url_sir_score = 0

            # Write the results to the output CSV
            writer.writerow([
                summary, content, summarization_sir_score, url_sir_score, 
                limitations, contribution, url
            ])

if __name__ == "__main__":
    input_csv = "outputs/combined_output_ollama.csv"
    output_csv = "graded_outputs_ollama_V2.csv"
    grade_articles(input_csv, output_csv)


