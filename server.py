"this server.py is for startting the service"

import os
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define, options

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from check_code import CheckCode

# server port
define("port", default=19191, help="run on the given port", type=int)

reload(sys)
sys.setdefaultencoding('utf-8')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        pass

class CheckCodeHandler(tornado.web.RequestHandler):
    def post(self):
        check_code = CheckCode()
        code_img, code_str = check_code.create_check_code();
        print(code_img, code_str)
        mstream = StringIO.StringIO()
        img = code_img
        img.save(mstream, "jpeg")
        #code_img.save("static/images/%s.gif" % rand, "gif")
        #self.redirect("static/images/%s.gif" % rand)
        self.write(mstream.getvalue())

    def get(self, *args, **kwargs):
        self.post()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/code", CheckCodeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
