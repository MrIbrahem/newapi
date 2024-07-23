"""
Usage:
from newapi.super import bot_wd

"""
# ---
import sys
import datetime
from datetime import timedelta
from newapi import printe
from newapi.super.super_login import Login
from newapi.super.bots.handel_errors import HANDEL_ERRORS

User_tables = {}


def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)


class WD_API(Login, HANDEL_ERRORS):
    def __init__(self, lang, family="wikidata"):
        # ---
        self.username = ""
        # ---
        super().__init__(lang, family)
        # ---
        self.lang = lang
        # ---
        self.save_move = False
        # ---
        self.family = "wikidata"
        # ---
        if User_tables != {}:
            for f, tab in User_tables.items():
                self.add_User_tables(f, tab)

    def get_username(self):
        return self.username

    def Login_to_wiki(self):
        # ---
        self.log_to_wiki_1()
