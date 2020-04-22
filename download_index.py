import json
import os
import requests

from time import sleep


base_url = 'https://www.vam.ac.uk/api/json/museumobject/search?before=2030&images=1&limit=45&offset={0}'
offset = 0
total = None

while total is None or offset <= total:
    response = requests.get(base_url.format(offset))
    if response.status_code == 200:
        data = response.json()
        total = data['meta']['result_count']
        for record in data['records']:
            filename = list(record['fields']['object_number'][1:])
            dirname = os.path.join('data', *filename)
            filename = os.path.join(dirname, '{0}.index.json'.format(record['fields']['object_number']))
            os.makedirs(dirname, exist_ok=True)
            with open(filename, 'w') as out_f:
                json.dump(record, out_f)
    offset = offset + 45
    print('Downloaded {0} of {1}'.format(offset, total))
    sleep(5)
