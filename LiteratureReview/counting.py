import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to count occurrences of each entry in a column
def count_entries_in_column(csv_file, column_name):
    entry_counts = {}

    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            entry = row[column_name]
            if entry in entry_counts:
                entry_counts[entry] += 1
            else:
                entry_counts[entry] = 1

    return entry_counts

# Example usage:
csv_file_path = "outputs/classification_results.csv"
column_name_to_count = "Model_final"  # Name of the column you want to count entries in

entry_counts = count_entries_in_column(csv_file_path, column_name_to_count)

# Calculate percentages
total_entries = sum(entry_counts.values())
percentages = {entry: (count / total_entries) * 100 for entry, count in entry_counts.items()}

# Create output folder if it doesn't exist
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(entry_counts.values(), labels=entry_counts.keys(), autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Models')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'pie_chart.png'))
plt.show()

# Bar Chart
plt.figure(figsize=(12, 6))
plt.barh(list(entry_counts.keys()), entry_counts.values(), color='skyblue', edgecolor='black')
plt.title('Counts of Models', fontsize=16)
plt.xlabel('Count', fontsize=14)
plt.ylabel('Model', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'bar_chart_counts.png'))
plt.show()

# Bar Chart with percentages
plt.figure(figsize=(12, 6))
plt.barh(list(percentages.keys()), percentages.values(), color='skyblue', edgecolor='black')
plt.title('Percentage Distribution of Models', fontsize=16)
plt.xlabel('Percentage', fontsize=14)
plt.ylabel('Model', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Display percentages on bars
for index, value in enumerate(percentages.values()):
    plt.text(value, index, f'{value:.1f}%', va='center')

plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'bar_chart_percentages.png'))
plt.show()

# Pie Chart
plt.figure(figsize=(15, 6))
plt.subplot(1, 3, 1)
plt.pie(entry_counts.values(), labels=entry_counts.keys(), autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Models')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

# Bar Chart
plt.subplot(1, 3, 2)
plt.barh(list(entry_counts.keys()), entry_counts.values(), color='skyblue', edgecolor='black')
plt.title('Counts of Models', fontsize=16)
plt.xlabel('Count', fontsize=14)
plt.ylabel('Model', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Bar Chart with percentages
plt.subplot(1, 3, 3)
plt.barh(list(percentages.keys()), percentages.values(), color='skyblue', edgecolor='black')
plt.title('Percentage Distribution of Models', fontsize=16)
plt.xlabel('Percentage', fontsize=14)
plt.ylabel('Model', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Display percentages on bars
for index, value in enumerate(percentages.values()):
    plt.text(value, index, f'{value:.1f}%', va='center')

plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'combined_charts.png'))
plt.show()