import bs4

from selenium import webdriver

import sys
import time
import os
import random

NO_SLOT_PATTERN = 'No delivery windows available. New windows are released throughout the day.'
NEXT_SLOT_EL_ID = 'delivery-slot-form'

def on_slots_open():
    print("Slots open")
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

        # Wait for user to login
        print("Please do the following:")
        print("1. Login to the Whole Foods website")
        print("2. Select items")
        print("3. Procede to the checkout page")
        print("Press [ENTER] when you reach the select time slot page")
        input()

        # Refresh site every so often until a slot opens
        no_open_slots = True

        while no_open_slots:
            # Wait random time before refreshing
            refresh_delay = random.randrange(20, 30) + (random.randrange(10, 100) / 1000)
            print("Refreshing in {}".format(refresh_delay))
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
                    print("No slots available")
            except AttributeError:
                print("Could not find slot selection element")
                continue
    except KeyboardInterrupt:
        driver.quit()
        print("Exited")

wait_for_slots('https://primenow.amazon.com/checkout/enter-checkout?merchantId=A60EDBF48VWF4&ref=pn_sc_ptc_bwr&siteState=clientContext%3D139-2884847-4954330%2CsourceUrl%3Dhttps%253A%252F%252Fprimenow.amazon.com%252Fcheckout%252Fenter-checkout%253FmerchantId%253DA60EDBF48VWF4%2526ref%253Dpn_sc_ptc_bwr%2Csignature%3DyxVgpUj2BTjSBczxFa3HZKaH8oJjgj3D&openid.assoc_handle=amzn_houdini_desktop_us&openid.claimed_id=https%3A%2F%2Fprimenow.amazon.com%2Fap%2Fid%2Famzn1.account.AGPB7XCY7Q5US7ARDHMA43FD7OYQ&openid.identity=https%3A%2F%2Fprimenow.amazon.com%2Fap%2Fid%2Famzn1.account.AGPB7XCY7Q5US7ARDHMA43FD7OYQ&openid.mode=id_res&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.op_endpoint=https%3A%2F%2Fprimenow.amazon.com%2Fap%2Fsignin&openid.response_nonce=2020-04-04T18%3A13%3A28Z1384691716231590270&openid.return_to=https%3A%2F%2Fprimenow.amazon.com%2Fcheckout%2Fenter-checkout%3FmerchantId%3DA60EDBF48VWF4%26ref%3Dpn_sc_ptc_bwr%26siteState%3DclientContext%253D139-2884847-4954330%252CsourceUrl%253Dhttps%25253A%25252F%25252Fprimenow.amazon.com%25252Fcheckout%25252Fenter-checkout%25253FmerchantId%25253DA60EDBF48VWF4%252526ref%25253Dpn_sc_ptc_bwr%252Csignature%253DyxVgpUj2BTjSBczxFa3HZKaH8oJjgj3D&openid.signed=assoc_handle%2Cclaimed_id%2Cidentity%2Cmode%2Cns%2Cop_endpoint%2Cresponse_nonce%2Creturn_to%2Cns.pape%2Cpape.auth_policies%2Cpape.auth_time%2Csigned&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.auth_policies=http%3A%2F%2Fschemas.openid.net%2Fpape%2Fpolicies%2F2007%2F06%2Fnone&openid.pape.auth_time=2020-04-04T18%3A13%3A28Z&openid.sig=tyxlj76%2FBeJPizhiqjRWLcqFizIPZjnXoAwOOnOqa1s%3D&serial=&')


