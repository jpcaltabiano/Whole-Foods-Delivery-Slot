#!/usr/bin/env python3
import bs4
from selenium import webdriver

import sys
import time
import os
import random
import pickle
import logging

START_URL = 'https://primenow.amazon.com/cart?ref_=pn_sf_nav_cart'
COOKIES_FILE_NAME = 'cookies.pkl'
NO_SLOT_PATTERN = 'No delivery windows available. New windows are released throughout the day.'

LOGGER = logging.getLogger('wf-slot')
console_hdlr = logging.StreamHandler()
console_hdlr.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] ' +
                                            '%(message)s', '%Y-%m-%d %H:%M:%S'))
LOGGER.addHandler(console_hdlr)
LOGGER.setLevel(logging.DEBUG)

def on_slots_open():
    LOGGER.info("Slots open")
    os.system('./on-slots-open')

def wait_for_slots(productUrl):
    try:
        # Initialize browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }

        driver = webdriver.Firefox()
        driver.get(productUrl)           
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, features='html.parser')

        # Load cookies from previous session
        if os.path.isfile(COOKIES_FILE_NAME):
            for cookie in pickle.load(open(COOKIES_FILE_NAME, 'rb')):
                driver.add_cookie(cookie)
            LOGGER.info("Loaded cookies from {} from last session"
                        .format(COOKIES_FILE_NAME))

        # Wait for user to login
        LOGGER.info("Please do the following:")
        LOGGER.info("1. Login to the Whole Foods website")
        LOGGER.info("2. Select items")
        LOGGER.info("3. Procede to the checkout page")
        LOGGER.info("Press [ENTER] when you reach the select time slot page")
        input()

        # Save cookies for future use
        pickle.dump(driver.get_cookies(), open(COOKIES_FILE_NAME, 'wb'))
        LOGGER.info("Saved cookies into {} for future use"
                    .format(COOKIES_FILE_NAME))

        # Refresh site every so often until a slot opens
        no_open_slots = True

        while no_open_slots:
            # Wait random time before refreshing
            refresh_delay = random.randrange(20, 30) + (random.randrange(10, 100) / 1000)
            LOGGER.info("Refreshing in {}".format(refresh_delay))
            time.sleep(refresh_delay)

            driver.refresh()

            # Inspect slot selector element
            html = driver.page_source
            
            try:
                if NO_SLOT_PATTERN in html:
                    LOGGER.info("No slots available")
                else:
                    no_open_slots = False
                    on_slots_open()
            except AttributeError:
                LOGGER.info("Could not find slot selection element")
                continue
    except KeyboardInterrupt:
        driver.quit()
        LOGGER.info("Exited")

wait_for_slots(START_URL)


