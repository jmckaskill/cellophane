
import os
import sys
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape

PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(PATH, 'static')

escape = tornado.escape.xhtml_escape
json = tornado.escape.json_encode


class Handler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.color = '#2aa198'
        self.on_create()

    def on_message(self, message):
        self.on_receive(message)

    def on_close(self):
        self.on_destroy()
        
    def on_create(self):
        pass
        
    def on_receive(self, message):
        pass
        
    def on_destroy(self):
        pass
        
    def destroy(self):
        self.close()

    def write(self, string, color=None):
        string = string.replace('\n', '<br>')
        color = color or self.color
        message = dict(cmd='write', message=string, color=color) 
        message = json(message)
        self.write_message(message)

    def writeline(self, string, color=None):
        self.write(string + '\n', color)
    
    def set_color(self, color):
        self.color = color
        
    def set_input_color(self, color):
        message = dict(cmd='set input color', color=color)
        message = json(message)
        self.write_message(message)
    
    def set_output_background_color(self, color):
        message = dict(cmd='set output background color', color=color)
        message = json(message)
        self.write_message(message)
        
    def set_input_background_color(self, color):
        message = dict(cmd='set input background color', color=color)
        message = json(message)
        self.write_message(message)
        
    def set_separator_color(self, color):
        message = dict(cmd='set separator color', color=color)
        message = json(message)
        self.write_message(message)
    
    def set_password_mode(self, on):
        if on:
            message = dict(cmd='set password on')
        else:
            message = dict(cmd='set password off')
        message = json(message)
        self.write_message(message)
    


class WebHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        self.template_items = kwargs
    def get(self):
        self.render(os.path.join(PATH, "cellophane.html"), **self.template_items)


class Cellophane:

    def __init__(self, client_class=Handler, hostname='localhost', port='8888', 
                 favicon_path=STATIC_PATH, title='cellophane', debug=True):
        self.client_class = client_class
        self.hostname = hostname
        self.port = port
        self.favicon_path = favicon_path
        self.title = title
        self.debug = debug
        
    def periodic(self, function, time):
        tornado.ioloop.PeriodicCallback(function, time).start()
    
    def go(self):
        handlers = [
            (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': self.favicon_path}),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
            (r'/', WebHandler, dict(hostname=self.hostname, port=self.port, title=self.title)),
            (r'/ws', self.client_class)
        ]
        application = tornado.web.Application(handlers, debug=self.debug)
        application.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()

        
        
        
    
        
        
        

    
    
    
    
    
    
    
    
    
    
    
    