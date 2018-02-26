# -*- coding: utf-8 -*-


class Annotator(object):
    """
    Annotates named-entity tag with Wikipedia text.
    """

    def __init__(self):
        self.remove_list = {'volume', 'period_date', 'percent', 'url', 'service', 'multiplication',
                            'n_person', 'school_age', 'seismic_intensity', 'period_month',
                            'phone_number', 'rank', 'n_animal', 'countx_other', 'point',
                            'periodx_other', 'calorie', 'space', 'period_time', 'n_country',
                            'n_product', 'numex_other', 'latitude_longtitude', 'id_number',
                            'n_flora', 'facility_part', 'temperature', 'weight', 'age', 'water_root',
                            'n_natural_object_other', 'intensity', 'time', 'n_facility',
                            'n_organization', 'postal_address', 'period_year', 'ordinal_number',
                            'physical_extent', 'speed', 'measurement_other', 'seismic_magnitude',
                            'n_event', 'period_week', 'frequency', 'ignored', 'stock', 'n_location_other'}

    def extract(self, i, doc, tags):
        tag = []
        while doc[i] != '>':
            tag.append(doc[i])
            i += 1
        i += 1
        tags.append(''.join(tag[1:]))
        if doc[i] == '<':
            return self.extract(i, doc, tags)
        return i, tags

    def extract2(self, i, doc, tags):
        tag = []
        while doc[i] != '>':
            tag.append(doc[i])
            i += 1
        i += 1
        tags.append(''.join(tag[1:]))
        if doc[i:].startswith('</'):
            return self.extract2(i, doc, tags)
        return i, tags

    def annotate(self, doc):
        i, j = 0, 0
        text = []
        spans = []
        entities = []
        while i < len(doc):
            if doc[i] == '<' and not doc[i:].startswith('</'):
                i, tags = self.extract(i, doc, [])
                j = i
            if doc[i:].startswith('</'):
                entities.append(tags)
                spans.append((len(text) - len(doc[j:i]), len(text)))
                i, _ = self.extract2(i, doc, [])
                continue
            text.append(doc[i])
            i += 1

        res = self._build_response(''.join(text), spans, entities)

        return res

    def to_bio(self, html):
        """Converts annotated text into BIO format.
        Args:
            html: html text.
        Return:
            tuple: a text and tags.
        Example:
            >>> html = '<a href="google">Google</a>'
            >>> to_bio(html)
            ('Google',
            ['B-Organization',
            'I-Organization',
            'I-Organization',
            'I-Organization',
            'I-Organization',
            'I-Organization']
        """
        res = self.annotate(html)
        text = res['text']
        entities = res['entities']
        tags = self._get_bio_tags(text, entities)

        return text, tags

    def _get_bio_tags(self, text, entities):
        tags = ['O'] * len(text)
        for entity in entities:
            begin_offset, end_offset = entity['beginOffset'], entity['endOffset']
            entity_type = entity['type']
            if entity_type in self.remove_list:
                continue
            for i in range(begin_offset, end_offset):
                tags[i] = 'I-{}'.format(entity_type)
            tags[begin_offset] = 'B-{}'.format(entity_type)

        return tags

    def _build_response(self, clean_text, spans, entity_types):
        res = {
            'text': clean_text,
            'entities': [

            ]
        }

        for (begin_offset, end_offset), entity_type in zip(spans, entity_types):
            entity = {
                'entity': clean_text[begin_offset: end_offset],
                'type': entity_type[0],
                'beginOffset': begin_offset,
                'endOffset': end_offset
            }
            res['entities'].append(entity)

        return res