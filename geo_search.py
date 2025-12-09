#!/usr/bin/env python3
import argparse
import requests
import sys
from xml.etree import ElementTree

LINK = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def geo_esearch(keyword, db="gds", retmax=100):
    """Search datasets using NCBI ESearch."""
    url = f"{LINK}/esearch.fcgi"
    params = {
        "db": db,
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


def geo_esummary(id_list, db="gds"):
    """Fetch metadata using NCBI ESummary."""
    if not id_list:
        return []

    url = f"{LINK}/esummary.fcgi"
    params = {
        "db": db,
        "id": ",".join(id_list),
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error during ESummary: {e}")
        sys.exit(1)

    root = ElementTree.fromstring(r.content)
    results = []

    for doc in root.findall(".//DocSum"):
        record = {}
        record["id"] = doc.find("./Id").text

        for item in doc.findall("./Item"):
            name = item.attrib.get("Name")
            value = item.text

            # Handle multi-value fields
            if name in record:
                if not isinstance(record[name], list):
                    record[name] = [record[name]]
                record[name].append(value)
            else:
                record[name] = value

        results.append(record)

    return results


def print_results(records):
    """Pretty-print dataset summaries."""
    if not records:
        print("No records found.")
        return

    for rec in records:
        organism_field = rec.get("taxon") or rec.get("species") or rec.get("Organism")
        if isinstance(organism_field, list):
            organism_str = ", ".join(organism_field)
        else:
            organism_str = organism_field or "—"

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
        description="Search NCBI databases (default: GEO GDS) by keyword."
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="One or more keywords to search for (combined using AND/OR)."
    )
    parser.add_argument(
        "--max",
        type=int,
        default=100,
        help="Maximum number of results (default=100)"
    )
    parser.add_argument(
        "--operator",
        choices=["AND", "OR"],
        default="AND",
        help="Boolean operator to combine keywords (default: AND)"
    )
    parser.add_argument(
        "--db",
        default="gds",
        help="NCBI database to search (default: gds)"
    )

    args = parser.parse_args()

    # Combine keywords
    search_term = f" {args.operator} ".join(args.keywords)

    print(f"Searching NCBI db '{args.db}' for: '{search_term}' ...\n")

    # Run search and summary
    ids = geo_esearch(search_term, db=args.db, retmax=args.max)
    records = geo_esummary(ids, db=args.db)
    print_results(records)


if __name__ == "__main__":
    main()
