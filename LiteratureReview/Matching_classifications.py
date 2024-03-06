import os
import pandas as pd

# Read the CSV file
df = pd.read_csv('classified_articles_results_V1.csv')

# Assuming df is your DataFrame containing the columns Model, Model_abstract, and Model_classification

def determine_final_model(row):
    if row['Model'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'} and row['Model_abstract'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'} and row['Model'] == row['Model_abstract']:
        return row['Model']
    elif row['Model'] in {'PDF cannot be read', 'URL does not exist', 'Error processing PDF'} and row['Model_abstract'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'}:
        return row['Model_abstract']
    elif row['Model'] in {'PDF cannot be read', 'URL does not exist', 'Error processing PDF'} and row['Model_abstract'] == 'Model not identified':
        return 'read the paper'
    elif row['Model'] == 'Model not identified' and row['Model_abstract'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'}:
        return row['Model_abstract']
    elif row['Model'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'} and row['Model_abstract'] == 'Model not identified':
        return row['Model']
    elif row['Model'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'} and row['Model_abstract'] in {'Logistic Regression', 'Random Forest', 'Support Vector Machine', 'SIR-Type/deterministic', 'ARIMA', 'stochastic', 'Agent Based'} and row['Model'] != row['Model_abstract']:
        return 'read the paper'
    else:
        return 'No rule matched'

# Apply the function to create the Model_final column
df['Model_final'] = df.apply(determine_final_model, axis=1)

# Filter rows where Model_final is 'read the paper'
not_matching_df = df[df['Model_final'] == 'read the paper']

# Save the DataFrames to new CSV file
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

not_matching_df.to_csv(os.path.join(output_folder, 'classification_not_matching.csv'), index=False)
df.to_csv(os.path.join(output_folder, 'classification_results.csv'), index=False)