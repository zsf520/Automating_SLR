def format_keyword(keyword):
    # 如果关键词是词组，用引号包裹；如果是单词，加上星号
    if " " in keyword:
        return f'"{keyword}"'
    else:
        return f"{keyword}*"

def find_and_print_synonym_groups():
    synonym_groups = []

    while True:
        user_input = input("Enter a group of synonyms (comma-separated), or press 'ENTER' without typing anything to finish: ")
        
        if user_input.lower() == '':
            break

        keywords = [word.strip() for word in user_input.split(",")]
        
        formatted_keywords = [format_keyword(keyword) for keyword in keywords]
        current_group = f"({' OR '.join(formatted_keywords)})"
        synonym_groups.append(current_group)

    # 输出同义词组，用AND连接
    if synonym_groups:
        print("Query:")
        print(" AND ".join(synonym_groups))
    else:
        print("No input query found.")

if __name__ == "__main__":
    find_and_print_synonym_groups()
