#!/usr/bin/env python3
""" Web server.
"""
import os
import logging

import falcon
from eventlet import wsgi
import eventlet

from browser_api import BrowserAPI
from food_api import FoodAPI

class IndexPageResource:
    """ Redirects to the index.html file.
    """

    def on_get(self, req, resp):
        """ Redirect to index.html
        """
        raise falcon.HTTPMovedPermanently('/index.html')

# Setup logger
LOGGER = logging.getLogger('wf-slot')
console_hdlr = logging.StreamHandler()
console_hdlr.setFormatter(logging.Formatter(' %(asctime)s [%(levelname)s] ' +
                                            '%(name)s - %(message)s',
                                            '%Y-%m-%d %H:%M:%S'))
LOGGER.addHandler(console_hdlr)
LOGGER.setLevel(logging.DEBUG)
    
# Initialize Amazon food API clients
BROWSER_API = BrowserAPI(LOGGER)
FOOD_API = FoodAPI(LOGGER)
    
# Start server
APP = falcon.API()
APP.add_route('/', IndexPageResource())

CWD = os.path.dirname(os.path.realpath(__file__))
APP.add_static_route('/', os.path.join(CWD, './static'))

wsgi.server(eventlet.listen(('', 8000)), APP)
