# GEO Dataset Search Tool  
A command-line tool for searching NCBI GEO (Gene Expression Omnibus) datasets by keyword.

---

## Overview

**GEO Search Tool** is a Python-based program that lets you search the  
**NCBI Gene Expression Omnibus (GEO)** for datasets using desired keywords.  
It uses the NCBI **ESearch** and **ESummary** E-utilities to:

- Search GEO dataset metadata
- Retrieve detailed & relevant information (title, summary, dataset type)
- Correctly handle **multi-species** datasets
- Display results in a clean, readable terminal format

---

## Features

- 🔎 Search GEO by keyword  
- 📚 Supports GSE, GSM, and GPL datasets  
- 🧬 Multi-species organism detection  
- 📝 Clean, formatted terminal output  
- ⚙️ Adjustable result limits (`--max`)  
- 💡 Installable as a `geo-search` command  

---

##  Installation

## Clone the Repository

```bash
git clone https://github.com/jordynn20/geo-search
cd geo_search
```


---

## Usage & Example
## Basic Search
geo-search "breast cancer"

## Optional Parameters

--db → Choose database (default: gds)

Examples: --db sra, --db pubmed

--max → Maximum number of results

Default: 100

--operator → Boolean operator for multiple keywords (AND or OR)

Default: AND

## Output
🔍 Searching GEO for: 'breast cancer' ...


📌 Accession:  GSE12345

🏷  Title:      Expression profiling in breast cancer

📚 Type:       GSE

🧬 Organism(s): Homo sapiens

🔬 Samples:    48

📝 Summary:    Gene expression analysis of primary tumors...



