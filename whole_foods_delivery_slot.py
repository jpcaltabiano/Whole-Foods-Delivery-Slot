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
import logging
import argparse
import json

CHECK_CMD_NAME = 'check-slots'
SAVE_CMD_NAME = 'save-cart'

START_URL = 'https://primenow.amazon.com/'
NO_SLOT_PATTERN = 'No delivery windows available. New windows are released throughout the day.'
    
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

        # Refresh site every so often until a slot opens
        no_open_slots = True

        while no_open_slots:
            # Wait random time before refreshing
            refresh_delay = random.randrange(20, 30) +\
                            (random.randrange(10, 100) / 1000)
                             
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

    # Load cookies
    load_cookies(driver)

    # Wait for user to login
    print("Once logged in press [ENTER]")
    input()

    # Save cookies
    save_cookies(driver)

    # Create API client
    api = FoodAPI(driver)

    # Get list items
    cart = api.get_cart()

    item_details = api.get_item_details(driver, 'B074H5SRZX', 'A60EDBF48VWF4')
    logger.info("Item details={}".format(item_details))

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
console_hdlr.setFormatter(logging.Formatter(' %(asctime)s [%(levelname)s] ' +
                                            '%(name)s - %(message)s',
                                            '%Y-%m-%d %H:%M:%S'))
LOGGER.addHandler(console_hdlr)
LOGGER.setLevel(logging.DEBUG)

# Setup API clients
browser_api = 

# Run
if args.cmd == CHECK_CMD_NAME:
    sys.exit(wait_for_slots(LOGGER, START_URL))
elif args.cmd == SAVE_CMD_NAME:
    sys.exit(save_cart(LOGGER, START_URL))
