import pandas as pd
import re

model_patterns = [
        # 1st part indicates the model being referred to in the context of this rule
        # r'XXX\s*yyy': This regular expression pattern matches the phrase "xxx yyy" with optional whitespace between the words.
        ('Logistic Regression', r'Logistic\s*Regression'),
        ('Random Forest', r'Random\s*Forest'),
        ('Support Vector Machine', r'Support\s*Vector\s*Machine'),
        ('SIR-Type/deterministic', r'SIR'),
        ('SIR-Type/deterministic', r'SIRD'),
        ('SIR-Type/deterministic', r'SEIR'),
        ('SIR-Type/deterministic', r'SLIR'),
        ('SIR-Type/deterministic', r'deterministic\s*model'),
        ('ARIMA', r'ARIMA'),
        ('stochastic', r'stochastic'),
        ('Agent Based', r'Agent\s*Based')
        # we need more, but I cannot think of more
    ]

# Function to classify a text using rule-based method
def classify_text(text):
    for model, pattern in model_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return model
    return "Model not identified"

# Load CSV file
csv_file_path = "classified_articles_results_V1.csv"
df = pd.read_csv(csv_file_path)

# Check for NaN values in 'title' and 'abstract' columns and replace them with empty strings
df['title'] = df['title'].fillna('')
df['abstract'] = df['abstract'].fillna('')

# Apply classification to each row
df['Model_abstract'] = df.apply(lambda row: classify_text(row['title'] + ' ' + row['abstract']), axis=1)

# Save the modified DataFrame to a new CSV file
output_csv_file_path = "classified_articles_results_V1.csv"
df.to_csv(output_csv_file_path, index=False)

print("Classification done and saved to", output_csv_file_path)