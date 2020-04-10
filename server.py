#!/usr/bin/env python3
""" Web server.
"""
import os
import logging

import falcon
from eventlet import wsgi
import eventlet
import redis

from browser_api import BrowserAPI
from food_api import FoodAPI

class IndexPageResource:
    """ Redirects to the index.html file.
    """

    def on_get(self, req, resp):
        """ Redirect to index.html
        """
        raise falcon.HTTPMovedPermanently('/index.html')
    
class ItemsResource:
    """ Manages the list of known items.
    """

    def on_get(self, req, resp):
        """ Retrieve all items.
        """
        """ TODO:
        - Make return items
        - Make cart functionality
            - Server endpoints to:
                - Search items in the cart and / or archived
                - Search for items on the Whole Foods website
                - Add an item to the cart
            - BrowserAPI methods to search Whole Foods website and list items
            - Behavior:
                - The user will first search for items already in redis
                - If the item is in redis they can add / remove it from the cart
                - If the item is not in the cart the Whole Foods website will be
                  searched for the item
                - Only the first 10-20 items will be scraped and serialized 
                  in memory
        """

# Setup logger
LOGGER = logging.getLogger('wf-slot')
console_hdlr = logging.StreamHandler()
console_hdlr.setFormatter(logging.Formatter(' %(asctime)s [%(levelname)s] ' +
                                            '%(name)s - %(message)s',
                                            '%Y-%m-%d %H:%M:%S'))
LOGGER.addHandler(console_hdlr)
LOGGER.setLevel(logging.DEBUG)

# Connect to Redis
REDIS = redis.Redis(host='localhost', port=6379, db=0)
    
# Initialize Amazon food API clients
BROWSER_API = BrowserAPI(LOGGER)
FOOD_API = FoodAPI(LOGGER)
    
# Start server
APP = falcon.API()
APP.add_route('/', IndexPageResource())

CWD = os.path.dirname(os.path.realpath(__file__))
APP.add_static_route('/', os.path.join(CWD, './static'))

wsgi.server(eventlet.listen(('', 8000)), APP)
