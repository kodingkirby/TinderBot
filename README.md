# Tinderbot
>Likes people. A lot of people. 

![screenshot](docs/screenshots/screenshot1.png)

## Installation

OS X & Linux with Docker:

'''sh
docker build -t tinderbot .
docker run -it tinderbot
'''

This probably works on Windows too, just haven't tested it yet.

Native Python3:
'''sh
pip install robobrowser requests bs4 config tinydb lxml
python3 main.py
'''
## Quickstart

Once you launch the app, you'll be prompted for credentials. Type in the email address and password associated with your Facebook account. These are used by a robobrowser script to retrieve an Oauth token from Facebook to use with Tinder.

Once authenticated, you can start the autoliker.

![screenshot](docs/screenshots/screenshot2.png)


## Silent Mode
TinderBot has the capability to stay on in the background, liking people throughout the day. By default, the bot will wait 20-40 minutes between bursts of likes and will cease after 8 hours. 

_To use silent mode, you need to first rename tinder_config_ex.py to config.py and populate the username and password fields_

Run Silent Mode:
'''sh
python3 main.py s
'''

Optionally, you can specific how many 'bursts' to complete before stopping:
'''sh
python3 main.py s 15
'''

A burst value of 999 will run perpetually:
'''sh
python3 main.py 999
'''


This app carries no warranty, and is for educational use only
