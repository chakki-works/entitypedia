# -*- coding: utf-8 -*-
"""
Code for mapping seeds to other format.
"""

import argparse
import csv
import glob
import json
import os
import re
from collections import defaultdict


title2id = {}


def load_seeds(seed_dir):
    files = glob.glob(os.path.join(seed_dir, '**/*.csv'), recursive=True)
    d = defaultdict(list)
    for file in files:
        idx = file.index('seeds/')
        entity_type = file[idx+len('seeds/'):][:-4]  # cut .csv
        with open(file) as f:
            reader = csv.reader(f)
            for line in reader:
                try:
                    title, url, id = line[0], line[1], line[2]
                    title2id[title] = id
                    d[entity_type].append(title)
                except ValueError:
                    print('Error line is: {}'.format(line))

    return d


def save_seeds(seeds, file):
    with open(file, 'w') as f:
        for name, instances in seeds.items():
            for ins in instances:
                obj = {'class': name, 'val': ins, 'id': title2id[ins]}
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


def main(args):
    seeds = load_seeds(args.seed_dir)
    # seeds = mappings(seeds)
    save_seeds(seeds, args.save_file)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
    parser = argparse.ArgumentParser(description='Mapping seeds to other format.')
    parser.add_argument('--seed_dir', default=os.path.join(DATA_DIR, 'raw/seeds'), help='seed directory')
    parser.add_argument('--save_file', default=os.path.join(DATA_DIR, 'interim/seeds.jsonl'), help='save file')
    args = parser.parse_args()
    main(args)
