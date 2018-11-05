print('..loading')
import tinder_api
import fb_auth_token
import config
import features
from random import random
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
#import Image
import os
#from PIL import Image
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
    target_likes = input('how many ppl you tryna like? (try 0): ')
    tl = int(target_likes)
    autoliker(tl)

def test_mode():
    print('testmode')
    person = {'status': 200,
 'results': {'connection_count': 726,
  'common_like_count': 0,
  'common_friend_count': 0,
  'common_likes': [],
  'common_friends': [],
  '_id': '582e6c5299fd24862e3d3e0d',
  'bio': "- Animal Lover\n- Proud mother of a dog and a cat💕.\n- 5' Latina. \n- Obviously not skinny.🐷\n- Pizza is lifeeeeee 🍕\n- p a n s e x u a l 🌈 🦄\n- Clinical Medical Assistant💉.\n- Piercings & tattoos\n- Hablo español (idioma nativo) 🇲🇽\n- vámonos de rumba a Tijuana 🍻💃\n- Disneyland AP holder 👸🏼\n\nBtw my hair is red now 🤷🏼\u200d♀️\n\n-  Let’s date or whatever?😏🔥",
  'birth_date': '1994-11-03T08:17:22.352Z',
  'name': 'Isabel',
  'ping_time': '2014-12-09T00:00:00.000Z',
  'photos': [{'id': 'cd52ea22-4191-48c5-ac0a-b419db2be864',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1350_cd52ea22-4191-48c5-ac0a-b419db2be864.jpg',
    'fileName': 'cd52ea22-4191-48c5-ac0a-b419db2be864.mp4',
    'extension': 'jpg',
    'main': True,
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_cd52ea22-4191-48c5-ac0a-b419db2be864.jpg',
      'height': 800,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_cd52ea22-4191-48c5-ac0a-b419db2be864.jpg',
      'height': 400,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x216_cd52ea22-4191-48c5-ac0a-b419db2be864.jpg',
      'height': 216,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x106_cd52ea22-4191-48c5-ac0a-b419db2be864.jpg',
      'height': 106,
      'width': 84}],
    'processedVideos': [{'height': 800,
      'width': 640,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_cd52ea22-4191-48c5-ac0a-b419db2be864.mp4'},
     {'height': 600,
      'width': 480,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/480x600_cd52ea22-4191-48c5-ac0a-b419db2be864.mp4'},
     {'height': 400,
      'width': 320,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_cd52ea22-4191-48c5-ac0a-b419db2be864.mp4'}]},
   {'id': '4c9e8608-9662-403e-83dc-b8f050e86a4c',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1350_4c9e8608-9662-403e-83dc-b8f050e86a4c.jpg',
    'fileName': '4c9e8608-9662-403e-83dc-b8f050e86a4c.jpg',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_4c9e8608-9662-403e-83dc-b8f050e86a4c.jpg',
      'height': 800,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_4c9e8608-9662-403e-83dc-b8f050e86a4c.jpg',
      'height': 400,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x216_4c9e8608-9662-403e-83dc-b8f050e86a4c.jpg',
      'height': 216,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x106_4c9e8608-9662-403e-83dc-b8f050e86a4c.jpg',
      'height': 106,
      'width': 84}]},
   {'id': '84c66e3a-29dd-4367-8c3c-d389b7816f92',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1350_84c66e3a-29dd-4367-8c3c-d389b7816f92.jpg',
    'fileName': '84c66e3a-29dd-4367-8c3c-d389b7816f92.jpg',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_84c66e3a-29dd-4367-8c3c-d389b7816f92.jpg',
      'height': 800,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_84c66e3a-29dd-4367-8c3c-d389b7816f92.jpg',
      'height': 400,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x216_84c66e3a-29dd-4367-8c3c-d389b7816f92.jpg',
      'height': 216,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x106_84c66e3a-29dd-4367-8c3c-d389b7816f92.jpg',
      'height': 106,
      'width': 84}]},
   {'id': '102399ef-0b3c-4179-a62b-56bcfaa2aa07',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1080_102399ef-0b3c-4179-a62b-56bcfaa2aa07.jpg',
    'fileName': '102399ef-0b3c-4179-a62b-56bcfaa2aa07.jpg',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x640_102399ef-0b3c-4179-a62b-56bcfaa2aa07.jpg',
      'height': 640,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x320_102399ef-0b3c-4179-a62b-56bcfaa2aa07.jpg',
      'height': 320,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x172_102399ef-0b3c-4179-a62b-56bcfaa2aa07.jpg',
      'height': 172,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x84_102399ef-0b3c-4179-a62b-56bcfaa2aa07.jpg',
      'height': 84,
      'width': 84}]},
   {'id': '140f1004-bdeb-4513-9242-d46ee78660e3',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1080_140f1004-bdeb-4513-9242-d46ee78660e3.jpg',
    'fileName': '140f1004-bdeb-4513-9242-d46ee78660e3.jpg',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x640_140f1004-bdeb-4513-9242-d46ee78660e3.jpg',
      'height': 640,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x320_140f1004-bdeb-4513-9242-d46ee78660e3.jpg',
      'height': 320,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x172_140f1004-bdeb-4513-9242-d46ee78660e3.jpg',
      'height': 172,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x84_140f1004-bdeb-4513-9242-d46ee78660e3.jpg',
      'height': 84,
      'width': 84}]},
   {'id': '1e7be5dd-5027-4ccf-a23c-20489944dd22',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1350_1e7be5dd-5027-4ccf-a23c-20489944dd22.jpg',
    'fileName': '1e7be5dd-5027-4ccf-a23c-20489944dd22.mp4',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_1e7be5dd-5027-4ccf-a23c-20489944dd22.jpg',
      'height': 800,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_1e7be5dd-5027-4ccf-a23c-20489944dd22.jpg',
      'height': 400,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x216_1e7be5dd-5027-4ccf-a23c-20489944dd22.jpg',
      'height': 216,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x106_1e7be5dd-5027-4ccf-a23c-20489944dd22.jpg',
      'height': 106,
      'width': 84}],
    'processedVideos': [{'height': 800,
      'width': 640,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_1e7be5dd-5027-4ccf-a23c-20489944dd22.mp4'},
     {'height': 600,
      'width': 480,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/480x600_1e7be5dd-5027-4ccf-a23c-20489944dd22.mp4'},
     {'height': 400,
      'width': 320,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_1e7be5dd-5027-4ccf-a23c-20489944dd22.mp4'}]},
   {'id': '88cd0d2d-bc6c-44c3-81dc-42412b90d1de',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1080_88cd0d2d-bc6c-44c3-81dc-42412b90d1de.jpg',
    'fileName': '88cd0d2d-bc6c-44c3-81dc-42412b90d1de.jpg',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x640_88cd0d2d-bc6c-44c3-81dc-42412b90d1de.jpg',
      'height': 640,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x320_88cd0d2d-bc6c-44c3-81dc-42412b90d1de.jpg',
      'height': 320,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x172_88cd0d2d-bc6c-44c3-81dc-42412b90d1de.jpg',
      'height': 172,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x84_88cd0d2d-bc6c-44c3-81dc-42412b90d1de.jpg',
      'height': 84,
      'width': 84}]},
   {'id': 'bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1350_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.jpg',
    'fileName': 'bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.mp4',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.jpg',
      'height': 800,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.jpg',
      'height': 400,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x216_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.jpg',
      'height': 216,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x106_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.jpg',
      'height': 106,
      'width': 84}],
    'processedVideos': [{'height': 800,
      'width': 640,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x800_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.mp4'},
     {'height': 600,
      'width': 480,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/480x600_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.mp4'},
     {'height': 400,
      'width': 320,
      'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x400_bbc1b8e5-8cf2-4df7-a6ad-ace7b6b3e58e.mp4'}]},
   {'id': 'e0992e7e-3b1e-49ba-8247-fa23649593c7',
    'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/1080x1080_e0992e7e-3b1e-49ba-8247-fa23649593c7.jpg',
    'fileName': 'e0992e7e-3b1e-49ba-8247-fa23649593c7.jpg',
    'extension': 'jpg',
    'processedFiles': [{'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/640x640_e0992e7e-3b1e-49ba-8247-fa23649593c7.jpg',
      'height': 640,
      'width': 640},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/320x320_e0992e7e-3b1e-49ba-8247-fa23649593c7.jpg',
      'height': 320,
      'width': 320},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/172x172_e0992e7e-3b1e-49ba-8247-fa23649593c7.jpg',
      'height': 172,
      'width': 172},
     {'url': 'https://images-ssl.gotinder.com/582e6c5299fd24862e3d3e0d/84x84_e0992e7e-3b1e-49ba-8247-fa23649593c7.jpg',
      'height': 84,
      'width': 84}]}],
  'instagram': {'completed_initial_fetch': True,
   'last_fetch_time': '2018-09-12T09:28:20.971Z',
   'media_count': 73,
   'photos': [{'image': 'https://scontent.cdninstagram.com/vp/e13ce2abaea436ca33d6c31e88073e19/5C1D8C8E/t51.2885-15/sh0.08/e35/s640x640/35001134_363619330830530_3538971499064983552_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/a601ae243f19a9a24ac388398f6918f0/5C163329/t51.2885-15/e35/s150x150/35001134_363619330830530_3538971499064983552_n.jpg',
     'ts': '1529555691',
     'link': 'https://www.instagram.com/p/BkRgMhyF-cGiocCL2x_BKRGgcS2djlWBuehTWk0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/7beaa1d993061273d764a62f6de98eb2/5C2FD97E/t51.2885-15/sh0.08/e35/s640x640/34423521_1959212974101349_1862057288492122112_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/bd99f11d97fd32132e8ff1ca2eac2bce/5C1D51FB/t51.2885-15/e35/s150x150/34423521_1959212974101349_1862057288492122112_n.jpg',
     'ts': '1528911336',
     'link': 'https://www.instagram.com/p/Bj-TL2nl-09PO86vG7LQsOqrQVVkGvHSXl64io0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/24602b81125c3155ff2ed6a8b367396a/5C2F57CD/t51.2885-15/sh0.08/e35/s640x640/29718017_903998569770996_1541112069137367040_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/3c528d9a7f11e3e7bb5b2cded733f877/5C26486A/t51.2885-15/e35/s150x150/29718017_903998569770996_1541112069137367040_n.jpg',
     'ts': '1523288270',
     'link': 'https://www.instagram.com/p/BhWuCeAFT6QVPiXH7nZQHISjoYA0CbFSwzhMd80/'},
    {'image': 'https://scontent.cdninstagram.com/vp/130bb02f58b5026267a76528fb4e6f55/5C35BE08/t51.2885-15/sh0.08/e35/s640x640/29094901_459370381161417_6006718536066531328_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/f0c1ee412c1f25815701b564fb8f799c/5C201FAF/t51.2885-15/e35/s150x150/29094901_459370381161417_6006718536066531328_n.jpg',
     'ts': '1521938821',
     'link': 'https://www.instagram.com/p/BgugK1yF_5tURRsmdqHFSUi19AS8b0VMSKfkow0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/ad671aa0a30b1a3ca1b6bd324809ad4a/5C3662CF/t51.2885-15/sh0.08/e35/s640x640/27580095_2107840776148448_1304695504134733824_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/9a34239e8de0ec6cf199556996c861af/5C2AA84A/t51.2885-15/e35/s150x150/27580095_2107840776148448_1304695504134733824_n.jpg',
     'ts': '1518705788',
     'link': 'https://www.instagram.com/p/BfOJpZYlnT5Xq_e_zMF-qd3hEfTNdKYVqHoVh40/'},
    {'image': 'https://scontent.cdninstagram.com/vp/0e406e5ec6c865405025d3614290c936/5C22CA95/t51.2885-15/sh0.08/e35/s640x640/26869266_145737412889476_8752060424783921152_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/97387c995917a8070b0abb7dab9de0f2/5C156232/t51.2885-15/e35/s150x150/26869266_145737412889476_8752060424783921152_n.jpg',
     'ts': '1516808946',
     'link': 'https://www.instagram.com/p/BeVntZBFYuq_4fwSnv_mmW8bGlDgzM_uj7AfVs0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/8513a7993c9ff9088263536cb4a3e04b/5C171734/t51.2885-15/sh0.08/e35/s640x640/26154935_2058431231042864_8031600500061241344_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/26e01f732a4af24591855e9896e3dd25/5C2B2DE9/t51.2885-15/e35/c236.0.608.608/s150x150/26154935_2058431231042864_8031600500061241344_n.jpg',
     'ts': '1515397571',
     'link': 'https://www.instagram.com/p/BdrjuWOlH8RsYMAZYZJ7swb7YGaOdoaDydVdGg0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/23300c42464e1c7a65bff85d5f78c60b/5C398B56/t51.2885-15/sh0.08/e35/p640x640/25022435_917193788454084_3416450435890806784_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/aeb1e8ef6c0955fe031d316800782216/5C3585F8/t51.2885-15/e35/c0.135.1080.1080/s150x150/25022435_917193788454084_3416450435890806784_n.jpg',
     'ts': '1514276565',
     'link': 'https://www.instagram.com/p/BdKJky5ls4ZioM8bdQ8bAKAItsqTxqYL9EBiZw0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/1d8ebf1dc1af238fc3d86dfc2d89d9c5/5C2F0C3E/t51.2885-15/sh0.08/e35/s640x640/23594489_146630025979631_1702299142329466880_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/5e0207872c2c13ea8b350aa3b044c56c/5C18A899/t51.2885-15/e35/s150x150/23594489_146630025979631_1702299142329466880_n.jpg',
     'ts': '1510941154',
     'link': 'https://www.instagram.com/p/BbmvyJulY2qyjybNISucJlDXtZhowigF6-IVKM0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/40258d559e639c33507bc7e05afdf7d2/5C26F72A/t51.2885-15/sh0.08/e35/s640x640/22794576_289243198234299_2004369105699733504_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/8c84cef926c6f270a325ae30850288ec/5C32E28D/t51.2885-15/e35/s150x150/22794576_289243198234299_2004369105699733504_n.jpg',
     'ts': '1509219806',
     'link': 'https://www.instagram.com/p/BazckuHln0pIZyCZGrQdWwpg7na-S61omas6wc0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/02abf63b61e6f79c2acc35ce78e0ef06/5C1FA5C6/t51.2885-15/sh0.08/e35/s640x640/22277501_1988528058048445_3703091798697050112_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/f348651aa5fa1cd8168e1e91e426770c/5C352E1B/t51.2885-15/e35/c236.0.608.608/s150x150/22277501_1988528058048445_3703091798697050112_n.jpg',
     'ts': '1507004876',
     'link': 'https://www.instagram.com/p/BZxb7dLF2evqLwBJIh8-okVoP59-NywoXLVFRU0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/cda4abf4d3aa4bec9bf1355c4b7ac2e1/5C33C997/t51.2885-15/sh0.08/e35/s640x640/19379415_889269041222308_2702918662783762432_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/3faccee8b60832dc1fb32e538e5c81b5/5C3B3630/t51.2885-15/e35/s150x150/19379415_889269041222308_2702918662783762432_n.jpg',
     'ts': '1498086914',
     'link': 'https://www.instagram.com/p/BVnqRC1FJTQfCNiRJ81VqdWOvNyk_0E5-fOOMo0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/04636b62dd34365b6a662e7d7fcd1e50/5C3AAD16/t51.2885-15/sh0.08/e35/s640x640/18581384_181339352390605_5278353633841250304_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/2f508c479908ffe59f59671bf64ecbbb/5C1530B1/t51.2885-15/e35/s150x150/18581384_181339352390605_5278353633841250304_n.jpg',
     'ts': '1495420288',
     'link': 'https://www.instagram.com/p/BUYMFK2FrLmSVMZFxDPaT3JaaMdm7rmxizngwc0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/e7389a87c4f44a21eb4b882a047022f4/5C148991/t51.2885-15/sh0.08/e35/s640x640/18444432_1880220588900598_4788083318866313216_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/f0ae1e223d05e0384fb11152adb0bbac/5C1DE814/t51.2885-15/e35/s150x150/18444432_1880220588900598_4788083318866313216_n.jpg',
     'ts': '1494949653',
     'link': 'https://www.instagram.com/p/BUKKapMl-Hx2hfmHixJ6ifo-NsrXYyAowthd340/'},
    {'image': 'https://scontent.cdninstagram.com/vp/dd8b801cbdc383ef4a3e2f89b8bee72d/5C2431AE/t51.2885-15/sh0.08/e35/s640x640/18299061_1382275788519287_4712761854626103296_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/898641b32e409f96566014fe9e5bd226/5C17CB2B/t51.2885-15/e35/s150x150/18299061_1382275788519287_4712761854626103296_n.jpg',
     'ts': '1494256202',
     'link': 'https://www.instagram.com/p/BT1fwyxlpNxfRssUay_gzPUKtAXR47Egw-Q9eo0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/5bbd160bd2aa52cb8827870c517b8087/5C1A8A66/t51.2885-15/sh0.08/e35/s640x640/18161455_1744946715533130_86983120787603456_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/3e763cc92a5f95b59cff600732615ed2/5C3A945E/t51.2885-15/e35/c236.0.608.608/s150x150/18161455_1744946715533130_86983120787603456_n.jpg',
     'ts': '1493584329',
     'link': 'https://www.instagram.com/p/BTheRJNF5T7jKfIe3JZ4m4Q_lBRfqsLObB3_x00/'},
    {'image': 'https://scontent.cdninstagram.com/vp/b77711099daab63371e967b9270618e6/5C1D592B/t51.2885-15/sh0.08/e35/s640x640/17126659_168918610285913_4497910543754985472_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/2aaa3f2760d55262bbdebf89cf0a52aa/5C209E8C/t51.2885-15/e35/s150x150/17126659_168918610285913_4497910543754985472_n.jpg',
     'ts': '1489225085',
     'link': 'https://www.instagram.com/p/BRfjqzvFH2X04_5oZxnag-bDVKeKYnhRqjZgh80/'},
    {'image': 'https://scontent.cdninstagram.com/vp/5dda3c8fad2637bcba7b022ba2d859e2/5C3565EA/t51.2885-15/sh0.08/e35/p640x640/17076592_1770026349979633_3111184175038726144_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/987bca329157b187c8d7768b6cb64984/5C2ABDD6/t51.2885-15/e35/c0.90.720.720/s150x150/17076592_1770026349979633_3111184175038726144_n.jpg',
     'ts': '1488670185',
     'link': 'https://www.instagram.com/p/BRPBR9El8eQ4PnkrT93QbL8dap14HeC1G1UB5s0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/d8767b764eccddaeae7cde05e3c8b53c/5C3551C9/t51.2885-15/sh0.08/e35/s640x640/16789090_1466198716723611_3060597487585722368_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/9ce4d06a339fbb17039f50bdfcbeaf76/5C17874C/t51.2885-15/e35/s150x150/16789090_1466198716723611_3060597487585722368_n.jpg',
     'ts': '1487910698',
     'link': 'https://www.instagram.com/p/BQ4YrPclTqwMAS-3vklyTuJRR2__iHTM6P58nI0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/99b1e186627ad3f9d5e9cfa65a29e0c6/5C27F281/t51.2885-15/sh0.08/e35/s640x640/16906276_714669135361996_4983714552303583232_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/acf1199875923276f14280b48c77cfe7/5C19751C/t51.2885-15/e35/c236.0.608.608/s150x150/16906276_714669135361996_4983714552303583232_n.jpg',
     'ts': '1487806053',
     'link': 'https://www.instagram.com/p/BQ1RFKVlSoBaGSjE9Bm9O4DyvNaqGZn7Q6I3C40/'},
    {'image': 'https://scontent.cdninstagram.com/vp/8f69c642dbf4b77611d8ad67450a949c/5C322922/t51.2885-15/sh0.08/e35/s640x640/16788456_1210212722429619_6533582595173646336_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/9ff76f33c3cc613565ee9caaab870c03/5C2B0CFF/t51.2885-15/e35/c236.0.608.608/s150x150/16788456_1210212722429619_6533582595173646336_n.jpg',
     'ts': '1487643480',
     'link': 'https://www.instagram.com/p/BQwa_yLF_XYvgjiMfpnEAyrFJP0HK6UMkkq3RE0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/cd995bf2b81bb237a650302fd2b3b6f9/5C1D07E4/t51.2885-15/sh0.08/e35/s640x640/16788781_1369534076436318_7940509724091351040_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/5698b5c921e25315d7e8f0926cdadb2d/5C173D39/t51.2885-15/e35/c236.0.608.608/s150x150/16788781_1369534076436318_7940509724091351040_n.jpg',
     'ts': '1487274684',
     'link': 'https://www.instagram.com/p/BQlbkxyFbDuszDShZ08ilrmMSqm1zjBExkocw80/'},
    {'image': 'https://scontent.cdninstagram.com/vp/90f31b3cdea31458d3529f4ea231af1c/5C22C5C4/t51.2885-15/sh0.08/e35/s640x640/15803665_1396472850385207_8062586438539018240_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/abeedf16bb7cda20cbd624a3c83230ee/5C18B441/t51.2885-15/e35/s150x150/15803665_1396472850385207_8062586438539018240_n.jpg',
     'ts': '1483297556',
     'link': 'https://www.instagram.com/p/BOu5zduBwl_BghTZRrXAkh0wXovsaMxLh7CrJk0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/432ac637f893b1396c5b4ca21db9fd29/5C38F46A/t51.2885-15/sh0.08/e35/s640x640/15625393_191100238028230_6305521794556100608_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/7e8c2923c2aaf0a6c176f533caf3f73a/5C2A6FF7/t51.2885-15/e35/c236.0.608.608/s150x150/15625393_191100238028230_6305521794556100608_n.jpg',
     'ts': '1483147216',
     'link': 'https://www.instagram.com/p/BOqbDfDhxh7KT0gD1N6prU1m7kw7ipa8dY4aPE0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/ba8670207b4f9c39ed0db982b3355ee3/5C30FA2E/t51.2885-15/sh0.08/e35/p640x640/15534911_139996143156511_5658472511713574912_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/e973ebd1ba4a468e18463ccecf7bd72f/5C1A9580/t51.2885-15/e35/c0.135.1080.1080/s150x150/15534911_139996143156511_5658472511713574912_n.jpg',
     'ts': '1482468363',
     'link': 'https://www.instagram.com/p/BOWMPorBgLKkatilMyR3QpSkdf1yoWMwf7v2e80/'},
    {'image': 'https://scontent.cdninstagram.com/vp/f1c4d13173d4c62929d2ce069439d0af/5C16A7D5/t51.2885-15/sh0.08/e35/s640x640/14488295_1213134518732791_7847107276463669248_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/d38d3bf769c0d14d3cb3d549cdfa459a/5C37A650/t51.2885-15/e35/s150x150/14488295_1213134518732791_7847107276463669248_n.jpg',
     'ts': '1475028101',
     'link': 'https://www.instagram.com/p/BK4dEhKhp_DFBI4XyGd1jEzdHEWwISAPa4fZHI0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/694785555fd1846bbf05b3cd21353978/5C27E652/t51.2885-15/sh0.08/e35/p640x640/14280404_1225333957508223_1009357163_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/c972921fc4867b2b2f7e39f46443d005/5C20FE36/t51.2885-15/e35/c0.90.720.720/s150x150/14280404_1225333957508223_1009357163_n.jpg',
     'ts': '1473990277',
     'link': 'https://www.instagram.com/p/BKZhlDAhyjQvpilCTT2YjaVLbZsSLl5w_mufFo0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/307e4dd5c8d2aa0f29cbd08f3d195e38/5C375711/t51.2885-15/sh0.08/e35/s640x640/14334415_1024254524339233_1296889889_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/16d44f73fd723d8913f2f5bcaae48b00/5C3532E3/t51.2885-15/e35/c235.0.609.609/s150x150/14334415_1024254524339233_1296889889_n.jpg',
     'ts': '1473653774',
     'link': 'https://www.instagram.com/p/BKPfwFfB0mc_pWxabzTFkql5-i9wUtKPTqQ52U0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/3fc4bafa0c0b4924a9be9b0f1095f392/5C21F245/t51.2885-15/sh0.08/e35/s640x640/14156539_1209137335811310_879169733_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/b55fbc807f1d127f798a0e3aaaf85da6/5C3B6FE8/t51.2885-15/e35/c236.0.608.608/s150x150/14156539_1209137335811310_879169733_n.jpg',
     'ts': '1472858582',
     'link': 'https://www.instagram.com/p/BJ3zCvoB25OmrwkEN_3zgchzFzZ6fv1NO_45jQ0/'},
    {'image': 'https://scontent.cdninstagram.com/vp/150f94a7244aebf7ce6db8cce23e5fa3/5C1E4F87/t51.2885-15/sh0.08/e35/s640x640/13658392_679243538890009_1172070396_n.jpg',
     'thumbnail': 'https://scontent.cdninstagram.com/vp/8e9f411d73be07a614c2cc1bf5f2d3e3/5C25562A/t51.2885-15/e35/c236.0.608.608/s150x150/13658392_679243538890009_1172070396_n.jpg',
     'ts': '1471121021',
     'link': 'https://www.instagram.com/p/BJEA6F0h8ryyaKlXtd9ppmlH3P-Lgh7fk2eLNo0/'}],
   'profile_picture': 'https://scontent.cdninstagram.com/vp/6deb431387bd7c37bd006e5f7dae2e40/5C25F098/t51.2885-19/s150x150/34378526_1196619433813729_5368548325014372352_n.jpg',
   'username': 'laapeenguin'},
  'jobs': [],
  'schools': [{'name': 'Southwestern College', 'id': '124685387589022'}],
  'spotify_top_artists': [{'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/e4d513d1ff18c1baddb884543072c15123c76bd9',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/44b92f7751a7361859d67dc45c911db59615bd6e',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/694bd572a5b698e825e245ac062793cfc721bc10',
      'height': 160}],
    'top_track': {'name': 'I Like It',
     'id': '58q2HKrzhC3ozto2nDdN4z',
     'artists': [{'name': 'Cardi B', 'id': '4kYSro6naA4h99UJvo89HB'},
      {'name': 'Bad Bunny', 'id': '4q3ewBCX7sLwd24euuV69X'},
      {'name': 'J Balvin', 'id': '1vyhD5VmyZ7KMfW5gqLgo5'}],
     'uri': 'spotify:track:58q2HKrzhC3ozto2nDdN4z',
     'preview_url': 'https://p.scdn.co/mp3-preview/0f8734f51bb0a419959fdad3a0852621f9e6bc89?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'Invasion of Privacy',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/10c890602bb0c5e2076e29d10c1d3c4addaa152f',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/af948fc4cc3f16f7b9afcfa31a91ad3a2f460e8c',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/8d5427fb51d552c7dc7208981f8bd58af53e9956',
        'height': 64}],
      'id': '4KdtEKjY3Gi0mKiSdy96ML'}},
    'id': '4q3ewBCX7sLwd24euuV69X',
    'name': 'Bad Bunny'},
   {'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/9f65f9f5ba10e0243da093306d213f88ccb85da6',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/78e87fcc881b4572913167d8488f975c104451b7',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/4c8ff1e7bf10e7f5b1430a270de5faf5e9a21e2c',
      'height': 160}],
    'top_track': {'name': "Hips Don't Lie",
     'id': '3ZFTkvIE7kyPt6Nu3PEa7V',
     'artists': [{'name': 'Shakira', 'id': '0EmeFodog0BfCgMzAIvKQp'},
      {'name': 'Wyclef Jean', 'id': '7aBzpmFXB4WWpPl2F7RjBe'}],
     'uri': 'spotify:track:3ZFTkvIE7kyPt6Nu3PEa7V',
     'preview_url': 'https://p.scdn.co/mp3-preview/3859547944f57cfb7b996f6551148c9467889d4b?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'Oral Fixation Vol. 2',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/3d727554b08c9ce5c04b5cf82144150e3291d2fd',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/9b808e1c293a084e34b88bc4b9f0fc07d417958c',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/e234d27f81844acbd897c38776c39e66607b8f6f',
        'height': 64}],
      'id': '5ppnlEoj4HdRRdRihnY3jU'}},
    'id': '0EmeFodog0BfCgMzAIvKQp',
    'name': 'Shakira'},
   {'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/57f7e8bf00d2a3002e0bfdaa24983484911b6f6a',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/f8f308c86ee39e97e364f13c55da6d43125b8c8e',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/e6e7544aaff486d47e3bb69f0962e2324bb9ac93',
      'height': 160}],
    'top_track': {'name': 'Me Acostumbre (feat. Bad Bunny)',
     'id': '2FIm6YsSGL5acOqSuJDh5s',
     'artists': [{'name': 'Arcangel', 'id': '4SsVbpTthjScTS7U2hmr1X'},
      {'name': 'Bad Bunny', 'id': '4q3ewBCX7sLwd24euuV69X'}],
     'uri': 'spotify:track:2FIm6YsSGL5acOqSuJDh5s',
     'preview_url': 'https://p.scdn.co/mp3-preview/da404d49e7668d426bfb9612713b284e374b227e?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'Me Acostumbre (feat. Bad Bunny)',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/d10e66a07292893fd6d0ada6c709477efb2d9ad1',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/91dfd0f1c22e682dee94c2522f75fd65036a82eb',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/719c09e0ce36eeb0076fc7e1bdd08fa5ab7daf0c',
        'height': 64}],
      'id': '4yE7L5RhMkjX7KkweWjFYk'}},
    'id': '4SsVbpTthjScTS7U2hmr1X',
    'name': 'Arcangel'},
   {'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/72451364835d9bf39d11f77b421f40cc464cc235',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/0ca96aa4cba988ff9c5747b511bde9a97454bdf9',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/7388c9f440b100695f375a65bd0467a98cbc1019',
      'height': 160}],
    'top_track': {'name': 'EL BAÑO',
     'id': '2vvdTrdryjsl8DmPIMDWZU',
     'artists': [{'name': 'Enrique Iglesias', 'id': '7qG3b048QCHVRO5Pv1T5lw'},
      {'name': 'Bad Bunny', 'id': '4q3ewBCX7sLwd24euuV69X'}],
     'uri': 'spotify:track:2vvdTrdryjsl8DmPIMDWZU',
     'preview_url': 'https://p.scdn.co/mp3-preview/0456d479f76cda3f7547568cba1194b7d3f518ce?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'EL BAÑO',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/47ad2bec5af85577739b7bc237f3859e0e65c37a',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/f5626a4a5ec04867627ae3dc9c55821e9c9a6a47',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/de437660ae00c40647630fcec19b3dc077ec198d',
        'height': 64}],
      'id': '5phDwq3mKZdLiFxyRpgcCV'}},
    'id': '7qG3b048QCHVRO5Pv1T5lw',
    'name': 'Enrique Iglesias'},
   {'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/f1df9315a901dae49dd69c003a4784d58bd59e26',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/4ab9a90cd028ec70a7023919e880076c5e84007c',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/04206cea69afe4349ef9b2ce70969cf90d09dae0',
      'height': 160}],
    'top_track': {'name': 'I Wanna Know (feat. Bea Miller)',
     'id': '18W92Zm1KjLCbUIszOhpkD',
     'artists': [{'name': 'NOTD', 'id': '5jAMCwdNHWr7JThxtMuEyy'},
      {'name': 'Bea Miller', 'id': '1o2NpYGqHiCq7FoiYdyd1x'}],
     'uri': 'spotify:track:18W92Zm1KjLCbUIszOhpkD',
     'preview_url': 'https://p.scdn.co/mp3-preview/b8f3eb891176c4916e3a70e4d307d7ac85112c60?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'I Wanna Know (feat. Bea Miller)',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/b90ede6a3744b470d62ea167e2047309cd8cc67e',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/09a26f3dd8b4d8549e3dce20ea3a952a463d19f5',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/03b96ed7066fa6b1c2d2ba6f06a9ac34869c1be0',
        'height': 64}],
      'id': '2xqSl9X8ulJayI0KxABaLV'}},
    'id': '1o2NpYGqHiCq7FoiYdyd1x',
    'name': 'Bea Miller'},
   {'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/4bc58ee39cce2d47094221f58c68ecc6eb1eb9bb',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/795c419e19f1941d2b9e2c6e855ec9b0ed9287bc',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/a67469d81581d03e6ba71d0d0075a3711d863e19',
      'height': 160}],
    'top_track': {'name': 'Complicated',
     'id': '0jllH0usRFD4LJkJnGK9Lf',
     'artists': [{'name': "Olivia O'Brien", 'id': '1QRj3hoop9Mv5VvHQkwPEp'}],
     'uri': 'spotify:track:0jllH0usRFD4LJkJnGK9Lf',
     'preview_url': 'https://p.scdn.co/mp3-preview/ed51ea9fb68f27a420dbaad3aa0ec944b2a4a150?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'Complicated',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/fc3e7f2cd17a0a533fe04fab35d19dce222b404a',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/2f47cdfda049ef3157ed1200864ad091bf269602',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/563e1b94d23b31e64076bf8a93aa0fc905a4fe65',
        'height': 64}],
      'id': '18IaOJpyXfqbOsZIqmnfpZ'}},
    'id': '1QRj3hoop9Mv5VvHQkwPEp',
    'name': "Olivia O'Brien"},
   {'selected': True,
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/9472e27a19f6138f49476541fdaa7f2ef2344f09',
      'height': 640},
     {'width': 320,
      'url': 'https://i.scdn.co/image/cc2987577078a0d8ccf7b3b339ee3b8f329277ed',
      'height': 320},
     {'width': 160,
      'url': 'https://i.scdn.co/image/8c7db2e63db99ed1a942c940e56da2bcc77b4f95',
      'height': 160}],
    'top_track': {'name': 'Home with You',
     'id': '0iwsQWgtjSq2kUXuZwTDAL',
     'artists': [{'name': 'Madison Beer', 'id': '2kRfqPViCqYdSGhYSM9R0Q'}],
     'uri': 'spotify:track:0iwsQWgtjSq2kUXuZwTDAL',
     'preview_url': 'https://p.scdn.co/mp3-preview/3dd4e833f706e3637eb3a6d46312c41c450a44f1?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'As She Pleases',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/2793325ab7aab277ccf944b10a8318e75707897c',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/1d8fe22f7eaaf4cd13cb5a26e7bc1b758110c6ec',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/6b395b988db6f7b9c11a27ae6d28e1fcb8f6169a',
        'height': 64}],
      'id': '5boeEaUtj7gHXFxKtFFlzL'}},
    'id': '2kRfqPViCqYdSGhYSM9R0Q',
    'name': 'Madison Beer'},
   {'selected': True,
    'images': [{'width': 1000,
      'url': 'https://i.scdn.co/image/edabfb79fbf3d71ad9d0961a7b199a1470fe5372',
      'height': 719},
     {'width': 640,
      'url': 'https://i.scdn.co/image/a3c9dd492b973e5d5ebfd957b30325972c16d2d4',
      'height': 460},
     {'width': 200,
      'url': 'https://i.scdn.co/image/896866e81c4a3d873ce3a28b2396f75212d192a0',
      'height': 144},
     {'width': 64,
      'url': 'https://i.scdn.co/image/28b48ccc46a8cb61fbf3e67867fc7794acc6dc85',
      'height': 46}],
    'top_track': {'name': 'Atrévete-Te-Te',
     'id': '1q8NdCAQ9QUjpYiqzdd3mv',
     'artists': [{'name': 'Calle 13', 'id': '0yNSzH5nZmHzeE2xn6Xshb'}],
     'uri': 'spotify:track:1q8NdCAQ9QUjpYiqzdd3mv',
     'preview_url': 'https://p.scdn.co/mp3-preview/ea8d52eda23961ed663ebf99a90015c8d84ebf18?cid=b06a803d686e4612bdc074e786e94062',
     'album': {'name': 'Calle 13 (Explicit Version)',
      'images': [{'width': 640,
        'url': 'https://i.scdn.co/image/7366643a4418788c71022bfc859159b6a9e8ea78',
        'height': 640},
       {'width': 300,
        'url': 'https://i.scdn.co/image/3f7af00cd2ee51212a132d63cc0dd644b0d7e8f7',
        'height': 300},
       {'width': 64,
        'url': 'https://i.scdn.co/image/11479798ed64bb32c8e63f6ec6eec2296daf0a25',
        'height': 64}],
      'id': '5pmuwmV2OcuiTX7kNczQ16'}},
    'id': '0yNSzH5nZmHzeE2xn6Xshb',
    'name': 'Calle 13'}],
  'spotify_theme_track': {'name': 'Sexo Hardcore',
   'id': '40dgXhA8m9vZUvwjzzrI3P',
   'uri': 'spotify:track:40dgXhA8m9vZUvwjzzrI3P',
   'artists': [{'name': 'Bryan Montero', 'id': '4Gg2IUch9Ccr43Yz9GIJ4M'}],
   'preview_url': 'https://p.scdn.co/mp3-preview/ab19d54357cfc7fed6ca24a93858adc38105d78c?cid=b06a803d686e4612bdc074e786e94062',
   'album': {'name': 'Sexo Hardcore',
    'images': [{'width': 640,
      'url': 'https://i.scdn.co/image/3336205b94b3107b9b295162442960cf9cd96673',
      'height': 640},
     {'width': 300,
      'url': 'https://i.scdn.co/image/969ad2c3cfa407b383616082472228095ec43904',
      'height': 300},
     {'width': 64,
      'url': 'https://i.scdn.co/image/d22c63e4f6513f12cde4a57984c6ddbd8082f7dc',
      'height': 64}],
    'id': '2gtje6oZObJzDEgQrrEP17'}},
  'gender': 1,
  'show_gender_on_profile': True,
  'birth_date_info': 'fuzzy birthdate active, not displaying real birth_date',
  'distance_mi': 19,
  'is_tinder_u': False}}

  
    features.print_photos(person) #person needs to be dict with photos attribute 


def silent_mode(fb_username, fb_password):
    runs = 5
    current = 0
    likeAtATime = 0
    if len(sys.argv) > 2:
        runs = sys.argv[2]
    s = Session(fb_username, fb_password)
    s.init_db()
    #takes a GET recs and likes all in the returned list
    #waits 60 minutes and does the same thing again
    #each run averages 15 profiles returned
    while current < runs:
        autoliker(likeAtATime)
        randTime = 1200 + (random() * 10 * 60) #adds a random num of minutes from 1-90 on top of 20 baseline 
        print('sleeping for %d seconds...' % randTime)
        sleep(randTime) # randTime is between 20-40 minutes.
        current += 1

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


