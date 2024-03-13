import os

import pandas as pd

# Load the original CSV
original_df = pd.read_csv("classification_results_bibtex.csv")

# Subset the dataframe based on the condition
subset_df = original_df[original_df['Model_final'].str.contains('SIR-Type/deterministic')]

output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save the subset dataframe to a new CSV
output_csv = os.path.join(output_folder,'SIR_type_bibtex.csv')
subset_df.to_csv(output_csv, index=False)

