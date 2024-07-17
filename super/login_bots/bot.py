"""

from newapi.super.login_bots.bot import LOGIN_HELPS

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}

"""
import inspect
import time
import requests
from warnings import warn

import pywikibot
from newapi import printe
from newapi.super.login_bots.r3_token_bot import get_r3_token, dump_r3_token

seasons_by_lang = {}
User_tables = {}


def warn_err(err):
    """
    Return formatted warning message with error details.
    """
    err = str(err)
    nn = inspect.stack()[1][3]
    return f"\ndef {nn}(): {err}"


class LOGIN_HELPS:
    def __init__(self):
        print("class LOGIN_HELPS:")

    def add_User_tables(self, family, table):
        if self.family == family:
            User_tables[family] = table
            self.username = table["username"]
            self.password = table["password"]

    def make_new_r3_token(self):
        """
        Log in to the wiki and get authentication token.
        """
        time.sleep(0.5)

        colors = {"ar": "yellow", "en": "lightpurple"}

        color = colors.get(self.lang, "")

        Bot_passwords = self.password.find("@") != -1

        printe.output(f"<<{color}>> newapi/page.py: Log_to_wiki {self.endpoint}")
        printe.output(f"newapi/page.py: log to {self.lang}.{self.family}.org user:{self.username}, ({Bot_passwords=})")

        logintoken = self.get_logintoken()

        if not logintoken:
            return False

        success = self.get_login_result(logintoken)

        if success:
            printe.output("<<green>> new_api login Success")
        else:
            return False

        r3_params = {"format": "json", "action": "query", "meta": "tokens"}

        try:
            r33 = self.post_it(r3_params)
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(e)
            pywikibot.output("CRITICAL:")

        if not r33:
            _exceptions_ = [
                """('Connection aborted.', OSError("(104, "ECONNRESET")"))""",
            ]
            return False

        csrftoken = r33.get("query", {}).get("tokens", {}).get("csrftoken", "")
        # ---
        dump_r3_token(self.lang, self.family, self.username, csrftoken)
        # ---
        return csrftoken

    def get_logintoken(self):
        r1_params = {
            "format": "json",
            "action": "query",
            "meta": "tokens",
            "type": "login",
        }

        # WARNING: /data/project/himo/core/bots/newapi/page.py:101: UserWarning: Exception:502 Server Error: Server Hangup for url: https://ar.wikipedia.org/w/api.php

        try:
            r11 = self.post_it(r1_params)
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(e)
            pywikibot.output("CRITICAL:")
            return {}

        return r11.get("query", {}).get("tokens", {}).get("logintoken", "")

    def get_login_result(self, logintoken):
        r2_params = {
            "format": "json",
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.password,
            "lgtoken": logintoken,
        }

        r22 = {}

        try:
            r22 = self.post_it(r2_params)
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(e)
            pywikibot.output("CRITICAL:")
        # ---
        success = r22.get("login", {}).get("result", "").lower() == "success"
        # ---
        if success:
            return True
        # ---
        reason = r22.get("login", {}).get("reason", "")
        # ---
        pywikibot.output("<<red>> Traceback (most recent call last):")
        warn(warn_err(f"Exception:{str(r22)}"), UserWarning)
        # ---
        if reason == "Incorrect username or password entered. Please try again.":
            pywikibot.output(f"user:{self.username}, pass:******")
        # ---
        pywikibot.output("CRITICAL:")
        return False

    def log_to_wiki_1(self):
        # ---
        # return self.make_new_r3_token()
        # ---

        # ---
        return self.get_r3token()

    def get_r3token(self):
        r3_token = get_r3_token(self.lang, self.family, self.username)
        # ---
        if r3_token == "make_new":
            r3_token = self.make_new_r3_token()
        # ---
        return r3_token

    def post_it(self, params, files=None, timeout=30):
        headers = {
            "User-Agent": self.user_agent,
        }
        # ---
        seasons_by_lang.setdefault(self.lang, requests.Session())
        # ---
        req0 = seasons_by_lang[self.lang].request("POST", self.endpoint, data=params, files=files, timeout=timeout, headers=headers)
        # ---
        data = self.parse_data(req0)
        # ---
        return data
