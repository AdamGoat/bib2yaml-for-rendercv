import bibtexparser
# from pylatexenc.latex2text import LatexNodes2Text
import yaml

# lt = LatexNodes2Text()

months_to_num_dict = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}

def null_checker(bib_entry, key):
    return bib_entry[key] if key in bib_entry and bib_entry[key] is not None else None

def bib2yaml(input_file, output_file, author_name, sort_by_date=True, number_papers=True):
    with open(input_file) as f:
        db = bibtexparser.load(f)

    new_output = []

    if sort_by_date:
        sortedDB = sorted(db.entries, key=lambda x: (x.get("year", ""), x.get("month", "")), reverse=True)
    else:
        sortedDB = db.entries

    num_papers = len(sortedDB) + 1

    for entry in sortedDB:

        # TODO: Check if the any of the visible name is same as the CV author, if yes then encapsulate in "***"

        authors = [author.strip() for author in entry["author"].split("and")]
        authors = ["***"+author+"***" if author_name in author else author for author in authors]
        # if len(authors) > 7:
        #     authors = [authors[0], "et al."]
        if number_papers:
            num_papers -= 1
            filtered_entry = {
                "title": f"{num_papers}. {entry['title']}",
                "authors": authors,
                "journal": null_checker(entry, "journal"),
                "doi": null_checker(entry, "doi"),
                "url": null_checker(entry, "url"),
            }
        else:
            filtered_entry = {
                "title":  entry["title"],
                "authors": authors,
                "journal": null_checker(entry, "journal"),
                "doi": null_checker(entry, "doi"),
                "url": null_checker(entry, "url"),
            }

        year = entry.get("year")
        month = entry.get("month").lower() if entry.get("month") else None

        if year:
            full_date = str(year)
            if month:
                full_date = f"{year}-{months_to_num_dict[month]:02d}"

        filtered_entry["date"] = full_date

        new_output.append({key: value for key, value in filtered_entry.items() if value is not None})

    with open(output_file, "w") as yaml_file:
        yaml.dump(new_output, yaml_file, sort_keys=False)

    print(f"Entries have been written to {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert BibTeX to YAML format.")
    parser.add_argument("input_file", help="Path to the input BibTeX file.")
    parser.add_argument("output_file", help="Path to the output YAML file.")
    parser.add_argument("author_name", help="Name of the author to highlight in the YAML output.")
    parser.add_argument("--sort_by_date", action="store_true", help="Sort entries by date.")
    parser.add_argument("--number_papers", action="store_true", help="Number the papers.")

    args = parser.parse_args()

    bib2yaml(args.input_file, args.output_file, args.author_name, args.sort_by_date, args.number_papers) 
    # Example usage:
    # bib2yaml("pubs.bib", "pubs.yml", sort_by_date=True, number_papers=True)
    # This will convert the BibTeX file "pubs.bib" to "pubs.yml", sorting by date and numbering the papers. 
    # Note: The `sort_by_date` argument is implemented to sort entries by year and month.
