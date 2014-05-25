import uuid
import sys

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import Flask, render_template

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import (WebSocketResource,
                                       WSGIRootResource,
                                       HTTPChannelHixie76Aware)

from protocol import MyServerProtocol

# WSGI Flask based application
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

    app.debug = debug

    # create a Twisted Web resource for our WebSocket server
    wsFactory = WebSocketServerFactory("ws://localhost:8080",
                                       debug=debug,
                                       debugCodePaths=debug)

    wsFactory.protocol = MyServerProtocol
    wsFactory.setProtocolOptions(allowHixie76=True)  # needed if Hixie76 is to be supported

    wsResource = WebSocketResource(wsFactory)

    # create a Twisted Web WSGI resource for our Flask server
    wsgiResource = WSGIResource(reactor,
                                reactor.getThreadPool(),
                                app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource,
                                    {'ws': wsResource})

    # create a Twisted Web Site and run everything
    site = Site(rootResource)
    site.protocol = HTTPChannelHixie76Aware  # needed if Hixie76 is to be supported

    reactor.listenTCP(8080, site)
    reactor.run()