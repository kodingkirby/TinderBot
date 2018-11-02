print('..loading')
import tinder_api
import fb_auth_token
import config
import features
from bs4 import BeautifulSoup
#system UI calls
import getpass
import sys
from os import system, name  #for clear screen
from time import sleep
#Db
from tinydb import TinyDB, Query
#If u wanna automate...
#fb_username = config.fb_username
#fb_password = config.fb_password


#Holds auth tokens and db state
class Session:
    def __init__ (self, fb_username, fb_password):
        self.fb_access_token = fb_auth_token.get_fb_access_token(fb_username, fb_password)
        self.fb_user_id = fb_auth_token.get_fb_id(self.fb_access_token)
        self.tinder_auth_token = tinder_api.get_auth_token(self.fb_access_token, self.fb_user_id)
        print('fb_access_token:')
        print(self.fb_access_token)
        print('fb_user_id:')
        print(self.fb_user_id)
        print('tinder_auth_token')
        print(self.tinder_auth_token)
        sleep(1)
        print('Login successful ✅')
        sleep(3)
   
    def check_auth(self):
        print('fb_access_token:')
        print(self.fb_access_token)
        print('fb_user_id:')
        print(self.fb_user_id)
        print('tinder_auth_token')
        print(self.tinder_auth_token)

    #DB Helpers
    def init_db(self):
        self.rec_db = TinyDB('user_rec_db.json')
        self.match_db = TinyDB('matches.json')
        self.updates_db = TinyDB('updates.json')

    def close_db(self):
        self.rec_db.close()
        self.updates_db.close()
        self.match_db.close()

    #Recommendation Array objects
    def set_recs(self, rec_array):
        self.recommendations = rec_array

#Tracks UI state
class UserInterface():
    def __init__(self, mode):
        self.run = True
        self.mode = mode

def clear_screen():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def get_recommendations():
    recommendations = tinder_api.get_recommendations()
    recommended_users = list((recommendations['data']['results']))
    print('Users returned: ' + str(len(recommended_users)))
    print('UserIDs: ')
    for r in recommended_users:
        print('ID: ' + r['user']['_id'] + ' Name: ' + r['user']['name']+  '      s_number: ' + str(r['s_number']))
    return recommended_users

def archive_recommendations():
    #possibly do machine learning on results with a predictor later
    User = Query()
    for r in recommended_users:
        updated_entries = rec_db.upsert(r, User.user._id == r['user']['_id'])
        print('updated ' + r['user']['name'] + ' in user_rec_db')

def autoliker(how_many_likes):
    #how_many_likes: how many people to like before stopping
    ppl_liked = 0
    User = Query()
    print('lets get this bread 🍞')
    responses = []
    #Get recs and auto like peeps, let me know if I get an instant match
    try:
        while ppl_liked <= how_many_likes:
            recommendations = tinder_api.get_recommendations()
            recommended_users = list((recommendations['data']['results']))
            new = len(recommended_users)
            print(str(new) + ' new recs, playa!')

            for r in recommended_users:
                print('Liking: ' + r['user']['name'] + ' ID: ' + r['user']['_id'])
                response = tinder_api.like(r['user']['_id'], str(r['s_number']))
                features.pause()
                sleep(4)
                features.pause()
                responses.append(response)
                #if response['match'] == True:
                #    print(r['name'] + ' matched with you!')
                #if rec_db.search(User.user._id == r['user']['_id']):
                #    print('Yo, we\'ve swiped right on this person before...')    
                #rec_db.upsert(r, User.user._id == r['user']['_id'])
                #print('Storing ' + r['user']['name'] + '\'s profile' + ' in user_rec_db')
                features.pause()
                sleep(1)
                ppl_liked += 1
    except Exception as e:
       print('yo, something broke...') 

    print('autoliker complete')
    print('ppl liked: ' + str(ppl_liked) + '  ✅')


def help_menu(list):
    counter = 0
    for l in list:
        counter += 1
        string = '[' + str(counter) + '] ' + l 
        print(string)

def cli_autoliker():
    target_likes = input('how many ppl you tryna like?: ')
    tl = int(target_likes)
    autoliker(tl)

def test_mode():
    print('testmode')

def silent_mode(fb_username, fb_password):
    target = 5
    if len(sys.argv) > 2:
        target = sys.argv[2]
    s = Session(fb_username, fb_password)
    s.init_db()
    autoliker(target)

def cli_mode():
    clear_screen()
    art = '''
     _   _           _           _           _   
    | |_(_)_ __   __| | ___ _ __| |__   ___ | |_ 
    | __| | '_ \ / _` |/ _ \ '__| '_ \ / _ \| __|
    | |_| | | | | (_| |  __/ |  | |_) | (_) | |_ 
     \__|_|_| |_|\__,_|\___|_|  |_.__/ \___/ \__|                                                                      
    '''
    print(art)
    email = input('✉️ facebook email: ')
    pswd = getpass.getpass('🔐 facebook password:')
    s = Session(email, pswd)
    s.init_db()
    #todo: database search/view
    #todo: message pickup line
    #-how many girls to message?
    #-I am going to use the pickup lines in pickup.txt
    #-
    options = ['🤖 Autoliker ', '🔑 Check Auth Tokens ', '🛠 Stealth Settings ', '❌ Quit']
    help = ''
    while ui.run:
        clear_screen()
        print('🔥 Tinderbot Main Menu 🔥')
        print()
        help_menu(options)
        print()
        opstring = input('Enter an option:')
        option = int(opstring)

        if option == 1:
            cli_autoliker()
            input('...Autoliker complete, press enter to return to main menu...')
            sleep(3)
        if option == 2:
            print(options[1])
            s.check_auth
            input('...CheckAuth complete, press enter to return to main menu...')
            sleep(3)
        if option == 3:
            print(options[2])
        if option == 4:
            print(options[3])
            s.close_db()
            ui.run = False
        else:
            print('invalid input')


#=========Main Driver===========#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if (sys.argv[1]) == 't':
            ui = UserInterface('test')
            print(ui.mode)
            test_mode()
        if (sys.argv[1] == 's'):
            ui = UserInterface('silent')
            silent_mode(config.fb_username, config.fb_password)
    else:
        ui = UserInterface('cli')
        cli_mode()


