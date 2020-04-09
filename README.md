# Whole Foods Delivery Slot
Automatically checks for Whole Foods delivery slots.

# Table Of Contents
- [Overview](#overview)
- [Usage](#usage)

# Overview
A fork of [@pcomputo 's Whole Foods delivery slot script](https://github.com/pcomputo/Whole-Foods-Delivery-Slot).

Modified to work specifically with the Amazon Prime Whole Foods delivery 
website. Additional modifications were made to the code.

See [the Usage section](#usage) for instructions.

# Usage
This script is geared towards more advanced users with terminal knowledge.

It has only been tested on Linux.

## Install
First download this repository and navigate to its root directory. Either using 
`git clone` or by downloading [this ZIP file](https://github.com/Noah-Huppert/Whole-Foods-Delivery-Slot/archive/master.zip)
and extracting it.

Install [Python 3](https://www.python.org/).  
Install [Pipenv](https://pipenv.pypa.io/en/latest/):

```
pip3 install pipenv
```

Install [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [geckodriver](https://github.com/mozilla/geckodriver).

Finally install this script's Python dependencies:

```
pipenv install
```

## Setup
The script will invoke another script in the repository root named 
`on-slots-open` when a Whole Foods delivery slot becomes available.

Create this file:

```
touch on-slots-open
chmod +x on-slots-open
```

Then edit this file to your liking. Remember to add a shabang at the top.

I made my script call me using [Twilio](https://www.twilio.com) when a 
slot opened:

```python
#!/usr/bin/env python3
from twilio.rest import Client

ACCOUNT_SID = 'YOUR ACCOUNT SID'
AUTH_TOKEN = 'YOUR ACCOUNT AUTH TOKEN'

FROM_PHONE_NUMBER = 'YOUR TWILIO PHONE NUMBER'
TO_PHONE_NUMBER = 'YOUR PHONE NUMBER'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

call = client.calls.create(
    twiml='<Response><Say>A Whole Foods delivery slot has become available, login to the Whole Foods Delivery site quickly to place your order!</Say></Response>',
    to=TO_PHONE_NUMBER,
    from_=FROM_PHONE_NUMBER,
)

print("Call sid={}".format(call.sid))
```

## Run
Run the script:

```
pipenv run whole_foods_delivery_slot.py
```

Then follow the instructions in the terminal.
