# Define label options globally
label_options = ['All field', 'Title', 'Author', 'Abstract', 'Keyword']


def query():
    """
    Generate a search query based on user input of keywords groups with labels.
    """
    print(
        "Specify a search field by choosing corresponding number and then enter a group of keywords separated by "
        "commas .")
    print("An OR relationship will be set between words within one keywords group.")
    print("An AND relationship will be set between different keywords groups.")
    print("Choose 6 to end entering.")
    # Prompt user to choose a search field or end input
    print("\nChoose a search field number or enter '6' to finish:")
    for i, option in enumerate(label_options, 1):
        print(f"{i}. {option}")
    print(f"{len(label_options) + 1}. End")

    synonym_batches = []

    while True:

        label_input = input("\nEnter the search field number: ")

        try:
            label_index = int(label_input)

            if label_index == 6:
                break

            if 1 <= label_index <= len(label_options):
                user_friendly_label = label_options[label_index - 1]
            else:
                print("Invalid search field number. Please choose a number from the list.")
                continue

            # Prompt user to enter keywords for the selected search field
            while True:
                keywords_input = input(f"\nEnter keywords for '{user_friendly_label}': ")

                if keywords_input.strip():  # Check if input is not empty
                    break
                else:
                    print("Invalid input. Keywords cannot be empty. Please enter at least one keyword.")

            keywords = [word.strip() for word in keywords_input.split(",")]

            # Create a dictionary for the current batch and update it with the label and keywords
            current_batch = {'label': user_friendly_label, 'keywords': keywords}
            synonym_batches.append(current_batch)

        except ValueError:
            print("Invalid input format. Please enter a valid search field number.")
            continue

    # print("Synonym batches:")
    # for batch in synonym_batches:
    #     print(f"{batch['label']}: {batch['keywords']}")

    return synonym_batches


def generate_acm_query(synonym_batches):
    """
    Process user-inputted synonym batches and generate a query based on ACM Digital Library syntax.
    """
    acm_labels = ['AllField', 'Title', 'ContribAuthor', 'Abstract', 'Keyword']
    query_parts = []

    for batch in synonym_batches:
        label = batch['label']
        keywords = batch['keywords']

        # Process keywords, wrap phrases in double quotes
        processed_keywords = []
        for keyword in keywords:
            if ' ' in keyword:  # Check if the keyword is a phrase
                processed_keywords.append(f'"{keyword}"')
            else:
                processed_keywords.append(keyword)

        # Combine keywords using ACM Digital Library syntax
        keyword_str = f' OR '.join(processed_keywords)

        # Create a query part for the current batch
        query_part = f"{acm_labels[label_options.index(label)]}:({keyword_str})"
        query_parts.append(query_part)

    # Combine query parts using ACM Digital Library syntax
    final_query = f' AND '.join(query_parts)

    return final_query


def generate_ieee_query(synonym_batches):
    """
    Process user-inputted synonym batches and generate a query based on IEEE Xplore syntax.
    """
    ieee_labels = ['All Metadata', 'Document Title', 'Authors', 'Abstract', 'Author Keywords']
    query_parts = []

    for batch in synonym_batches:
        label = batch['label']
        keywords = batch['keywords']

        # Process keywords, wrap phrases in double quotes and add labels
        processed_keywords = []
        for keyword in keywords:
            if ' ' in keyword:  # Check if the keyword is a phrase
                processed_keywords.append(f'"{ieee_labels[label_options.index(label)]}":"{keyword}"')
            else:
                processed_keywords.append(f'"{ieee_labels[label_options.index(label)]}":{keyword}')

        # Combine keywords using IEEE Xplore syntax
        keyword_str = f' OR '.join(processed_keywords)

        # Create a query part for the current batch
        query_parts.append(f'({keyword_str})')

    # Combine query parts using IEEE Xplore syntax
    final_query = f' AND '.join(query_parts)

    return final_query


def generate_wos_query(synonym_batches):
    """
    Process user-inputted synonym batches and generate a query based on Web of Science syntax.
    """
    wos_labels = ['ALL', 'TI', 'AU', 'AB', 'AK']
    query_parts = []

    for batch in synonym_batches:
        label = batch['label']
        keywords = batch['keywords']

        # Process keywords, wrap phrases in double quotes
        processed_keywords = []
        for keyword in keywords:
            if ' ' in keyword:  # Check if the keyword is a phrase
                processed_keywords.append(f'"{keyword}"')
            else:
                processed_keywords.append(keyword)

        # Combine keywords using Web Of Science syntax
        keyword_str = f' OR '.join(processed_keywords)

        # Create a query part for the current batch
        query_part = f"{wos_labels[label_options.index(label)]}=({keyword_str})"
        query_parts.append(query_part)

    # Combine query parts using Web Of Science syntax
    final_query = f' AND '.join(query_parts)

    return final_query


def generate_query():
    synonym_batches = query()
    if synonym_batches:
        acm_query = generate_acm_query(synonym_batches)
        ieee_query = generate_ieee_query(synonym_batches)
        wos_query = generate_wos_query(synonym_batches)
        print("\nACM Digital Library Query:\n", acm_query)
        print("\nIEEE Xplore Query:\n", ieee_query)
        print("\nWeb of Science Query:\n", wos_query)
    else:
        print("No synonym batches entered.")
