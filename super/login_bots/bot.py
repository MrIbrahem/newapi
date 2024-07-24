"""

from newapi.super.login_bots.bot import LOGIN_HELPS

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}

"""
import sys
import os
import inspect
import json
import traceback
import requests
from warnings import warn
from http.cookiejar import MozillaCookieJar

import pywikibot
from newapi import printe
from newapi.super.login_bots.r3_token_bot import get_r3_token, dump_r3_token

from newapi.super.login_bots.cookies_bot import get_file_name, del_cookies_file

# cookies = get_cookies(lang, family, username)
seasons_by_lang = {}
users_by_lang = {}
User_tables = {}


def default_user_agent():
    tool = os.getenv("HOME")
    if tool:
        # "/data/project/mdwiki"
        tool = tool.split("/")[-1]
    else:
        tool = "himo"
    # ---
    li = f"{tool} bot/1.0 (https://{tool}.toolforge.org/; tools.{tool}@toolforge.org)"
    # ---
    # printe.output(f"default_user_agent: {li}")
    # ---
    return li


def warn_err(err):
    """
    Return formatted warning message with error details.
    """
    err = str(err)
    nn = inspect.stack()[1][3]
    return f"\ndef {nn}(): {err}"


def exception_err(e):
    pywikibot.output("<<red>> Traceback (most recent call last):")
    warn(warn_err(f"Exception:{str(e)}"), UserWarning, stacklevel=2)
    pywikibot.output("CRITICAL:")


class LOGIN_HELPS:
    def __init__(self):
        # print("class LOGIN_HELPS:")
        self.cookie_jar = False
        self.session = requests.Session()
        # ---
        # check if self has username before writeself.username = ""
        self.username = getattr(self, "username") if hasattr(self, "username") else ""
        self.family = getattr(self, "family") if hasattr(self, "family") else ""
        self.lang = getattr(self, "lang") if hasattr(self, "lang") else ""
        # ---
        self.password = ""
        self.username_in = ""
        self.Bot_or_himo = 0
        self.cookies_file = ""
        self.user_table_done = False
        self.user_agent = default_user_agent()
        self.headers = {"User-Agent": self.user_agent}
        self.sea_key = f"{self.lang}-{self.family}-{self.username}"

    def add_User_tables(self, family, table):
        print(f"add_User_tables: {family=}")
        if self.family == family:
            self.user_table_done = True
            User_tables[family] = table
            self.username = table["username"]
            self.password = table["password"]
            self.sea_key = f"{self.lang}-{self.family}-{self.username}"

    def make_new_r3_token(self):
        r3_params = {"format": "json", "action": "query", "meta": "tokens"}
        r33 = {}
        try:
            req = self.post_it(r3_params)
            r33 = req.json()
        except Exception as e:
            exception_err(e)

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
        # time.sleep(0.5)

        colors = {"ar": "yellow", "en": "lightpurple"}

        color = colors.get(self.lang, "")
        if self.lang == "test" and "testwikidata" not in sys.argv:
            raise Exception("test")

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
        jsson1 = {}
        try:
            r11 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=r1_params, headers=self.headers)
            if not str(r11.status_code).startswith("2"):
                printe.output(f"<<red>> newapi {r11.status_code} Server Error: Server Hangup for url: {self.endpoint}")
        except Exception as e:
            exception_err(e)
            return {}

        try:
            jsson1 = r11.json()
        except Exception as e:
            print(r11.text)
            exception_err(e)
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
            req = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=r2_params, headers=self.headers)
            r22 = req.json()
        except Exception as e:
            exception_err(e)
        # ---
        success = r22.get("login", {}).get("result", "").lower() == "success"
        # ---
        if success:
            self.loged_in()
            return True
        # ---
        reason = r22.get("login", {}).get("reason", "")
        # ---
        # exception_err(r22)
        # ---
        if reason == "Incorrect username or password entered. Please try again.":
            pywikibot.output(f"user:{self.username}, pass:******")
        # ---
        return False

    def log_to_wiki_1(self, do=False):
        # ---
        return self.make_new_r3_token()
        # ---
        # if do: return self.get_r3token()
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
            r22 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=params, headers=self.headers)
            json1 = r22.json()
            # print(json1)
        except Exception as e:
            exception_err(e)
            return False
        # ---
        # {'batchcomplete': '', 'query': {'userinfo': {'id': 593870, 'name': 'Mr.Ibrahembot', 'groups': ['bot', 'editor', '*', 'user', 'autoconfirmed'], 'rights': ['apihighlimits', 'editautoreviewprotected', 'editeditorprotected', 'ipblock-exempt', 'noratelimit', 'bot', 'autoconfirmed', 'editsemiprotected', 'nominornewtalk', 'autopatrol', 'suppressredirect', 'writeapi', 'autoreview', 'sboverride', 'skipcaptcha', 'abusefilter-bypass-blocked-external-domains', 'review', 'unreviewedpages', 'patrolmarks', 'read', 'edit', 'createpage', 'createtalk', 'abusefilter-log-detail', 'abusefilter-view', 'abusefilter-log', 'flow-hide', 'flow-edit-title', 'move-rootuserpages', 'move-categorypages', 'minoredit', 'applychangetags', 'changetags', 'move', 'flow-edit-post', 'movestable']}}}
        # ---
        userinfo = json1.get("query", {}).get("userinfo", {})
        # ---
        # print(json1)
        # ---
        if "anon" in userinfo:
            return False
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
        seasons_by_lang[self.sea_key] = requests.Session()
        # ---
        self.cookies_file = get_file_name(self.lang, self.family, self.username)
        # ---
        self.cookie_jar = MozillaCookieJar(self.cookies_file)
        # ---
        if os.path.exists(self.cookies_file):
            print(f"Load cookies from file, including session cookies {self.cookies_file}")
            try:
                self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
                print("We have %d cookies" % len(self.cookie_jar))
                # ---
                # if len(self.cookie_jar) == 0: self.cookies_file.write_text("")
                # ---
            except Exception as e:
                exception_err(e)
                # self.cookies_file.write_text("")
        # ---
        seasons_by_lang[self.sea_key].cookies = self.cookie_jar  # Tell Requests session to use the cookiejar.
        # ---
        loged_t = False
        # ---
        if len(self.cookie_jar) > 0:
            if self.loged_in():
                loged_t = True
                printe.output("<<green>> Already logged in as " + self.username_in)
        else:
            # self.cookies_file.write_text("")
            loged_t = self.log_in()
        # ---
        # r3_token = self.make_new_r3_token()
        # ---
        if loged_t:
            self.cookie_jar.save(ignore_discard=True, ignore_expires=True)
        # ---
        # return seasons_by_lang[self.sea_key]

    def params_w(self, params):
        if self.family == "wikipedia" and self.lang == "ar" and params.get("summary") and self.username.find("bot") == -1:
            params["summary"] = ""

        self.Bot_or_himo = 1 if "bot" in self.username else 0

        params["bot"] = self.Bot_or_himo
        if "minor" in params and params["minor"] == "":
            params["minor"] = self.Bot_or_himo

        if params["action"] in ["edit", "create", "upload", "delete", "move"] or params["action"].startswith("wb") or self.family == "wikidata":
            params["assertuser"] = self.username

        return params

    def parse_data(self, req0):
        """
        Parse JSON response data.
        """
        text = ""
        try:
            if isinstance(req0, dict):
                data = req0
            else:
                data = req0.json()

            if data.get("error", {}).get("*", "").find("mailing list") > -1:
                data["error"]["*"] = ""
            if data.get("servedby"):
                data["servedby"] = ""

            return data
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(f"error:{e} when json.loads(response.text)")
            pywikibot.output("CRITICAL:")
            text = str(req0.text).strip()

        valid_text = text.startswith("{") and text.endswith("}")

        if not text or not valid_text:
            return {}

        try:
            data = json.loads(text)
            return data
        except Exception as e:
            pywikibot.output("<<red>> Traceback (most recent call last):")
            pywikibot.output(f"error:{e} when json.loads(response.text)")
            pywikibot.output(traceback.format_exc())
            pywikibot.output(self.url_o_print)
            pywikibot.output("CRITICAL:")

        return {}

    def post_it_2(self, params, files=None, timeout=30):
        # ---
        if not self.user_table_done:
            printe.output("<<green>> user_table_done == False!")
            printe.output("<<green>> user_table_done == False!")
            printe.output("<<green>> user_table_done == False!")
            # do error
            if "raise" in sys.argv:
                raise Exception("user_table_done == False!")
        # ---
        if "dopost" in sys.argv:
            printe.output("<<green>> dopost:::")
            req0 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=params, files=files, timeout=timeout, headers=self.headers)
            return req0
        # ---
        req0 = None
        # ---
        try:
            req0 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=params, files=files, timeout=timeout, headers=self.headers)

        except requests.exceptions.ReadTimeout:
            printe.output(f"<<red>> ReadTimeout: {self.endpoint=}, {timeout=}")

        except Exception as e:
            exception_err(e)
        # ---
        return req0

    def post_it(self, params, files=None, timeout=30):
        params = self.params_w(params)
        # ---
        session = seasons_by_lang.get(self.sea_key)
        # ---
        if not self.username_in:
            self.username_in = users_by_lang.get(self.lang, "")
        # ---
        if not session:
            self.make_new_session()
        # ---
        if not self.username_in:
            printe.output("<<red>> no username_in.. ")
            # return {}
        # ---
        req0 = self.post_it_2(params, files=files, timeout=timeout)
        # ---
        if not req0:
            printe.output("<<red>> no req0.. ")
            return {}
        # ---
        return req0

    def post_it_parse_data(self, params, files=None, timeout=30, relogin=False):
        # ---
        req = self.post_it(params, files, timeout)
        # ---
        data = {}
        # ---
        if req:
            data = self.parse_data(req)
        # ---
        error = data.get("error", {})
        # ---
        # {'code': 'assertnameduserfailed', 'info': 'You are no longer logged in as "Mr. Ibrahem", ....', '*': ''}
        # ---
        if error:
            code = error.get("code", "")
            # ---
            if code == "assertnameduserfailed":
                # ---
                del_cookies_file(self.cookies_file)
                # ---
                self.username_in = ""
                self.make_new_session()
                # ---
                return self.post_it_parse_data(params, files, timeout, relogin=True)
        # ---
        return data
