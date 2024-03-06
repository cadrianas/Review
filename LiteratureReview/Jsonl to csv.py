import json
import csv


with open('papers_v3.jsonl') as f:
    data = [json.loads(line) for line in f]

# Extract keys for CSV header
header = data[0].keys()

# Write to CSV
with open('papers_v3.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)





