import json
import os
import re
import requests

from bs4 import BeautifulSoup
from time import sleep



def get_text(root, selector, default=''):
    result = root.select(selector)
    if len(result) > 0:
        return result[0].text
    return default


def format_field(field: str) -> str:
    parts = re.split('\s+|/+', field)
    result = []
    for idx, part in enumerate(parts):
        if idx == 0:
            result.append(part.lower())
        else:
            result.append(part.title())
    return ''.join(result)


search_base_url = 'https://api.vam.ac.uk/v2/objects/search?images_exist=true&page='
record_base_url = 'https://collections.vam.ac.uk/item/'

meta_response = requests.get(f'{search_base_url}1')
if meta_response.status_code == 200:
    data = meta_response.json()
    pages = data['info']['pages']

    for page in range(1, pages + 1):
        print(f'Processing page {page} of {pages}')
        search_response = requests.get(f'{search_base_url}{page}')
        if search_response.status_code == 200:
            data = search_response.json()
            total = data['info']['pages']
            for record in data['records']:
                filename = os.path.join('data', *record['systemNumber'], f'{record["systemNumber"]}.json')
                dirname = os.path.dirname(filename)
                if not os.path.exists(dirname):
                    os.makedirs(dirname, exist_ok=True)
                if not os.path.exists(filename):
                    record_response = requests.get(f'{record_base_url}{record["systemNumber"]}')
                    if record_response.status_code == 200:
                        doc = BeautifulSoup(record_response.text, 'html.parser')
                        record['title'] = get_text(doc, 'h1.object-page__title', 'Untitled')
                        record['description'] = get_text(doc, '.etc-details__cell-free-content', '')
                        for row in doc.select('table.etc-details tbody tr'):
                            field = get_text(row, 'td.etc-details__cell-name', None)
                            value = row.select('td.etc-details__cell-data')
                            if field and value:
                                value = value[0]
                                field_name = format_field(field)
                                if value.select('li'):
                                    record[field_name] = [item.text for item in value.select('li')]
                                elif value.select('a'):
                                    record[field_name] = [item.text for item in value.select('a')]
                                else:
                                    record[field_name] = value.text
                        with open(filename, 'w') as out_f:
                            json.dump(record, out_f)
                        sleep(1)
        sleep(5)
