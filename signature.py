import os
from pathlib import Path
from bs4 import BeautifulSoup

directory_path = '.'
output_file_path = 'out.txt'

def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'lxml')
    elements = soup.select('.sig-param')
    texts = [element.get_text() for element in elements]
    return '\t'.join(texts) + '\n'

def main():
    output = ''
    for file_name in os.listdir(directory_path):
        print(file_name)
        file_path = Path(directory_path) / file_name
        if file_path.suffix == '.html':
            output += file_name + "\t" + process_html_file(file_path)

    with open(output_file_path, 'a', encoding='utf-8') as out_file:
        out_file.write(output)

    print(f'Results appended to {output_file_path}')

if __name__ == '__main__':
    main()

