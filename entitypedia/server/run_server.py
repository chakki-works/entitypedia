import os
import random

import tornado.ioloop
import tornado.web
import tornado.httpserver

from entitypedia.server.trie import create_trie
BASE_DIR = os.path.dirname(__file__)
trie, entity_dic = create_trie()


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class SearchHandler(tornado.web.RequestHandler):

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        query = data["query"]
        res = trie.start_with_prefix(query)
        posts = [{'entity': e,
                  'url': entity_dic[e]['url'],
                  'score':random.random(),
                  'entity_type': entity_dic[e]['type']} for e in res]
        message = {"posts": posts}
        self.write(message)


def main():
    application = tornado.web.Application([
        (r'/', IndexHandler),
        (r"/e/search", SearchHandler),
    ],
        template_path=os.path.join(BASE_DIR, 'templates'),
        static_path=os.path.join(BASE_DIR, 'static'),
        xsrf_cookies=True,
        cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get('PORT', 8888))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
