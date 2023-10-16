import bibtexparser
import csv
from modules.filter import *


def bib_to_csv(bib_file_paths, csv_file_path, min_pages=None, max_pages=None, publication_types=None):
    unique_entries = set()  # Used to track items that have been processed
    duplicate_count = 0

    # Get the upper and lower limits of the number of pages entered by the user
    if min_pages is None:
        min_pages_input = input(
            "\nEnter the minimum page limit (Press 'ENTER' without typing anything to have no limit):").strip()
        min_pages = int(min_pages_input) if min_pages_input else None

    if max_pages is None:
        max_pages_input = input(
            "\nEnter the maximum page limit (Press 'ENTER' without typing anything to have no limit):").strip()
        max_pages = int(max_pages_input) if max_pages_input else None

    # Get the publication type entered by the user, multiple are allowed, separated by commas
    if publication_types is None:
        types_input = input("\nEnter publication type limits (Press 'ENTER' without typing anything to have no limit, "
                            "separate multiple types with commas):")
        publication_types = [map_entry_type(t.strip().lower()) for t in types_input.split(',')] if types_input else None

    # Open CSV file for writing
    print("\nProcessing. Please wait...")
    with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        # Create a CSV writer, specify the quotation mark rule as csv.QUOTE_MINIMAL, and set the escape character to
        # double quotation marks
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL, escapechar='"')

        # Write the header row of the CSV file
        csv_writer.writerow(['Type', 'Title', 'Abstract', 'Authors', 'Keywords', 'DOI', 'Publication Date', 'Pages'])

        # Process each BibTeX file
        for bib_file_path in bib_file_paths:
            # Detect BibTeX file encoding
            bib_encoding = detect_encoding(bib_file_path)

            # Read BibTeX files, using the detected encoding
            with open(bib_file_path, 'r', encoding=bib_encoding) as bib_file:
                bib_database = bibtexparser.load(bib_file)

            # Use filter_entries function to filter
            filtered_entries = filter_entries(bib_database.entries, min_pages, max_pages, publication_types)

            # Traverse each filtered item and write the required fields to the CSV file
            for entry in filtered_entries:
                # Get the value of the required field, or 'No data' if the field does not exist
                title = entry.get('title', 'No data')
                abstract = entry.get('abstract', 'No data')
                authors = entry.get('author', 'No data')
                keywords = entry.get('keywords', 'No data')
                doi = entry.get('doi', 'No data')
                pub_date = entry.get('year', 'No data')
                pages = entry.get('pages', 'No data')
                entry_type = entry.get('entry_type', 'No data')

                # Use title and author information to determine whether the entry has been processed to prevent
                # duplication
                entry_identifier = f"{title}_{authors}"
                if entry_identifier not in unique_entries:
                    # Write to CSV file
                    csv_writer.writerow([entry_type, title, abstract, authors, keywords, doi, pub_date, pages])
                    unique_entries.add(entry_identifier)
                else:
                    duplicate_count += 1

    # print(f"\nDetected and removed {duplicate_count} duplicate entries.")
    print("\nThe result file has been created in 'output' folder.")
