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
LOCAL_STORAGE_FILE_NAME = 'local-storage.pkl'
NO_SLOT_PATTERN = 'No delivery windows available. New windows are released throughout the day.'
NEXT_SLOT_EL_ID = 'delivery-slot-form'

LOGGER = logging.getLogger('wf-slot')
console_hdlr = logging.StreamHandler()
console_hdlr.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] ' +
                                            '%(message)s', '%Y-%m-%d %H:%M:%S'))
LOGGER.addHandler(console_hdlr)
LOGGER.setLevel(logging.DEBUG)


class LocalStorage:
    """ Local storage access class from this Stack Overflow answer: https://stackoverflow.com/a/46361900
    """
    def __init__(self, driver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()

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
        local_storage = LocalStorage(driver)

        # Load cookies from previous session
        if os.path.isfile(COOKIES_FILE_NAME):
            for cookie in pickle.load(open(COOKIES_FILE_NAME, 'rb')):
                driver.add_cookie(cookie)
            LOGGER.info("Loaded cookies from {} from last session"
                        .format(COOKIES_FILE_NAME))

        # Load local storage from previous session
        if os.path.isfile(LOCAL_STORAGE_FILE_NAME):
            items = pickle.load(open(LOCAL_STORAGE_FILE_NAME, 'rb'))
            for key in items:
                local_storage.set(key, items[key])
            LOGGER.info("Loaded local storage from {} from last session"
                        .format(LOCAL_STORAGE_FILE_NAME))

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

        # Save local storage for future use
        pickle.dump(local_storage.items(), open(LOCAL_STORAGE_FILE_NAME, 'wb'))
        LOGGER.info("Saved local storage in {} for future use"
                    .format(LOCAL_STORAGE_FILE_NAME))

        # Refresh site every so often until a slot opens
        no_open_slots = True

        while no_open_slots:
            # Wait random time before refreshing
            refresh_delay = random.randrange(20, 30) + (random.randrange(10, 100) / 1000)
            LOGGER.info("Refreshing in {}".format(refresh_delay))
            time.sleep(refresh_delay)

            driver.refresh()

            # Parse HTML
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, features='html.parser')

            # Inspect slot selector element
            try:
                next_slot_text = soup.find(id=NEXT_SLOT_EL_ID).text

                if NO_SLOT_PATTERN not in next_slot_text:
                    no_open_slots = False
                    on_slots_open()
                else:
                    LOGGER.info("No slots available")
            except AttributeError:
                LOGGER.info("Could not find slot selection element")
                continue
    except KeyboardInterrupt:
        driver.quit()
        LOGGER.info("Exited")

wait_for_slots(START_URL)


