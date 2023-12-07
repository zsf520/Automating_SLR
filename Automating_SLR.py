from modules.query import *
from modules.bib_to_csv import *
import os


def is_valid_folder_name(folder_name):
    # Check if the folder name is a valid directory name
    return bool(folder_name) and not any(char in r'\/:*?"<>|' for char in folder_name)


if __name__ == "__main__":

    slr_folder = './SLRs'  # Specify the subdirectory where the folders will be created

    # Ensure the 'SLR' subdirectory exists
    if not os.path.exists(slr_folder):
        os.makedirs(slr_folder)

    generate_query()

    while True:
        # Get user input for the folder name
        search_folder_name = input(
            "\nYou can name this SLR and a folder will be created with this name for subsequent operations: ").strip()
        search_folder_name = search_folder_name

        # Validate folder name
        if not is_valid_folder_name(search_folder_name):
            print("Invalid folder name. Please avoid special characters and make sure it's a valid directory name.")
            continue

        # Try creating the search folder
        try:
            os.makedirs(os.path.join(slr_folder, search_folder_name))
            break  # Break the loop if folder creation is successful
        except FileExistsError:
            print(f"The folder '{search_folder_name}' already exists. Please choose a different name.")

    # Pause and wait for user input
    input("\nCopy Query to search in ODLs, export the results as BibTex files, and put the BibTex files into the "
          f"'{slr_folder}/{search_folder_name}' folder, then press Enter to start analysis")

    print("\nProcessing. Please wait...")

    # Specify the folder where the BibTeX file is located
    bib_folder = os.path.join(slr_folder, search_folder_name)

    # Get all bib files in the folder
    bib_files = list_bib_files(bib_folder)

    # Specify the output CSV file path
    output_csv = os.path.join(slr_folder, search_folder_name, f"{search_folder_name}.csv")

    # Get the publication type
    publication_types = choose_publication_types(bib_folder)

    # Call the processing function, remove duplicates and generate CSV, and apply filtering conditions
    bib_to_csv(bib_files, output_csv, publication_types=publication_types)

    input(
        f"\nResult file '{search_folder_name}.csv' created in the '{slr_folder}/{search_folder_name}' folder. Press "
        f"'ENTER' to"
        f"exit...")
