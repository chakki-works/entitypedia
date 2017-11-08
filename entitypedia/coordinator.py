class Coordinator(object):

    def __init__(self, query_generator, api, saver):
        self.generator = query_generator
        self.api = api
        self.saver = saver

    def execute(self, template_file, template_args={}, save_file=''):
        query = self.generator.build(template_file, **template_args)
        results = self.api.run_query(query)
        self.saver.save(results, save_file)
