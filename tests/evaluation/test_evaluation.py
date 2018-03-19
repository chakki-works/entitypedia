import os
import unittest

from seqeval.metrics import f1_score, classification_report, accuracy_score

from entitypedia.evaluation.converter import to_iob2
from entitypedia.knowledge_ner.recognizer import KnowledgeBaseRecognizer
from entitypedia.corpora.datasets import load_jsonl


class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recognizer = KnowledgeBaseRecognizer()
        file = os.path.join(os.path.dirname(__file__), '../../data/interim/title_entity.jsonl')
        for d in load_jsonl(file):
            entity, label = list(d.items())[0]
            sub_type = label.split('/')[-1]
            label = label.split('/')[0]
            cls.recognizer.add_entity(entity, label)
            cls.recognizer.add_word(entity, sub_type, page_url='', image_url='')
        cls.recognizer.build()

    def setUp(self):
        BASE_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw/corpora')
        self.mainichi_dir = os.path.join(BASE_DIR, 'mainichi')
        self.bccwj_dir = os.path.join(BASE_DIR, 'bccwj')

    def test_f1_score(self):
        remove_types = {'volume', 'period_date', 'percent', 'url', 'service', 'multiplication',
                        'n_person', 'school_age', 'seismic_intensity', 'period_month',
                        'phone_number', 'rank', 'n_animal', 'countx_other', 'point',
                        'periodx_other', 'calorie', 'space', 'period_time', 'n_country',
                        'n_product', 'numex_other', 'latitude_longtitude', 'id_number',
                        'n_flora', 'facility_part', 'temperature', 'weight', 'age', 'water_root',
                        'n_natural_object_other', 'intensity', 'time', 'n_facility',
                        'n_organization', 'postal_address', 'period_year', 'ordinal_number',
                        'physical_extent', 'speed', 'measurement_other', 'seismic_magnitude',
                        'n_event', 'period_week', 'frequency', 'ignored', 'stock', 'n_location_other'}
        X_true, y_true = to_iob2(self.mainichi_dir, remove_types)
        y_pred = [self.recognizer.iob2(text) for text in X_true]
        print(classification_report(y_true, y_pred))
        print(f1_score(y_true, y_pred))
        print(accuracy_score(y_true, y_pred))
        s_true, s_pred = set(), set()
        for y_t, y_p in zip(y_true, y_pred):
            for t, p in zip(y_t, y_p):
                s_true.add(t.split('-')[-1])
                s_pred.add(p.split('-')[-1])
        print(s_true.intersection(s_pred))
        print(s_true - s_pred)
        print(s_pred - s_true)