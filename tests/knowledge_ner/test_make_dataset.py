import os, glob, csv

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
SAVE_DIR = os.path.join(ROOT_DIR, 'data')
DATA_DIR = os.path.join(ROOT_DIR, '../entitypedia/data/raw/seeds')
files = glob.glob(os.path.join(DATA_DIR, '**/*.csv'), recursive=True)


with open(os.path.join(SAVE_DIR, 'data.csv'), 'w') as wf:
    writer = csv.writer(wf, lineterminator='\n')
    
    for file in files:
        idx = file.index('seeds/')
        entity_type = file[idx+len('seeds/'):][:-4]  # cut '.csv'
        sub_type = entity_type.split('/')[-1]
        entity_type = entity_type.split('/')[0]
        if entity_type in {'color', 'disease', 'natural_object'}:
            continue
        with open(file) as f:
            reader = csv.reader(f)
            for line in reader:
                word, url, page_id, image_url, abst = line
                writer.writerow([word, entity_type, sub_type, url, image_url])
