from modules.query import *
from modules.bib_to_csv import *

if __name__ == "__main__":
    query()

    # Pause and wait for user input
    input("\nCopy Query to search in ODLs, export the results as BibTex files, and put the BibTex files into the "
          "‘bibfiles’ folder, then press Enter to continue")

    # Specify the folder where the BibTeX file is located
    bib_folder = './bibfiles'

    # Get all bib files in the folder
    bib_files = list_bib_files(bib_folder)

    # Specify the output CSV file path
    output_csv = './output/output.csv'

    # Call the processing function, remove duplicates and generate CSV, and apply filtering conditions
    bib_to_csv(bib_files, output_csv)

    input("\nPress 'ENTER' to exit...")
