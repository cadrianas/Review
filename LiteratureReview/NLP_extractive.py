# extractive text summarization using the Gensim library
import nltk
nltk.download()
import pandas as pd
from gensim.summarization import summarize
#Load the data
data = pd.read_csv('output_V2.csv')
# Preprocess the data. Ensure that the abstracts are not empty and handle any missing values:
data = data.dropna(subset=['abstract'])
# Summarize using Gensim
# Create an empty column for summaries
data['summary'] = ""

# Iterate through each row and generate a summary
for index, row in data.iterrows():
    abstract = row['abstract']

    # Check if the abstract is not empty
    if abstract:
        # Summarize the abstract using Gensim's summarize function
        summary = summarize(abstract, ratio=0.2)  # Adjust the ratio for the length of the summary

        # Store the summary in the 'summary' column
        data.at[index, 'summary'] = summary

# Display the results
print(data[['title', 'citation_number', 'publication_date', 'summary']])




