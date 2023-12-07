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
    print("Choose logical operators 'OR' or 'AND' between different keyword groups.")
    print("Choose 6 to end entering.")
    # Prompt user to choose a search field or end input
    print("\nChoose a search field number or enter '6' to finish:")
    for i, option in enumerate(label_options, 1):
        print(f"{i}. {option}")
    print(f"{len(label_options) + 1}. End")

    synonym_batches = []

    logical_operators = []

    while True:

        label_input = input("\nEnter the search field number or choose 6 to end: ")

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

            # If there are multiple batches, prompt the user to choose the logical operator for connecting groups
            if len(synonym_batches) > 1:
                print("\nChoose the logical operator for connecting this group with the previous one:")
                print("1. OR")
                print("2. AND")

                operator_choice = input("Enter the number of your choice: ")

                # Validate the operator choice input
                while operator_choice not in ['1', '2']:
                    print("Invalid input. Please enter either '1' or '2'.")
                    operator_choice = input("Enter the number of your choice: ")

                # Map the user's choice to the corresponding logical operator
                logical_operator = 'OR' if operator_choice == '1' else 'AND'
                logical_operators.append(logical_operator)

        except ValueError:
            print("Invalid input format. Please enter a valid search field number.")
            continue

    # print("Synonym batches:")
    # for batch in synonym_batches:
    #     print(f"{batch['label']}: {batch['keywords']}")

    # Update each batch with the corresponding logical operator
    for i, batch in enumerate(synonym_batches[1:], 1):
        batch['logical_operator'] = logical_operators[i - 1]

    return synonym_batches


def generate_acm_query(synonym_batches):
    """
    Process user-inputted synonym batches and generate a query based on ACM Digital Library syntax.
    """
    acm_labels = ['AllField', 'Title', 'ContribAuthor', 'Abstract', 'Keyword']
    query_parts = []

    for i, batch in enumerate(synonym_batches):
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

        # Get the logical operator for connecting groups, default to 'AND' if not present
        logical_operator = batch.get('logical_operator', 'AND')

        # Create a query part for the current batch
        query_part = f"{acm_labels[label_options.index(label)]}:({keyword_str})"

        # Add the logical operator before each group except for the first one
        if i > 0:
            query_parts.append(f' {logical_operator} ')

        query_parts.append(query_part)

    # Combine query parts using ACM Digital Library syntax
    final_query = ''.join(query_parts)

    return final_query


def generate_ieee_query(synonym_batches):
    """
    Process user-inputted synonym batches and generate a query based on IEEE Xplore syntax.
    """
    ieee_labels = ['All Metadata', 'Document Title', 'Authors', 'Abstract', 'Author Keywords']
    query_parts = []

    for i, batch in enumerate(synonym_batches):
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

        # Get the logical operator for connecting groups, default to 'AND' if not present
        logical_operator = batch.get('logical_operator', 'AND')

        # Create a query part for the current batch
        query_parts.append(f' {logical_operator} ({keyword_str})' if i > 0 else f'({keyword_str})')

    # Combine query parts using IEEE Xplore syntax
    final_query = ''.join(query_parts)

    return final_query


def generate_wos_query(synonym_batches):
    """
    Process user-inputted synonym batches and generate a query based on Web of Science syntax.
    """
    wos_labels = ['ALL', 'TI', 'AU', 'AB', 'AK']
    query_parts = []

    for i, batch in enumerate(synonym_batches):
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

        # Get the logical operator for connecting groups, default to 'AND' if not present
        logical_operator = batch.get('logical_operator', 'AND')

        # Create a query part for the current batch
        query_part = f"{wos_labels[label_options.index(label)]}=({keyword_str})"
        query_parts.append(f' {logical_operator} {query_part}' if i > 0 else f'{query_part}')

    # Combine query parts using Web Of Science syntax
    final_query = ''.join(query_parts)

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
