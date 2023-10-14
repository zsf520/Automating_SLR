import chardet
import os


def list_bib_files(folder_path):
    bib_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".bib"):
            bib_files.append(os.path.join(folder_path, file))
    return bib_files


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def extract_page_number(entry):
    # Try to get the number of pages from the 'numpages' field
    numpages = entry.get('numpages', '')
    if numpages.isdigit():
        return int(numpages)

    # Try to extract the page number range from the 'pages' field and calculate the number of pages, if '-' is not
    # present, the number of pages is 1
    pages = entry.get('pages', '')

    # Check if the string is valid before trying to split
    if '-' in pages:
        start, end = map(str.strip, pages.split('-'))
        if start.isdigit() and end.isdigit():
            return int(end) - int(start) + 1

    # If the 'pages' field does not exist or cannot be parsed, return "No data"
    return "No data"
