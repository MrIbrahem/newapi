"""

from newapi.super.login_bots.bot import LOGIN_HELPS

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}

"""
import os
import inspect
import time
import requests
from warnings import warn
from http.cookiejar import MozillaCookieJar

import pywikibot
from newapi import printe
from newapi.super.login_bots.r3_token_bot import get_r3_token, dump_r3_token

from newapi.super.login_bots.cookies_bot import get_file_name, dump_cookies

# cookies = get_cookies(lang, family, username)
# dump_cookies(lang, family, username, cookies)
seasons_by_lang = {}
users_by_lang = {}
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
        self.cookie_jar = False
        self.session = requests.Session()
        self.username_in = ""

    def add_User_tables(self, family, table):
        if self.family == family:
            User_tables[family] = table
            self.username = table["username"]
            self.password = table["password"]

    def make_new_r3_token(self):
        r3_params = {"format": "json", "action": "query", "meta": "tokens"}

        try:
            req = self.post_it(r3_params)
            r33 = req.json()
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

    def log_in(self):
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
            return True
        else:
            return False

    def get_logintoken(self):
        r1_params = {
            "format": "json",
            "action": "query",
            "meta": "tokens",
            "type": "login",
        }

        # WARNING: /data/project/himo/core/bots/newapi/page.py:101: UserWarning: Exception:502 Server Error: Server Hangup for url: https://ar.wikipedia.org/w/api.php

        try:
            r11 = seasons_by_lang[self.lang].request("POST", self.endpoint, data=r1_params)
            jsson1 = r11.json()
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(e)
            pywikibot.output("CRITICAL:")
            return {}

        return jsson1.get("query", {}).get("tokens", {}).get("logintoken", "")

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
            req = seasons_by_lang[self.lang].request("POST", self.endpoint, data=r2_params)
            r22 = req.json()
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(e)
            pywikibot.output("CRITICAL:")
        # ---
        success = r22.get("login", {}).get("result", "").lower() == "success"
        # ---
        if success:
            self.loged_in()
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

    def log_to_wiki_1(self, do=False):
        # ---
        # return self.make_new_r3_token()
        # ---
        if do:
            return self.get_r3token()
        # ---
        return True

    def get_r3token(self):
        r3_token = get_r3_token(self.lang, self.family, self.username)
        # ---
        if r3_token == "make_new":
            r3_token = self.make_new_r3_token()
        # ---
        return r3_token

    def loged_in(self):
        params = {
            "format": "json",
            "action": "query",
            "meta": "userinfo",
            "uiprop": "groups|rights",
        }

        json1 = {}

        try:
            r22 = seasons_by_lang[self.lang].request("POST", self.endpoint, data=params)
            json1 = r22.json()
            # print(json1)
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(e)
            pywikibot.output("CRITICAL:")
        # ---
        # {'batchcomplete': '', 'query': {'userinfo': {'id': 593870, 'name': 'Mr.Ibrahembot', 'groups': ['bot', 'editor', '*', 'user', 'autoconfirmed'], 'rights': ['apihighlimits', 'editautoreviewprotected', 'editeditorprotected', 'ipblock-exempt', 'noratelimit', 'bot', 'autoconfirmed', 'editsemiprotected', 'nominornewtalk', 'autopatrol', 'suppressredirect', 'writeapi', 'autoreview', 'sboverride', 'skipcaptcha', 'abusefilter-bypass-blocked-external-domains', 'review', 'unreviewedpages', 'patrolmarks', 'read', 'edit', 'createpage', 'createtalk', 'abusefilter-log-detail', 'abusefilter-view', 'abusefilter-log', 'flow-hide', 'flow-edit-title', 'move-rootuserpages', 'move-categorypages', 'minoredit', 'applychangetags', 'changetags', 'move', 'flow-edit-post', 'movestable']}}}
        # ---
        userinfo = json1.get("query", {}).get("userinfo", {})
        # ---
        if "anon" in userinfo:
            return False
        # ---
        # print(userinfo)
        # ---
        self.username_in = userinfo.get("name", "")
        users_by_lang[self.lang] = self.username_in
        # ---
        return True

    def make_new_session(self):
        # ---
        print("make_new_session:")
        # ---
        # self.session = requests.Session()
        # ---
        seasons_by_lang[self.lang] = requests.Session()
        # ---
        cookies_file = get_file_name(self.lang, self.family, self.username)
        # ---
        self.cookie_jar = MozillaCookieJar(cookies_file)
        # ---
        if os.path.exists(cookies_file):
            print("Load cookies from file, including session cookies")
            self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
            print("We have %d cookies" % len(self.cookie_jar))
        # ---
        seasons_by_lang[self.lang].cookies = self.cookie_jar  # Tell Requests session to use the cookiejar.
        # ---
        if self.loged_in():
            print("Already logged in as " + self.username_in)
        else:
            self.log_in()
        # ---
        # r3_token = self.make_new_r3_token()
        # ---
        self.cookie_jar.save(ignore_discard=True, ignore_expires=True)
        # ---
        # return seasons_by_lang[self.lang]

    def post_it(self, params, files=None, timeout=30):
        headers = {
            "User-Agent": self.user_agent,
        }
        # ---
        session = seasons_by_lang.get(self.lang)
        self.username_in = users_by_lang.get(self.lang, "")
        # ---
        if not session:
            self.make_new_session()
        # ---
        if not self.username_in:
            printe.output("<<red>> no username_in.. ")
            return {}
        # ---
        params["assertuser"] = self.username
        # ---
        req0 = seasons_by_lang[self.lang].request("POST", self.endpoint, data=params, files=files, timeout=timeout, headers=headers)
        # ---
        if not req0:
            return {}
        # ---
        return req0
