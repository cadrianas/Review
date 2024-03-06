
# his Python script defines a function called merge_csv that merges two CSV files into one,
# by appending the rows of the second CSV file to the end of the first CSV file
import csv


def merge_csv(csv1_path, csv2_path, output_csv_path):
    # Read CSV 1 and write to output CSV
    with open(csv1_path, 'r', newline='', encoding='utf-8') as csv1_file, \
            open(output_csv_path, 'w', newline='', encoding='utf-8') as output_csv_file:
        csv_writer = csv.writer(output_csv_file)

        # Read rows from CSV 1 and write to output CSV
        csv_reader = csv.reader(csv1_file)
        for row in csv_reader:
            csv_writer.writerow(row)

    # Read CSV 2 and append rows to output CSV
    with open(csv2_path, 'r', newline='', encoding='utf-8') as csv2_file, \
            open(output_csv_path, 'a', newline='', encoding='utf-8') as output_csv_file:
        csv_writer = csv.writer(output_csv_file)

        # Skip the header row in CSV 2
        next(csv2_file)

        # Read rows from CSV 2 and append to output CSV
        csv_reader = csv.reader(csv2_file)
        for row in csv_reader:
            csv_writer.writerow(row)
# Example usage:
csv1_path = "processed_papers_V3_result.csv"
csv2_path = "processed_papers_V3_result_P2.csv"
output_csv_path = "classified_articles_results.csv"
merge_csv(csv1_path, csv2_path, output_csv_path)
