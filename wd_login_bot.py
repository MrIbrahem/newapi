"""

from newapi.wd_login_bot import WD_API
# api_new = WD_API('test', family='wikidata')
# api_new = WD_API('www', family='wikidata')
# json1    = api_new.post_params(params, addtoken=False)

"""
# ---
import os
import sys
from newapi.super import bot_wd
from newapi import useraccount

# ---
tool = os.getenv("HOME")
if tool:
    tool = tool.split("/")[-1]
# ---
pyy_file = __file__.replace("\\", "/").split("/")[-1]
# ---
User_tables = {
    "username": useraccount.username,
    "password": useraccount.password,
}
# ---
if "workibrahem" in sys.argv:
    User_tables = {
        "username": useraccount.hiacc,
        "password": useraccount.hipass,
    }
    # ---
    print(f"{pyy_file} use {User_tables['username']} account.")
# ---
bot_wd.User_tables["wikidata"] = User_tables
# ---
WD_API = bot_wd.WD_API


def test():
    pass


if __name__ == "__main__":
    # super_page.print_test[1] = True
    test()
