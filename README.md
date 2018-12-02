##Tinderbot
#About
Shoutout to fbessez and rtt for the Tinder API documentation 

In the time it took me to write this, tinder changed it's endpoint hostname as well as the json nesting structure that returned user recommendation data for my particular user account. Not sure if it was because I was hammering its servers indiscriminately at first or whether it was just coincidence. Either way, try to rate limit your queries with the pause() function.

##Quickstart
#CLI mode with Docker
By far the quickest way to get started. User inputs paramters interactively

'''
docker build -t tinderbot .
docker run -it tinderbot
'''

#To run with native python:
1. pip install requirements.txt
(or)
pip install robobrowser requests bs4 config tinydb lxml
2. python3 main.py
3. If you want to use 'silent mode' (headless autorun), rename the config file to config.py and populate with your user credentials. Run with   python3 main.py s
Optionally, you can specify how many runs to go for before stopping:
python3 main.py s 15

no warranty, for educational use only
