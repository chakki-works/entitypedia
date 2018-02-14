import json
import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.web import url

from knowledge_ner.reader import read_csv
from knowledge_ner.recognizer import KnowledgeBaseRecognizer

sample_file = os.path.join(os.path.dirname(__file__), '../../data/data.csv')
recognizer = KnowledgeBaseRecognizer()
for entity, entity_type, sub_type, page_url, image_url in read_csv(sample_file):
    recognizer.add_entity(entity, entity_type)
    recognizer.add_word(entity, sub_type, page_url, image_url)
recognizer.build()


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html', sent='')

    def post(self):
        sent = self.get_argument('sent')
        entities = recognizer.analyze(sent)
        print(entities)
        if entities:
            self.write(json.dumps(entities))


class NERHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index2.html', sent='', entities=[])

    def post(self):
        sent = self.get_argument('sent')
        entities = recognizer.analyze(sent)
        print(entities)
        if entities:
            self.render('index2.html', sent=sent, entities=entities['entities'])
            # self.write(json.dumps(entities))


BASE_DIR = os.path.dirname(__file__)


def main():
    application = tornado.web.Application([
        url(r'/', MainHandler),
        url(r'/ner', NERHandler, name='ner'),
    ],
        template_path=os.path.join(BASE_DIR, 'templates'),
        static_path=os.path.join(BASE_DIR, 'static'),
    )
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get('PORT', 8000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()