from modules.bibread import *


def map_entry_type(entry_type):
    # Map the user input type to the corresponding BibTeX type
    type_mapping = {
        'journal': 'article',
        'conference': 'inproceedings'
        # Add other types of mappings
    }

    # Handle direct input of "journal" or "conference"
    lower_entry_type = entry_type.lower()
    if lower_entry_type in type_mapping:
        return type_mapping[lower_entry_type]

    return entry_type


def filter_entries(entries, min_pages=None, max_pages=None, publication_types=None):
    filtered_entries = []

    for entry in entries:
        # Get the value of the required field, or an empty string if the field does not exist
        entry_type = entry.get('ENTRYTYPE', '').lower()  # Get the entry type and convert to lowercase

        # Get pages
        pages = extract_page_number(entry)

        # If user set any page limit, entries' page number with "No data" will be skipped
        if min_pages is not None or max_pages is not None:
            # If the page number is "No data", skip the current entry
            if pages == "No data":
                continue

        # Convert min_pages and max_pages to strings for comparison with the value of the 'pages' field
        min_pages_str = str(min_pages) if min_pages is not None else None
        max_pages_str = str(max_pages) if max_pages is not None else None

        # Determine whether to retain the entry based on filter conditions
        pages_condition = (min_pages_str is None or (pages is not None and pages >= int(min_pages_str))) and \
                          (max_pages_str is None or (pages is not None and pages <= int(max_pages_str)))

        types_condition = publication_types is None or entry_type in publication_types

        if pages_condition and types_condition:
            # Add 'pages' and 'entry_type' to entry
            entry['pages'] = pages
            entry['entry_type'] = entry_type
            filtered_entries.append(entry)

    return filtered_entries
