
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Read the CSV file into a Pandas DataFrame
df = pd.read_csv('processed_papers_V3.csv')

# Step 2: Convert the 'date of publication' column to datetime format
df['publicationDate'] = pd.to_datetime(df['publicationDate'])

# Step 3: Extract the month and year from the publication dates
df['year_month'] = df['publicationDate'].dt.to_period('M')

# Step 4: Identify articles published before December 2019
before_dec_2019 = df['publicationDate'] < pd.Timestamp('2019-12-01')

# Step 5: Replace the Period objects with NaN for articles published before December 2019
df.loc[before_dec_2019, 'year_month'] = np.nan

# Step 6: Fill NaN values with 'Unknown' and convert 'year_month' column to strings
df['year_month'] = df['year_month'].fillna('Unknown').astype(str)

# Step 7: Count the frequency of publications for each month
monthly_frequency = df['year_month'].value_counts().sort_index()

# Remove the "Unknown" category from the data
monthly_frequency = monthly_frequency.drop('Unknown', errors='ignore')

# Step 8: Plot the data using Matplotlib
plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(monthly_frequency)), monthly_frequency, color='skyblue')

# Customizing x-axis ticks
plt.title('Monthly Frequency of Publications')
plt.xlabel('Year-Month')
plt.ylabel('Frequency')

# Handling x-tick labels
plt.xticks(range(len(monthly_frequency)), monthly_frequency.index, rotation=45)

# Adding counts on top of the bars (excluding the "Unknown" category)
#for bar in bars:
#    yval = bar.get_height()
#    plt.text(bar.get_x() + bar.get_width()/2, yval + 20, yval, ha='center', va='bottom')

# Annotating the number of unknown publications elsewhere on the figure
unknown_count = df['year_month'].value_counts().get('Unknown', 0)
plt.text(len(monthly_frequency)/2, max(monthly_frequency) + 50, f'Unknown: {unknown_count}', ha='center')

plt.tight_layout()

# Step 9: Save the figure in the "outputs" folder
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
plt.savefig(os.path.join(output_folder, 'monthly_frequency.pdf'))

plt.show()


