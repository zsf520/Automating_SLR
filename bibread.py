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

def bib_to_csv(bib_file_paths, csv_file_path):
    unique_entries = set()  # 用于跟踪已经处理过的条目
    duplicate_count = 0

    # 打开CSV文件以写入
    with open(csv_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        # 创建CSV写入器，指定引号的规则为csv.QUOTE_MINIMAL
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)

        # 写入CSV文件的标题行
        csv_writer.writerow(['Title', 'Abstract', 'Authors', 'Keywords', 'DOI', 'Publication Date'])

        # 处理每个BibTeX文件
        for bib_file_path in bib_file_paths:
            # 检测BibTeX文件编码
            bib_encoding = detect_encoding(bib_file_path)

            # 读取BibTeX文件，使用检测到的编码
            with open(bib_file_path, 'r', encoding=bib_encoding) as bib_file:
                bib_database = bibtexparser.load(bib_file)

            # 遍历BibTeX数据库的每一项，并将所需字段写入CSV文件
            for entry in bib_database.entries:
                # 获取所需字段的值，如果字段不存在则为空字符串
                title = entry.get('title', '')
                abstract = entry.get('abstract', '')
                authors = entry.get('author', '')
                keywords = entry.get('keywords', '')
                doi = entry.get('doi', '')
                pub_date = entry.get('year', '')  # 这里简化为使用'year'字段作为publication date

                # 利用标题和作者信息判断条目是否已经处理过，防止重复
                entry_identifier = f"{title}_{authors}"
                if entry_identifier not in unique_entries:
                    # 写入CSV文件
                    csv_writer.writerow([title, abstract, authors, keywords, doi, pub_date])
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

    # 调用处理函数，去重并生成CSV
    bib_to_csv(bib_files, output_csv)
