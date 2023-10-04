from bibread import*
from query import*

if __name__ == "__main__":
    query()

    # 暂停并等待用户输入
    input("press Enter to continue")

    # 指定BibTeX文件所在文件夹
    bib_folder = './bibfiles'

    # 获取文件夹内所有的bib文件
    bib_files = list_bib_files(bib_folder)

    # 指定输出的CSV文件路径
    output_csv = 'output.csv'

    # 调用处理函数，去重并生成CSV，并应用过滤条件
    bib_to_csv(bib_files, output_csv)