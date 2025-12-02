#!/usr/bin/env python3
import argparse
import requests
import sys
from xml.etree import ElementTree

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def geo_esearch(keyword, retmax=100):
    """Search GEO datasets using NCBI ESearch."""
    url = f"{EUTILS}/esearch.fcgi"
    params = {
        "db": "gds",
        "term": keyword,
        "retmax": retmax,
        "retmode": "json"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error during ESearch: {e}")
        sys.exit(1)

    data = r.json()
    ids = data["esearchresult"].get("idlist", [])
    return ids


def geo_esummary(id_list):
    """Fetch metadata for GEO datasets using NCBI ESummary."""
    if not id_list:
        return []

    url = f"{EUTILS}/esummary.fcgi"
    params = {
        "db": "gds",
        "id": ",".join(id_list),
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error during ESummary: {e}")
        sys.exit(1)

    # ESummary returns XML, so parse it
    root = ElementTree.fromstring(r.content)

    results = []
    for doc in root.findall(".//DocSum"):
        record = {}
        record["id"] = doc.find("./Id").text

    for item in doc.findall("./Item"):
        name = item.attrib.get("Name")
        value = item.text

    # Handle multi-value fields (e.g., multiple taxa)
        if name in record:
        # Convert to list if not already
            if not isinstance(record[name], list):
                record[name] = [record[name]]
            record[name].append(value)
        else:
            record[name] = value

        results.append(record)

    return results


def print_results(records):
    """Pretty-print GEO dataset summaries."""
    if not records:
        print("No GEO records found.")
        return

    for rec in records:
        organism_field = rec.get("taxon") or rec.get("species") or rec.get("Organism")
        if isinstance(organism_field, list):
            organism_str = ", ".join(organism_field)
        else:
            organism_str = organism_field or "—"   
        #for multi-organism functionality 
        print("──────────────────────────────────")
        print(f"📌 Accession: {rec.get('Accession', '(unknown)')}")
        print(f"🏷  Title:     {rec.get('title', '—')}")
        print(f"📚 Type:      {rec.get('gdstype', '—')}")
        print(f"🧬 Organism(s): {organism_str}")
        print(f"🔬 Samples:   {rec.get('n_samples', '—')}")
        print(f"📝 Summary:   {rec.get('summary', '—')}")
        print("──────────────────────────────────\n")


def main():
    parser = argparse.ArgumentParser(
        description="Search NCBI GEO (Gene Expression Omnibus) datasets by keyword."
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="One or more keywords to search for (will be combined with AND)"
    )
    parser.add_argument(
        "--max",
        type=int,
        default=100,
        help="Maximum number of results to return (default=100)"
    )
    parser.add_argument(
        "--operator",
        choices=["AND", "OR"],
        default="AND",
        help="Boolean operator to combine multiple keywords (default: AND)"
    )
    args = parser.parse_args()

    # Combine multiple keywords into a single search term with AND
    search_term = " AND ".join(args.keywords)
    print(f"🔍 Searching GEO for: '{search_term}' ...\n")

    # Run the search and summary
    ids = geo_esearch(search_term, args.max)
    records = geo_esummary(ids)
    print_results(records)



if __name__ == "__main__":
    main()
