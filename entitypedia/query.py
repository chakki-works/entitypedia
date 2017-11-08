import os

from jinja2 import Environment, FileSystemLoader


class QueryBuilder(object):

    def __init__(self, template_dir=os.path.join(os.path.dirname(__file__), '../data/sparql')):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def build(self, template_file, **kwargs):
        template = self.env.get_template(template_file)
        query = template.render(kwargs)

        return query
