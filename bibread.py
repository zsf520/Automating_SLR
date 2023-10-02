import bibtexparser
import csv
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
    # 尝试从 'numpages' 字段中获取页数
    numpages = entry.get('numpages', '')
    if numpages.isdigit():
        return int(numpages)

    # 尝试从 'pages' 字段中提取页码范围并计算页数，如果不存在 '-'，则页数为 1
    pages = entry.get('pages', '')
    if '-' in pages:
        start, end = map(int, pages.split('-'))
        return end - start + 1
    else:
        return 1

def map_entry_type(entry_type):
    # 将用户输入的类型映射为相应的BibTeX类型
    type_mapping = {
        'journal': 'article',
        'conference': 'inproceedings'
        # 添加其他类型的映射
    }

    # 处理直接输入 "journal" 或 "conference" 的情况
    lower_entry_type = entry_type.lower()
    if lower_entry_type in type_mapping:
        return type_mapping[lower_entry_type]

    return entry_type

def filter_entries(entries, min_pages=None, max_pages=None, publication_types=None):
    filtered_entries = []

    for entry in entries:
        # 获取所需字段的值，如果字段不存在则为空字符串
        entry_type = entry.get('ENTRYTYPE', '').lower()  # 获取条目类型，并转换为小写

        # 获取页数
        pages = extract_page_number(entry)

        # 根据过滤条件判断是否保留该条目
        pages_condition = (min_pages is None or (pages is not None and pages >= min_pages)) and \
                          (max_pages is None or (pages is not None and pages <= max_pages))

        types_condition = publication_types is None or entry_type in publication_types

        if pages_condition and types_condition:
            # 添加 'pages' 和 'entry_type' 到 entry 中
            entry['pages'] = pages
            entry['entry_type'] = entry_type
            filtered_entries.append(entry)

    return filtered_entries

def bib_to_csv(bib_file_paths, csv_file_path, min_pages=None, max_pages=None, publication_types=None):
    unique_entries = set()  # 用于跟踪已经处理过的条目
    duplicate_count = 0

    # 获取用户输入的页数上下限
    if min_pages is None:
        min_pages_input = input("请输入最小页数限制（留空则不限制）: ").strip()
        min_pages = int(min_pages_input) if min_pages_input else None

    if max_pages is None:
        max_pages_input = input("请输入最大页数限制（留空则不限制）: ").strip()
        max_pages = int(max_pages_input) if max_pages_input else None

    # 获取用户输入的出版类型，允许多个，用逗号分隔
    if publication_types is None:
        types_input = input("请输入出版类型限制（留空则不限制，多个类型用逗号分隔）: ")
        publication_types = [map_entry_type(t.strip().lower()) for t in types_input.split(',')] if types_input else None

    # 打开CSV文件以写入
    with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        # 创建CSV写入器，指定引号的规则为csv.QUOTE_MINIMAL，并设置转义字符为双引号
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL, escapechar='"')

        # 写入CSV文件的标题行
        csv_writer.writerow(['Type', 'Title', 'Abstract', 'Authors', 'Keywords', 'DOI', 'Publication Date', 'Pages'])

        # 处理每个BibTeX文件
        for bib_file_path in bib_file_paths:
            # 检测BibTeX文件编码
            bib_encoding = detect_encoding(bib_file_path)

            # 读取BibTeX文件，使用检测到的编码
            with open(bib_file_path, 'r', encoding=bib_encoding) as bib_file:
                bib_database = bibtexparser.load(bib_file)

            # 使用 filter_entries 函数进行过滤
            filtered_entries = filter_entries(bib_database.entries, min_pages, max_pages, publication_types)

            # 遍历过滤后的每一项，并将所需字段写入CSV文件
            for entry in filtered_entries:
                # 获取所需字段的值，如果字段不存在则为空字符串
                title = entry.get('title', '')
                abstract = entry.get('abstract', '')
                authors = entry.get('author', '')
                keywords = entry.get('keywords', '')
                doi = entry.get('doi', '')
                pub_date = entry.get('year', '')  # 这里简化为使用'year'字段作为publication date
                pages = entry.get('pages', '')
                entry_type = entry.get('entry_type', '')

                # 利用标题和作者信息判断条目是否已经处理过，防止重复
                entry_identifier = f"{title}_{authors}"
                if entry_identifier not in unique_entries:
                    # 写入CSV文件
                    csv_writer.writerow([entry_type, title, abstract, authors, keywords, doi, pub_date, pages])
                    unique_entries.add(entry_identifier)
                else:
                    duplicate_count += 1

    print(f"Detected and removed {duplicate_count} duplicate entries.")

if __name__ == "__main__":
    # 指定BibTeX文件所在文件夹
    bib_folder = './bibfiles'

    # 获取文件夹内所有的bib文件
    bib_files = list_bib_files(bib_folder)

    # 指定输出的CSV文件路径
    output_csv = 'output.csv'

    # 调用处理函数，去重并生成CSV，并应用过滤条件
    bib_to_csv(bib_files, output_csv)