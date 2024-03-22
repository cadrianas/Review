import pandas as pd
from transformers import BartTokenizer, BartForConditionalGeneration, PegasusTokenizer, PegasusForConditionalGeneration
import argparse

def bart_summarization(document, bart_tokenizer, bart_model):
    if pd.isna(document):
        return "No content to summarize."

    inputs = bart_tokenizer(document, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = bart_model.generate(inputs['input_ids'], max_length=150, min_length=40, length_penalty=2.0,
                                      num_beams=4, early_stopping=True)
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary


def pegasus_summarization(document, pegasus_tokenizer, pegasus_model):
    if pd.isna(document):
        return "No content to summarize."

    inputs = pegasus_tokenizer(document, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
    summary_ids = pegasus_model.generate(inputs['input_ids'], max_length=100, min_length=50, length_penalty=2.0,
                                         num_beams=4, early_stopping=True)
    summary = pegasus_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def main(args):
    # Load data
    data = pd.read_csv(args.input_csv)

    # Load Pegasus tokenizer and model for summarization
    pegasus_tokenizer = PegasusTokenizer.from_pretrained(args.pegasus_model)
    pegasus_model = PegasusForConditionalGeneration.from_pretrained(args.pegasus_model)

    # Load BART tokenizer and model for summarization
    bart_tokenizer = BartTokenizer.from_pretrained(args.bart_model)
    bart_model = BartForConditionalGeneration.from_pretrained(args.bart_model)

    # Generate summaries for each document using BERT
    data['summary_BART'] = data['abstract'].apply(lambda x: bart_summarization(x, bart_tokenizer, bart_model))

    # Generate summaries for each document using Pegasus
    data['summary_Pegasus'] = data['abstract'].apply(lambda x: pegasus_summarization(x, pegasus_tokenizer, pegasus_model))

    # Save the results in a single CSV file
    data.to_csv(args.output_csv, index=False)
    print(f"Summaries saved to '{args.output_csv}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate summaries for documents using BART and Pegasus models.")
    parser.add_argument("input_csv", type=str, help="Path to the input CSV file containing document data.")
    parser.add_argument("output_csv", type=str, help="Path to save the output CSV file with summaries.")
    parser.add_argument("--bart_model", type=str, default='facebook/bart-large-cnn', help="Pretrained BART model name or path.")
    parser.add_argument("--pegasus_model", type=str, default='google/pegasus-xsum', help="Pretrained Pegasus model name or path.")
    args = parser.parse_args()

    main(args)
