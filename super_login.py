# ---
# from newapi import super_login
# super_login.User_tables["wikipedia"] = User_tables
# ---
# bot   = Login(lang, family="wikipedia")
# login = bot.Log_to_wiki()
# json1 = bot.post(params, Type="post", addtoken=False)
# ---
import inspect
import sys
import time
import json
import requests
import urllib
import urllib.parse
import traceback
from warnings import warn
import pywikibot
from newapi import printe
from requests.exceptions import Timeout

# ---
print_test = {1: False}
# ---
User_tables = {"mdwiki": {}, "wikidata": {}, "wikipedia": {}, "nccommons": {}}
# ---
tokens_by_lang = {}
seasons_by_lang = {}
# ---
ar_lag = {1: 3}
login_lang = {1: True}


def warn_err(err):
    err = str(err)
    nn = inspect.stack()[1][3]
    return f"\ndef {nn}(): {err}"


class Login:
    def __init__(self, lang, family="wikipedia"):
        self.lang = lang
        self.family = family
        self.r3_token = ""
        self.url_o_print = ""

        User_tables.setdefault(self.family, {"username": "", "password": ""})
        tokens_by_lang.setdefault(self.lang, "")
        seasons_by_lang.setdefault(self.lang, requests.Session())

        self.username = User_tables[self.family]["username"]
        self.password = User_tables[self.family]["password"]

        self.Bot_or_himo = 1 if "bot" not in self.username else ""

        self.endpoint = f"https://{self.lang}.{self.family}.org/w/api.php"
        # self.season = requests.Session()

    def Log_to_wiki(self):
        return True

    def p_url(self, params):
        if print_test[1] or "printurl" in sys.argv:
            pams2 = {
                k: v[:100] if isinstance(v, str) and len(v) > 100 else v
                for k, v in params.items()
            }
            self.url_o_print = (
                f"{self.endpoint}?{urllib.parse.urlencode(pams2)}".replace(
                    "&format=json", ""
                )
            )
            printe.output(self.url_o_print)

    def prase_data(self, req0):
        text = ""
        try:
            data = req0.json()
            return data
        except Exception as e:
            text = str(req0.text).strip()

        valid_text = text.startswith("{") and text.endswith("}")

        if not text or not valid_text:
            return {}

        try:
            data = json.loads(text)
            return data
        except Exception as e:
            pywikibot.output("<<lightred>> Traceback (most recent call last):")
            pywikibot.output(f"error:{e} when json.loads(response.text)")
            pywikibot.output(traceback.format_exc())
            pywikibot.output(self.url_o_print)
            if str(e) == "Expecting value: line 1 column 1 (char 0)":
                pywikibot.output(params)
            pywikibot.output("CRITICAL:")

        return {}

    def make_response(self, params, files=None):
        self.p_url(params)

        seasons_by_lang.setdefault(self.lang, requests.Session())

        # handle errors
        try:
            req0 = seasons_by_lang[self.lang].post(self.endpoint, data=params, files=files, timeout=30)
            # req0.raise_for_status()

        except requests.exceptions.ReadTimeout:
            printe.output(f'ReadTimeout: {self.endpoint}')

        except Exception:
            pywikibot.output("<<lightred>> Traceback (most recent call last):")
            pywikibot.output(traceback.format_exc())
            pywikibot.output("CRITICAL:")
            return {}

        data = self.prase_data(req0)
        return data

    def Log_to_wiki_1(self):

        login_lang[1] = self.lang

        time.sleep(0.5)

        colors = {"ar": "yellow", "en": "lightpurple"}

        color = colors.get(self.lang, "")

        # self.season = requests.Session()
        printe.output(f"<<{color}>> newapi/page.py: Log_to_wiki {self.endpoint}")

        r2_params = {
            "format": "json",
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.password,
            "lgtoken": "",
        }

        printe.output(
            f"newapi/page.py: log to {self.lang}.{self.family}.org user:{self.username}"
        )

        r1_params = {
            "format": "json",
            "action": "query",
            "meta": "tokens",
            "type": "login",
        }

        # WARNING: /data/project/himo/core/newapi/page.py:101: UserWarning: Exception:502 Server Error: Server Hangup for url: https://ar.wikipedia.org/w/api.php

        r11 = self.make_response(r1_params)

        r2_params["lgtoken"] = (
            r11.get("query", {}).get("tokens", {}).get("logintoken", "")
        )

        if r2_params["lgtoken"] == "":
            return False

        r22 = self.make_response(r2_params)

        if r22 == {}:
            return False

        success = r22.get("login", {}).get("result", "").lower() == "success"

        if not success:
            reason = r22.get("login", {}).get("reason", "")
            pywikibot.output("<<lightred>> Traceback (most recent call last):")
            warn(warn_err(f"Exception:{str(r22)}"), UserWarning)
            if reason == "Incorrect username or password entered. Please try again.":
                pywikibot.output(f"user:{self.username}, pass:{self.password}")
            pywikibot.output("CRITICAL:")
            return False

        printe.output(f"<<green>> {__file__} login Success")

        r3_params = {"format": "json", "action": "query", "meta": "tokens"}
        r33 = self.make_response(r3_params)

        if r33 == {}:
            _Except_ions_ = [
                """('Connection aborted.', OSError("(104, "ECONNRESET")"))""",
            ]
            return False

        r3_token = r33.get("query", {}).get("tokens", {}).get("csrftoken", "")
        self.r3_token = r3_token

        tokens_by_lang[self.lang] = r3_token
        # printe.output(f'<<green>> r3_token: {self.r3_token}')

    def filter_params(self, params):
        if (
            self.family == "wikipedia"
            and params.get("summary")
            and self.username.find("bot") == -1
        ):
            params["summary"] = ""

        if "workibrahem" in sys.argv:
            params["summary"] = ""

        if params["action"] in ["query"]:
            if "bot" in params:
                del params["bot"]
            if "summary" in params:
                del params["summary"]

        return params

    def post(self, params, Type="get", addtoken=False, CSRF=True, files=None):
        # if login_lang[1] != self.lang:
        # printe.output(f'<<red>> login_lang[1]: {login_lang[1]} != self.lang:{self.lang}')
        # self.Log_to_wiki_1()

        if self.r3_token == "":
            self.r3_token = tokens_by_lang.get(self.lang, "")

        if self.r3_token == "":
            self.Log_to_wiki_1()

        params["format"] = "json"
        params["utf8"] = 1
        params["bot"] = self.Bot_or_himo
        params["maxlag"] = ar_lag[1]

        if "minor" in params and params["minor"] == "":
            params["minor"] = self.Bot_or_himo

        if addtoken or params["action"] in ["edit", "create", "upload", "delete"]:
            if self.r3_token == "":
                warn(warn_err('self.r3_token == "" '), UserWarning)
                warn(warn_err('self.r3_token == "" '), UserWarning)
            params["token"] = self.r3_token

        params = self.filter_params(params)

        params.setdefault("formatversion", "1")

        data = self.make_response(params, files=files)

        if data == {}:
            return {}

        error = data.get("error", {})
        if error != {}:
            # printe.output(data)
            Invalid = error.get("info", "")
            code = error.get("code", "")
            # printe.output(Invalid)
            if Invalid == "Invalid CSRF token." and CSRF:
                pywikibot.output(
                    f'<<lightred>> ** error "Invalid CSRF token.".\n{self.r3_token} '
                )
                self.r3_token = ""
                self.Log_to_wiki_1()
                return self.post(params, Type=Type, addtoken=addtoken, CSRF=False)

        if "printdata" in sys.argv:
            # printe.output( json.dumps(data,ensure_ascii=False) )
            printe.output(data)

        return data
