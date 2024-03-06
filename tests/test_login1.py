"""

python3 core8/pwb.py newapi/tests/test_login

python3 core8/pwb.py newapi/tests/test_login

"""
from newapi import useraccount

User_tables = {
    "username": useraccount.username,
    "password": useraccount.password + "213"
}
# ---
from newapi import super_login1

super_login1.User_tables['wikipedia'] = User_tables
# ---
Login = super_login1.Login
# ---
bot = Login('en', family='wikipedia')
login = bot.Log_to_wiki()
# ---
params = {
    'action': 'query',
    'titles': 'User:Mr. Ibrahem',
    'prop': 'revisions',
    'rvprop': 'content',
    'rvslots': '*',
    'format': 'json'
}
# ---
json1 = bot.post(params, Type='post', addtoken=False)
# ---
print(json1)
# ---
