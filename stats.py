import json
import os

from collections import Counter


keys = [
    'object',
    'year_start',
    'year_end',
    'place_made',
    'people',
    'organisations',
    'techniques',
    'materials',
    'categories',
    'events',
    'subjects',
    'concepts',
    'styles',
]
values = dict([(key, []) for key in keys])
coverage = dict([(key, 0) for key in keys])
total = 0

for basepath, _, filenames in os.walk('data-transformed'):
    for filename in filenames:
        if filename.endswith('.transformed.json'):
            with open(os.path.join(basepath, filename)) as in_f:
                data = json.load(in_f)
            for key in keys:
                if data[key]:
                    if isinstance(data[key], list):
                        values[key].extend(data[key])
                    else:
                        values[key].append(data[key])
                    coverage[key] = coverage[key] + 1
            total = total + 1


#for key, entries in values.items():
#    print(key, Counter(entries).most_common())

for key, cover in coverage.items():
    print(key, cover, cover/total)

print(Counter(values['year_end']).most_common())
