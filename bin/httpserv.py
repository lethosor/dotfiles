#!/usr/bin/env python-system
import os.path
import mimetypes

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import sys

class FileHandler(tornado.web.RequestHandler):
    def get(self, path):
        if not path:
            path = 'index.html'

        if not os.path.exists(path):
            raise tornado.web.HTTPError(404)

        mime_type = mimetypes.guess_type(path)
        self.set_header("Content-Type", mime_type[0] or 'text/plain')

        print('send %s' % path)
        outfile = open(path, 'rb')
        for line in outfile:
            self.write(line)
        self.finish()
        print('done')

def main():
    # tornado.options.enable_pretty_logging()
    application = tornado.web.Application([
        (r"/(.*)", FileHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(dict(enumerate(sys.argv)).get(1, 8000))
    print('Listening on port %i' % port)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
