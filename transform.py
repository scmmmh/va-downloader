import json
import os

for basepath, _, filenames in os.walk('data'):
    for filename in filenames:
        if filename.endswith('.details.json'):
            with open(os.path.join(basepath, filename)) as in_f:
                data = json.load(in_f)['fields']
            result = {
                'id': data['object_number'],
                'marks': data['marks'],
                'notes': data['history_note'],
                'description': data['public_access_description'],
                'physical_description': data['physical_description'],
                'title': data['descriptive_line'],
                'credit': data['credit'],
                'object': [data['object']],
                'year_start': data['year_start'],
                'year_end': data['year_end'],
                'dimensions': data['dimensions'],
                'date': data['date_text'],
                'place_made': [],
                'people': [],
                'organisations': [],
                'techniques': [],
                'materials': [],
                'categories': [],
                'events': [],
                'subjects': [],
                'concepts': [],
                'labels': [],
                'collections': [],
                'physical_location': [],
                'styles': [],
                'images': [],

            }
            for place in data['places']:
                if place['fields']['source'] == 'production':
                    result['place_made'].append(place['fields']['name'])
                else:
                    print(place['fields'])
            for name in data['names']:
                if name['fields']['name'] != 'Unknown':
                    if name['fields']['type'] == 'person' or name['fields']['type'] == 'people':
                        result['people'].append(name['fields']['name'])
                    elif name['fields']['type'] == 'organisation':
                        result['organisations'].append(name['fields']['name'])
                    else:
                        print(name['fields'])
            for technique in data['techniques']:
                result['techniques'].append(technique['fields']['name'])
            for material in data['materials']:
                result['materials'].append(material['fields']['name'])
            for category in data['categories']:
                result['categories'].append(category['fields']['name'])
            for event in data['events']:
                result['events'].append(event['fields']['name'])
            for subject in data['subjects']:
                if subject['fields']['source'] == 'object':
                    result['subjects'].append(subject['fields']['name'])
                elif subject['fields']['source'] == 'concept':
                    result['concepts'].append(subject['fields']['name'])
            for label in data['labels']:
                result['labels'].append(label['fields']['label_text'])
            for collection in data['collections']:
                result['collections'].append(collection['fields']['name'])
            for gallery in data['galleries']:
                result['physical_location'].append(gallery['fields']['name'])
            for style in data['styles']:
                result['styles'].append(style['fields']['name'])
            for image in data['image_set']:
                result['images'].append(image['fields']['image_id'])
            target_filename = os.path.join(basepath, filename.replace('.details.json', '.transformed.json')).replace('data', 'data-transformed')
            os.makedirs(os.path.dirname(target_filename), exist_ok=True)
            with open(target_filename, 'w') as out_f:
                json.dump(result, out_f)
