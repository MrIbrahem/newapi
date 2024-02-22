import sys
import os
import configparser

project = '/data/project/himo/'
# ---
if not os.path.isdir(project):
    project = 'I:/core/master'
# ---
config = configparser.ConfigParser()
config.read(project + '/user.ini')
DEFAULT = config['DEFAULT']

username = config['DEFAULT']['botusername']
password = config['DEFAULT']['botpassword']
# ---

passworden = config['DEFAULT']['passworden']
passwordwd = config['DEFAULT']['passwordwd']

password_ar = config['DEFAULT']['password_ar']
password_en = config['DEFAULT']['password_en']

hiacc = config['DEFAULT']['hiacc']
hipass = config['DEFAULT']['hipass']

mdwiki_pass = config['DEFAULT']['mdwiki_pass']

qs_token = config['DEFAULT']['qs_token']
qs_tokenbot = config['DEFAULT']['qs_tokenbot']

if "workibrahem" in sys.argv:
    username = hiacc
    password = hipass
