import requests
import json

query = "(HPV prevalence) | (HPV female prevalence)"
fields = "title,abstract,publicationDate,citationCount,authors,openAccessPdf"
#fields_of_study = "Mathematics"

url = f"http://api.semanticscholar.org/graph/v1/paper/search/bulk?query={query}&fields={fields}"
r = requests.get(url).json()

print(f"Will retrieve an estimated {r['total']} documents")
retrieved = 0

with open(f"papers_HPV_V2.jsonl", "a") as file:
    while True:
        if "data" in r:
            retrieved += len(r["data"])
            print(f"Retrieved {retrieved} papers...")
            for paper in r["data"]:
                print(json.dumps(paper), file=file)
        if "token" not in r:
            break
        r = requests.get(f"{url}&token={r['token']}").json()

print(f"Done! Retrieved {retrieved} papers total")
