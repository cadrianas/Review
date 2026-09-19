# Computational analysis of the COVID-19 modelling literature

Research code and a working literature review developed from a PhD thesis project on computational approaches to the COVID-19 modelling literature.

The project explores how programmatic literature retrieval, rule-based classification, and local language-model summarisation can support a literature review. The manuscript discusses selected studies of transmission, interventions, vaccination, variants, statistical surveillance, and forecasting.

**Read the review:** [PDF](LiteratureReview/output/pdf/covid19_modelling_review.pdf) · [Editable Markdown](LiteratureReview/preprint/manuscript.md)

## Scope and status

The current manuscript is a selective narrative review with 28 references spanning 2020 to early 2024. The wider collection was retrieved from Semantic Scholar in approximately August 2024. It is not a systematic review or an exhaustive survey of the field.

Ollama was used for the final summarisation approach. BART, Pegasus, and T5 were preliminary experiments. Automated classifications and summaries are research aids and require checking against the original papers.

This repository contains research scripts developed iteratively, not a packaged application or a validated end-to-end pipeline. Several scripts use fixed filenames, expect intermediate files, or run processing immediately when executed. The manuscript remains a working draft and has not been independently peer reviewed as part of this repository.

## Repository guide

| Location | Contents |
| --- | --- |
| `LiteratureReview/preprint/manuscript.md` | Main editable manuscript, including references and methods |
| `LiteratureReview/output/pdf/covid19_modelling_review.pdf` | Rendered review |
| `LiteratureReview/get_papers.py`, `search_papers.py` | Historical Semantic Scholar retrieval scripts |
| `LiteratureReview/Converting_Semantic_to_csv.py` | JSONL-to-CSV metadata conversion |
| `LiteratureReview/classification.py`, `abstract_classification.py` | Keyword rules applied to PDF text or titles and abstracts |
| `LiteratureReview/Matching_classifications.py` | Reconciliation of the two classification outputs |
| `LiteratureReview/Olama_using_csv.py` | Ollama summarisation of abstracts with bibliographic entries |
| `LiteratureReview/Ollama_summary_using_txt.py` | Ollama summarisation of extracted article text |
| `LiteratureReview/Summarisation_scripts_not_needed/` | Earlier summarisation experiments retained for context |
| `LiteratureReview/Scoring/` | Experimental scoring code; generated outputs are excluded |
| Other Python and R scripts | Data preparation, downloads, plotting, and exploratory processing |

The retained Ollama scripts contain different configurations: the CSV summariser specifies `llama2:13b`, while the text summariser specifies `llama3`. These settings document the implementations present here; they should not be interpreted as a complete log of all historical runs.

## Documented workflow

1. **Retrieve records.** Query Semantic Scholar with COVID-19/SARS-CoV-2 and modelling-related terms, using a Mathematics field-of-study filter and pagination.
2. **Prepare metadata.** Convert JSONL records into tabular data and extract bibliographic fields and available PDF links.
3. **Organise papers.** Apply keyword rules to titles, abstracts, and accessible PDF text. Flag disagreements for inspection.
4. **Generate summaries.** Use Ollama to assist reading and synthesis, with original-paper checks for claims used in the review.
5. **Write the synthesis.** Select papers relevant to the review's questions and compare their assumptions, data, and interpretation.

The saved scripts preserve aspects of the original workflow but do not establish an exact search date, a complete screening history, or identical processing for every record. Keyword classification returns the first matching category and can miss multiple methods within one paper. PDF availability and text extraction also affect coverage. The historical queries contain spelling errors and should be reviewed before reuse.

## Working with the scripts

Use Python 3 and a separate virtual environment. Dependencies vary by script; there is no validated, pinned environment for the complete historical workflow.

For example, the CSV-based Ollama script imports `ollama` and `httpx`. It expects a running Ollama service, the model named in the script, and a CSV with `citation_bibtex` and `abstract` columns:

```sh
cd LiteratureReview
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ollama httpx
mkdir -p outputs
python Olama_using_csv.py path/to/input.csv outputs/ollama_summaries.csv
```

The input dataset is not distributed in this public source package. Supply records you are permitted to process. Model installation and downloads are separate from the Python package installation; inspect the configured model and prompt before running.

Metadata conversion can be run separately with `pandas` installed:

```sh
python Converting_Semantic_to_csv.py path/to/records.jsonl path/to/records.csv
```

Other scripts use additional packages, including PDF extraction, plotting, and earlier summarisation libraries. Inspect their imports and input filenames before execution. These examples describe script interfaces; they are not a claim that the original collection can be reproduced exactly.

## Rebuilding the manuscript

Edit `LiteratureReview/preprint/manuscript.md`. With Pandoc and a LaTeX distribution installed, run from the repository root:

```sh
bash LiteratureReview/build_review.sh
```

The build generates LaTeX and the PDF from the Markdown. Generated LaTeX and auxiliary files are ignored; the selected review PDF is retained for readers. LaTeX can be regenerated for a preprint submission.

## Data and third-party material

The public source package excludes downloaded journal PDFs, extracted article full text, bulk API exports, generated summaries, classification tables, and intermediate datasets. Publication links remain in the manuscript references. Downloaded material should only be redistributed when its terms permit it; this project does not grant rights to third-party articles or metadata.

The ignore rules also exclude local environments, editor settings, caches, credentials, and build intermediates. Ignore rules do not remove files already committed or their historical versions. A public release should therefore use a reviewed clean export or a separately reviewed history cleanup.

## Citation and reuse

Until a stable preprint identifier is available, cite the manuscript title and link to the repository, identifying the commit or release consulted. No software or manuscript reuse licence has yet been selected. Public availability alone does not supply a reuse licence; third-party material retains its own terms.
