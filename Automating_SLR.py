from modules.query import *
from modules.bib_to_csv import *

if __name__ == "__main__":
    generate_query()

    # Pause and wait for user input
    input("\nCopy Query to search in ODLs, export the results as BibTex files, and put the BibTex files into the "
          "‘bibfiles’ folder, then press Enter to start analysis")

    print("\nProcessing. Please wait...")

    # Specify the folder where the BibTeX file is located
    bib_folder = './bibfiles'

    # Get all bib files in the folder
    bib_files = list_bib_files(bib_folder)

    # Specify the output CSV file path
    output_csv = './output/output.csv'

    # Get the publication type
    publication_types = choose_publication_types(bib_folder)

    # Call the processing function, remove duplicates and generate CSV, and apply filtering conditions
    bib_to_csv(bib_files, output_csv, publication_types=publication_types)

    input("\nPress 'ENTER' to exit...")
