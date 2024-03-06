import requests
import json

query = "(covid 19 metapupulation)| (sars cov 2 metapopulation) | (covid 19 modeling) | (covid 19 modelling) | (covid 19 bayesian inference) | (sars cov 2 modeling) | (sars cov 2 modelling) | (sars cov 2 bayesian inference) | (covid 19 case infection) | (sars cov 2 case infection) | (covid 19 mathematical modeling) | (sars cov 2 matheamtical modeling) | (sars cov 2 variance of concern) | (covid 19 variance of concern)"
fields = "title,abstract,publicationDate,publicationTypes,journal,publicationVenue,authors,openAccessPdf,citationStyles"
fields_of_study = "Mathematics"

url = f"http://api.semanticscholar.org/graph/v1/paper/search/bulk?query={query}&fields={fields}&fieldsOfStudy={fields_of_study}"
r = requests.get(url).json()

##print(f"Will retrieve an estimated {r['total']} documents")
retrieved = 0

with open(f"papers_V4.jsonl", "a") as file:
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

