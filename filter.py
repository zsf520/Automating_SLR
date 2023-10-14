from bibread import *


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

        # Get the number of pages
        pages = extract_page_number(entry)

        # Determine whether to retain the entry based on filter conditions
        pages_condition = (min_pages is None or (pages is not None and pages >= min_pages)) and \
                          (max_pages is None or (pages is not None and pages <= max_pages))

        types_condition = publication_types is None or entry_type in publication_types

        if pages_condition and types_condition:
            # Add 'pages' and 'entry_type' to entry
            entry['pages'] = pages
            entry['entry_type'] = entry_type
            filtered_entries.append(entry)

    return filtered_entries
