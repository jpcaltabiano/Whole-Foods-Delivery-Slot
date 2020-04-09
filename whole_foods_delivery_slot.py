#!/usr/bin/env python3
import bs4
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import time
import os
import random
import pickle
import logging
import argparse
import urllib

 # Maximum number of seconds to wait for an element
MAX_DRIVER_WAIT = 10

CHECK_CMD_NAME = 'check-slots'
SAVE_CMD_NAME = 'save-chart'

START_URL = 'https://primenow.amazon.com/'
CART_URL_PART = '/cart'
CHECKOUT_URL_PART = '/checkout'

COOKIES_FILE_NAME = 'cookies.pkl'

CART_BUTTON_XPATH = '//*[@aria-label="Cart"]/..' # Parent of link
NO_SUB_BUTTON_XPATH = '//*[@text="Leave out all unavailable items"]'
CHECKOUT_BUTTON_XPATH = '//a[@href="{}*"]'.format(CHECKOUT_URL_PART)

NO_SLOT_PATTERN = 'No delivery windows available. New windows are released throughout the day.'

def new_driver():
    """ Initializes browser driver.
    If cookies from a previous session are saved they will be loaded.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }

    driver = webdriver.Firefox()

    return driver

def load_cookies(driver):
    """ Loads browser cookies from file.
    Arguments:
    - driver: Web driver
    """
    if os.path.isfile(COOKIES_FILE_NAME):
        for cookie in pickle.load(open(COOKIES_FILE_NAME, 'rb')):
            driver.add_cookie(cookie)

def save_cookies(driver):
    """ Saves browser cookies for future use.
    Arguments:
    - driver: Browser driver
    """
    # Save cookies for future use
    pickle.dump(driver.get_cookies(), open(COOKIES_FILE_NAME, 'wb'))

def expect_condition_document_ready(driver):
    """ A custom selenium expect condition which ensures that a web page's
    document has completed loading.
    Arguments:
    - driver: Web driver

    Returns: True if document is completed loading, false otherwise.
    """
    return driver.execute_script("return document.readyState") == "complete"

def ensure_document_ready(driver):
    """ Ensures that the current page has finished loading
    Arguments:
    - driver: Web driver

    Raises:
    - selenium.common.exceptions.TimeoutException: If item cannot be located within
      MAX_DRIVER_WAIT seconds
    - Any other exception the selenium the WebDriverWait.until() or 
      execute_script() methods can raise
    """
    WebDriverWait(driver, MAX_DRIVER_WAIT).until(
        expect_condition_document_ready
    )

def get_element(driver, xpath):
    """ Gets an element from the page.
    Arguments:
    - driver: Web driver
    - xpath: XPATH of element to click
    
    Raises:
    - selenium.common.exceptions.TimeoutException: If item cannot be located within
      MAX_DRIVER_WAIT seconds
    - Any other exception the selenium the WebDriverWait.until() method can raise

    Returns: Element selected by XPATH
    """
    return WebDriverWait(driver, MAX_DRIVER_WAIT).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)
        )
    )

def click(driver, xpath):
    """ Clicks on an element based on the XPATH
    Arguments:
    - driver: Web driver
    - xpath: XPATH of element to click
    
    Raises:
    - selenium.common.exceptions.TimeoutException: If item cannot be located within
      MAX_DRIVER_WAIT seconds
    - Any other exception the selenium the WebDriverWait.until() or element 
      click() methods can raise
    """
    el = get_element(driver, xpath)
    
    el.click()

def ensure_url_contains(driver, url_part):
    """ Ensures that the current page URL contains url_part
    Arguments:
    - driver: Web driver
    - url_part: Portion of URL which must be present
    
    Raises:
    - selenium.common.exceptions.TimeoutException: If URL does not have url_part
      within MAX_DRIVER_WAIT seconds
    - Any other exception the selenium WebDriverWait.until() method can raise
    """
    WebDriverWait(driver, MAX_DRIVER_WAIT).until(
        EC.url_contains(url_part)
    )

def navigate_to_cart(driver):
    """ Navigates to the cart page from homepage.
    Arguments:
    - driver: Web driver
    """
    # Click on cart button
    click(driver, CART_BUTTON_XPATH)

    # Check URL is correct
    ensure_url_contains(driver, CART_URL_PART)

def navigate_to_checkout(driver):
    """ Navigates to the checkout page from homepage.
    Arguments:
    - driver: Web driver
    """
    # Go to cart page
    navigate_to_cart(driver)
    print("navigated to cart")

    ensure_document_ready(driver)

    # Click no substitutions button
    click(driver, NO_SUB_BUTTON_XPATH)
    print("clicked no sub button")

    # Navigate to checkout page
    click(driver, CHECKOUT_BUTTON_XPATH)
    print("clicked checkout button")

    # Check URL is correct
    ensure_url_contains(driver, CHECKOUT_URL_PART)
    
def on_slots_open(logger):
    """ Callback run when delivery slots are open.
    Arguments:
    - logger: Displays output to user
    """
    logger.info("Slots open")
    os.system('./on-slots-open')

def wait_for_slots(logger, start_url):
    """ Continuously checks for delivery slots.
    Arguments:
    - logger: Displays output to user
    - start_url: Homepage URL of Whole Foods website

    Returns: Process exit code
    """
    try:
        # Initialize browser
        driver = new_driver()
        driver.get(start_url)

        # Load cookies
        load_cookies(driver)

        # Wait for user to login
        logger.info("Please login to Whole Foods, then press [ENTER]")
        input()

        # Save cookies for future use
        save_cookies(driver)

        # Navigate to checkout page
        try:
            navigate_to_checkout(driver)
        except ValueError as e:
            logger.fatal("Failed to navigate to cart page: {}".format(e))
            return 1

        return 0

        # Refresh site every so often until a slot opens
        no_open_slots = True

        while no_open_slots:
            # Wait random time before refreshing
            refresh_delay = random.randrange(20, 30) + (random.randrange(10, 100) / 1000)
            logger.info("Refreshing in {}".format(refresh_delay))
            time.sleep(refresh_delay)

            driver.refresh()

            # Inspect slot selector element
            html = driver.page_source
            
            try:
                if NO_SLOT_PATTERN in html:
                    logger.info("No slots available")
                else:
                    no_open_slots = False
                    on_slots_open(logger)
            except AttributeError:
                logger.info("Could not find slot selection element")
                continue
    except KeyboardInterrupt:
        driver.quit()
        logger.info("Exited")

    return 0

def save_cart(logger, start_url):
    """ Save current cart to a file for later use.
    Arguments:
    - logger: Displays messages to user
    - start_url: Homepage to start process

    Returns: Process exit code
    """
    # Initialize browser
    driver = new_driver()
    driver.get(start_url)

    return 0

# Parse arguments
parser = argparse.ArgumentParser(description='Automatically checks for Whole '+
                                 'Foods delivery slots')
subparsers = parser.add_subparsers(help='Action to perform',
                                   dest='cmd')

check_parser = subparsers.add_parser(CHECK_CMD_NAME,
                                     help='Check for open delivery slots')
check_parser.add_argument('--restock-cart',
                          action='store_true',
                          help='Restock cart as items are taken off')

save_parser = subparsers.add_parser(SAVE_CMD_NAME,
                                    help='Save items currently in the cart. '+
                                    'These items can automatically be added '+
                                    'back to the cart when running the '+
                                    '"check-slots" command with the '+
                                    '--restock-cart option')

args = parser.parse_args()

if args.cmd is None: # Default to check command
    args.cmd = CHECK_CMD_NAME

# Setup logger
LOGGER = logging.getLogger('wf-slot')
console_hdlr = logging.StreamHandler()
console_hdlr.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] ' +
                                            '%(message)s', '%Y-%m-%d %H:%M:%S'))
LOGGER.addHandler(console_hdlr)
LOGGER.setLevel(logging.DEBUG)

# Run
if args.cmd == CHECK_CMD_NAME:
    sys.exit(wait_for_slots(LOGGER, START_URL))
elif args.cmd == SAVE_CMD_NAME:
    sys.exit(save_cart(LOGGER, START_URL))
