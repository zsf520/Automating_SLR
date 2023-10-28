import bibtexparser
import csv
from modules.filter import *


def get_unique_publication_types(bib_file_paths):
    unique_types = set()

    for bib_file_path in bib_file_paths:
        with open(bib_file_path, 'r', encoding=detect_encoding(bib_file_path), errors='replace') as bib_file:
            bib_database = bibtexparser.load(bib_file)
            for entry in bib_database.entries:
                entry_type = entry.get('ENTRYTYPE', '').lower()
                unique_types.add(entry_type)

    return list(unique_types)


def choose_publication_types(bib_folder):
    bib_files = list_bib_files(bib_folder)
    unique_publication_types = get_unique_publication_types(bib_files)

    if not unique_publication_types:
        print("No publication types found.")
        return None

    print("Available Publication Types:")
    for index, entry_type in enumerate(unique_publication_types, start=1):
        print(f"{index}. {entry_type}")

    while True:
        selection = input(
            "Enter the number(s) of the publication type(s) you want to include (comma-separated), "
            "or press Enter to include all types: ")

        if not selection:
            return unique_publication_types

        try:
            selected_indices = [int(idx) for idx in selection.split(',')]
            if all(1 <= idx <= len(unique_publication_types) for idx in selected_indices):
                selected_types = [unique_publication_types[idx - 1] for idx in selected_indices]
                return selected_types
            else:
                print("Invalid input. Please enter valid numbers within the listed range.")
        except ValueError:
            print("Invalid input. Please enter valid numbers separated by commas.")


def bib_to_csv(bib_file_paths, csv_file_path, min_pages=None, max_pages=None,
               start_date=None, end_date=None, publication_types=None):
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

    # Get user input for publication date restrictions
    if start_date is None:
        start_date_input = input(
            "\nEnter the start year for publication date limit (Press 'ENTER' without typing anything to have no "
            "limit):").strip()
        start_date = int(start_date_input) if start_date_input.isdigit() else None

    if end_date is None:
        end_date_input = input(
            "\nEnter the end year for publication date limit (Press 'ENTER' without typing anything to have no "
            "limit):").strip()
        end_date = int(end_date_input) if end_date_input.isdigit() else None

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
            # Use the new filter_by_publication_date function
            filtered_entries = filter_by_publication_date(filtered_entries, start_date, end_date)

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
                entry_identifier = f"{title.lower()}_{authors.lower()}"
                if entry_identifier not in unique_entries:
                    # Write to CSV file
                    csv_writer.writerow([entry_type, title, abstract, authors, keywords, doi, pub_date, pages])
                    unique_entries.add(entry_identifier)
                else:
                    duplicate_count += 1

    print(f"\nDetected and removed {duplicate_count} duplicate entries.")
    print("\nThe result file has been created in 'output' folder.")
