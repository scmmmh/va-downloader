import json
import os
import requests

from time import sleep


base_url = 'http://media.vam.ac.uk/media/thira/{0}'
count = 0
total = 0

for basepath, dirnames, filenames in os.walk('data'):
    total = total + len([fn for fn in filenames if fn.endswith('.details.json')])

for basepath, dirnames, filenames in os.walk('data'):
    for filename in filenames:
        if filename.endswith('.details.json'):
            with open(os.path.join(basepath, filename)) as in_f:
                data = json.load(in_f)
                if len(data['fields']['image_set']) == 0:
                    os.unlink(os.path.join(basepath, filename))
                    os.unlink(os.path.join(basepath, filename.replace('.details.json', '.index.json')))
                else:
                    missing = []
                    for idx, img in enumerate(data['fields']['image_set']):
                        image_filename = img['fields']['local'][img['fields']['local'].rfind('/') + 1:]
                        if not os.path.exists(os.path.join(basepath, image_filename)):
                            response = requests.get(base_url.format(img['fields']['local']))
                            if response.status_code == 200:
                                with open(os.path.join(basepath, image_filename), 'wb') as out_f:
                                    out_f.write(response.content)
                            else:
                                missing.append(idx)
                            sleep(1)
                    if missing:
                        missing.reverse()
                        for idx in missing:
                            del data['fields']['image_set'][idx]
                        with open(os.path.join(basepath, filename), 'w') as out_f:
                            json.dump(data, out_f)
            count = count + 1
    print('Processed {0} of {1} ({2:.2f}%)'.format(count, total, count / total * 100 if total > 0 else 0))
