"""

python3 core8/pwb.py newapi/tests/test_login

python3 core8/pwb.py newapi/tests/test_login

"""
from newapi import useraccount

User_tables = {"username": useraccount.username, "password": useraccount.password}
# ---
from newapi import super_login

super_login.User_tables['wikipedia'] = User_tables
# ---
Login = super_login.Login
# ---
bot = Login('axxr', family='wikipedia')
login = bot.Log_to_wiki()
# ---
params = {'action': 'query', 'titles': f"User:{User_tables['username']}", 'prop': 'revisions', 'rvprop': 'content', 'rvslots': '*', 'format': 'json'}
# ---
json1 = bot.post(params, Type='post', addtoken=False)
# ---
print(json1)
# ---
