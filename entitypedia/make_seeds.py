# -*- coding: utf-8 -*-
import csv
import glob
import json
import os
import re
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/raw/seeds')
files = glob.glob(os.path.join(DATA_DIR, '**/*.csv'), recursive=True)
word2id = {}


def load_seeds():
    d = defaultdict(list)
    for file in files:
        idx = file.index('seeds/')
        entity_type = file[idx+len('seeds/'):][:-4]  # cut .csv
        with open(file) as f:
            reader = csv.reader(f)
            for line in reader:
                try:
                    word, url, id = line[0], line[1], line[2]
                    word2id[word] = id
                    d[entity_type].append(word)
                except ValueError:
                    print('Error line is: {}'.format(line))
    print(d.keys())

    return d


def save_seeds(seeds, file):
    with open(file, 'w') as f:
        for name, instances in seeds.items():
            for ins in instances:
                obj = {'class': name, 'val': ins, 'id': word2id[ins]}
                f.write(json.dumps(obj))
                f.write('\n')


def mappings(seeds):
    """
    {
      'person': [...],
      'organization': [...],
      'facility': [...],
      'location': [...],
      'geo_region': [...],
      'objects': [...],
      'arts': [...],
      'living_things': [...],
      'event': [...],
      'other': [...]
    }
    """
    res = defaultdict(list)
    ptn_obj1 = re.compile(r'product/(material|clothing|money_form|drug|weapon|vehicle|food)')
    ptn_obj2 = re.compile(r'natural_object/(element|compound|mineral)')
    for s, instances in seeds.items():
        # 人
        if s.startswith('name'):
            res['name'].extend(instances)
        # 組織
        elif s.startswith('organization'):
            res['organization'].extend(instances)
        # 施設
        elif s.startswith('facility') and not s.startswith('facility/archaeological_place'):
            res['facility'].extend(instances)
        # 地名
        elif s.startswith('location/gpe') or s.startswith('location/region') or s.startswith('facility/archaeological_place'):
            res['location'].extend(instances)
        # 地形
        elif s.startswith('location/spa') or s.startswith('location/geological_region') or s.startswith('location/astral_body'):
            res['geo_region'].extend(instances)
        # 具体物
        elif ptn_obj1.search(s) or ptn_obj2.search(s):
            res['objects'].extend(instances)
        # 創作物
        elif s.startswith('product/art') or s.startswith('product/printing'):
            res['arts'].extend(instances)
        # 動植物
        elif s.startswith('natural_object/living_thing') or s.startswith('natural_object/living_thing_part'):
            res['living_things'].extend(instances)
        # イベント
        elif s.startswith('event') or s.startswith('disease') or s.startswith('color'):
            res['event'].extend(instances)
        else:
            res['other'].extend(instances)

    return res


if __name__ == '__main__':
    filename = 'seeds.jsonl'
    seeds = load_seeds()
    seeds = mappings(seeds)
    for name, instances in seeds.items():
        print('{}: {}'.format(name, len(instances)))
    save_seeds(seeds, filename)
