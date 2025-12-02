# GEO Search Tool  
A command-line tool for searching NCBI GEO (Gene Expression Omnibus) datasets by keyword.

---

## Overview

**GEO Search Tool** is a Python-based CLI program that lets you search the  
**NCBI Gene Expression Omnibus (GEO)** for datasets using keywords.  
It uses the NCBI **ESearch** and **ESummary** E-utilities to:

- Search GEO dataset metadata
- Retrieve detailed information (title, summary, dataset type)
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

### **Local installation**
```bash
pip install .

---

## Usage & Example
## Basic Search
geo-search "breast cancer"
## Limiting results number
geo-search "diabetes" --max 20
## Output
🔍 Searching GEO for: 'breast cancer' ...

──────────────────────────────────
📌 Accession:  GSE12345
🏷  Title:      Expression profiling in breast cancer
📚 Type:       GSE
🧬 Organism(s): Homo sapiens
🔬 Samples:    48
📝 Summary:    Gene expression analysis of primary tumors...
──────────────────────────────────

──────────────────────────────────
📌 Accession:  GSE99821
🏷  Title:      Cross-species tumor profiling
📚 Type:       GSE
🧬 Organism(s): Homo sapiens, Mus musculus
🔬 Samples:    32
📝 Summary:    Comparative profiling in human–mouse xenografts...
──────────────────────────────────

