import json

import dic
import pandas as pd
import csv
import ast

with open('papers_V2.jsonl') as f:
    data = [json.loads(line) for line in f]

dict_paperID =[]

for item in data:
    print(item['abstract'])
    dict_paperID.append(item['abstract'])



#with open('paperID.csv', 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow(["Paper ID"])
#    for val in dict_paperID:
#        writer.writerow([val])

#with open('Abstract.csv', 'w', newline='') as file:
#   writer = csv.writer(file)
#    writer.writerow(["abstract"])
#    for val in dict_paperID:
#        writer.writerow([val])






