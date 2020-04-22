import json
import os
import requests

from time import sleep


base_url = 'https://www.vam.ac.uk/api/json/museumobject/{0}'
count = 0
total = 0

for basepath, dirnames, filenames in os.walk('data'):
    total = total + len([fn for fn in filenames if fn.endswith('.index.json')])

for basepath, dirnames, filenames in os.walk('data'):
    for filename in filenames:
        if filename.endswith('.index.json') and filename.replace('.index.json', '.details.json') not in filenames:
            with open(os.path.join(basepath, filename)) as in_f:
                data = json.load(in_f)
                response = requests.get(base_url.format(data['fields']['object_number']))
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 0:
                        data = data[0]
                        with open(os.path.join(basepath, '{0}.details.json'.format(data['fields']['object_number'])), 'w') as out_f:
                            json.dump(data, out_f)
            count = count + 1
            sleep(5)
        elif filename.endswith('.index.json'):
            count = count + 1
    print('Processed {0} of {1} ({2:.2f}%)'.format(count, total, count / total * 100 if total > 0 else 0))
