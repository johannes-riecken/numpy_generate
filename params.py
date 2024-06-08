import json
import os
from pathlib import Path

from bs4 import BeautifulSoup

directory_path = '.'
output_file_path = 'params.txt'

def process_html_file(file_path):
    # Load the HTML content from the file
    with open(file_path, 'r') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the parameter list in the HTML content
    params = []
    field_list = soup.find('dl', class_='field-list')
    if field_list:
        param_dl = field_list.find('dl')
        if param_dl:
            for dt in param_dl.find_all('dt'):
                strong_tag = dt.find('strong')
                classifier = dt.find('span', class_='classifier')
                if strong_tag and classifier:
                    param_names = [name.strip() for name in strong_tag.get_text().split(',')]
                    param_type = classifier.get_text().strip()
                    for name in param_names:
                        params.append({name: param_type})


    # Convert the parameter list to JSON format
    params_json = json.dumps(params)
    return params_json

def main():
    output = ''
    for file_name in sorted(os.listdir(directory_path)):
        file_path = Path(directory_path) / file_name
        if file_path.suffix == '.html':
            output += file_name + "\t" + process_html_file(file_path) + "\n"

    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        out_file.write(output)

    print(f'Results written to {output_file_path}')

if __name__ == '__main__':
    main()
