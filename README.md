# Whole Foods Delivery Slot
Automatically checks for Whole Foods delivery slots.

# Table Of Contents
- [Overview](#overview)
- [Usage](#usage)

# Overview
A fork of [@pcomputo 's Whole Foods delivery slot script](https://github.com/pcomputo/Whole-Foods-Delivery-Slot).

The spirit of the original was kept and mind and additional features were added:

- Web interface
- Open slot notification via phone call
- Automated cart management

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

## Run
Start Redis listening on `localhost:6379` (used to persist data). If you do not
have Redis install you can run it in a container:

```
./redis-server start
```

This script uses [`podman`](https://podman.io/). To use a different container 
client set the `CONTAINER_CLI` environment variable.

Start the server:

```
pipenv shell
./server.py
```

Navigate to [localhost:8000](http://localhost:8000) and follow instructions.

A command line interface is also available:

```
pipenv shell
./cli.py -h
```

See the help message for available commands.
