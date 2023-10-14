def format_keyword(keyword):
    # If the keyword is a phrase, wrap it in quotation marks; if it is a word, add an asterisk
    if " " in keyword:
        return f'"{keyword}"'
    else:
        return f"{keyword}*"


def query():
    print("Enter keywords according to the following orders, and the search query will be generated.")
    print("Enter groups of synonyms separated by commas. Press 'ENTER' without typing anything to finish.")
    print("An OR relationship will be set between words within one synonyms group.")
    print("An AND relationship will be set between different synonyms groups.")

    synonym_groups = []

    while True:
        user_input = input("\nEnter a group of synonyms: ")

        if user_input.lower() == '':
            break

        keywords = [word.strip() for word in user_input.split(",")]

        formatted_keywords = [format_keyword(keyword) for keyword in keywords]
        current_group = f"({' OR '.join(formatted_keywords)})"
        synonym_groups.append(current_group)

    # Output synonymous phrases and connect them with AND
    if synonym_groups:
        print("\nQuery:")
        print(" AND ".join(synonym_groups))
    else:
        print("No input query found.")
