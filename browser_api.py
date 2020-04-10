import os
import pickle
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BrowserAPI:
    """ Client which uses the browser to access the Amazon food website.
    Fields:
    - driver: Web driver
    - logger: Displays messages to use
    """

    COOKIES_FILE_NAME = 'cookies.pkl'

    ITEM_PAGE_URL = 'https://primenow.amazon.com/dp/{asin}?qid=0&m={mid}'
    ITEM_PAGE_NAME_EL = '//*[@id="productTitle"]'
    ITEM_PAGE_IMAGE_EL = '//*[@id="landingImage"]'
    ITEM_PAGE_PRICE_EL = '//*[@id="priceblock_ourprice"]'
    ITEM_PAGE_ADD_CART_EL = '//*[@id="atc-declarative"]'

    def __init__(self, logger):
        """ Creates a new BrowserAPI. Starts a new web driver browser session.
        """
        self.driver = webdriver.Firefox()
        self.logger = logger

    def load_cookies(self):
        """ Loads cookies from a file and sets them in the current browser.
        """
        if os.path.isfile(self.COOKIES_FILE_NAME):
            for cookie in pickle.load(open(self.COOKIES_FILE_NAME, 'rb')):
                self.driver.add_cookie(cookie)

    def save_cookies(self):
        """ Saves browser cookies for future use in a file.
        """
        pickle.dump(self.driver.get_cookies(), open(self.COOKIES_FILE_NAME, 'wb'))

    def ensure_document_ready(self, timeout=10):
        """ Ensures that the current page has finished loading.
        Arguments:
        - timeout (int): Number of seconds to wait before action times out
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def get_element(self, xpath, timeout=10):
        """ Gets an element from the page.
        Arguments:
        - xpath: XPATH of element to click
        - timeout (int): Number of seconds to wait before action times out

        Returns: Element selected by XPATH
        """
        return WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )

    def click(self, xpath, timeout=10):
        """ Clicks on an element based on the XPATH.
        Arguments:
        - xpath: XPATH of element to click
        - timeout (int): Number of seconds to wait before action times out
        """
        el = self.get_element(xpath, timeout=timeout)

        el.click()

    def ensure_url_contains(self, url_part, timeout=10):
        """ Ensures that the current page URL contains url_part.
        Arguments:
        - url_part: Portion of URL which must be present
        - timeout (int): Number of seconds to wait before action times out
        """
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_part)
        )

    def get_item_details(self, asin, mid):
        """ Go to item web page and gather details.
        Arguments:
        - asin (str): Amazon standard identification number of product
        - mid (str): Merchant ID of product sellder

        Returns: dict with keys:
        - asin (str)
        - mid (str)
        - name (str)
        - image_url (str)
        - price (int)
        - offer_id (str)
        """
        # Navigate to item page
        self.driver.get(self.ITEM_PAGE_URL.format(asin=asin, mid=mid))

        # Extract information
        info = {
            'asin': asin,
            'mid': mid,
        }

        name_el = get_element(driver, self.ITEM_PAGE_NAME_EL)
        image_el = get_element(driver, self.ITEM_PAGE_IMAGE_EL)
        price_el = get_element(driver, self.ITEM_PAGE_PRICE_EL)
        add_cart_el = get_element(driver, self.ITEM_PAGE_ADD_CART_EL)

        info['name'] = name_el.text
        info['image_url'] = image_el.get_attribute('src')
        info['price'] = float(price_el.text.replace('$', ''))
        info['offer_id'] = json.loads(add_cart_el
            .get_attribute('data-primenow-atc'))['inputs']['offerListingID']

        return info
