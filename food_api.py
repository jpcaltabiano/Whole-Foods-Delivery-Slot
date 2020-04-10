""" HTTP API related functionality.
"""

import requests

class FoodAPI:
    """ Client which uses the Amazon food API directly.
    Fields:
    - headers: Headers to be included in every request
    - cookies: Amazon session cookies
    - logger: Displays messages to user

    The API cart object has the following notable keys:
    - customerState (map):
      - customerCanCheckout (bool)
      - customerAccessType (str): All caps, either "PRIME" or "GUEST"
    - cartSummary (map):
      - totalQuantity (int)
    - activeItemList (List[map]):
      - ASIN (str): Amazon standard identification number
      - itemID (str): ID of specific item in stock (guess)
      - offerID (str): ID of price offer (guess)
      - quantity (int)
      - stockOnHand (int)
      - merchantID (str): ID of seller
      - isToBeGiftWrapped (bool)
      - isReplaceable (bool)
    - cartErrors(map)
    - Top level key exists for each merchantID (map):
      - merchantCart (map):
        - subtotalAmount (float)
        ... Various fields summerizing cart for merchant ...
    """

    GET_CART_URL = 'https://primenow.amazon.com/cart/ajax/'

    ADD_ITEM_URL = 'https://primenow.amazon.com/cart/ajax/additem/\
                   ref=pn_dp_bb_atc?itemAsin={asin}&offerId={offer_id}&\
                   qid=0&quantity={quantity}'

    def __init__(self, logger):
        """ Creates a new client.
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
        }

        self.cookies = {}
        self.logger = logger

    def set_credentials(self, browser_api):
        """ Stores session credential cookies from the browser. Used to make
        authenticated HTTP requests.

        Arguments:
        - browser_api: Used to retrieve authentication cookies
        """
        for cookie in browser_api.driver.get_cookies():
            self.cookies[cookie['name']] = cookie['value']

    def get_cart(self):
        """ Retrieves the current cart.
        Raises:
        - IOError: If request was not a success
        Returns: A cart object
        """
        resp = requests.get(self.GET_CART_URL,
                            cookies=self.cookies,
                            headers=self.headers)
        if resp.status_code != 200:
            raise IOError("Received non-OK response, status code={}, text={}"
                          .format(resp.status_code, resp.text))

        return resp.json()

    def add_cart_item(self, asin, offer_id, quantity):
        """ Add an item to the cart.
        Arguments:
        - asin (str): Amazon standard identification number of product
        - offer_id (str): ID of merchant's offer on product
        - quantity (int): Number of items to add

        Raises:
        - IOError: If fails to add item to cart
        """
        resp = requests.get(self.ADD_ITEM_URL.format(asin=asin,
                                                     offer_id=offer_id,
                                                     quantity=quantity),
                            cookies=self.cookies,
                            headers=self.headers)
        if resp.status_code != 200:
            raise IOError("Received non-OK response, status code={}, text={}"
                          .format(resp.status_code, resp.text))
