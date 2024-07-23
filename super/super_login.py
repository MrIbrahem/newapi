# ---
"""
from newapi.super import super_login
# ---
# bot   = Login(lang, family="wikipedia")
# login = bot.Log_to_wiki()
# json1 = bot.post_params(params, Type="post", addtoken=False, files=None)

# ----

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}

# ----

"""
# ---
import os
import inspect
import sys
import json
import urllib.parse
import traceback
from warnings import warn

import pywikibot
from newapi import printe
from newapi.super.login_bots.bot import LOGIN_HELPS

file_name = os.path.basename(__file__)

print_test = {1: False}
User_tables = {"mdwiki": {}, "wikidata": {}, "wikipedia": {}, "nccommons": {}}
seasons_by_lang = {}
ar_lag = {1: 3}


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


def test_print(s):
    if "test_print" in sys.argv:
        printe.output(s)


def warn_err(err):
    """
    Return formatted warning message with error details.
    """
    err = str(err)
    nn = inspect.stack()[1][3]
    return f"\ndef {nn}(): {err}"


class Login(LOGIN_HELPS):
    """
    Represents a login session for a wiki.
    """

    def __init__(self, lang, family="wikipedia"):
        # print(f"class Login:{lang=}")

        super().__init__()

        self.lang = lang
        self.family = family
        self.r3_token = ""
        self.url_o_print = ""
        self.user_agent = default_user_agent()
        # self.headers = {"User-Agent": self.user_agent}

        self.endpoint = f"https://{self.lang}.{self.family}.org/w/api.php"

    def Log_to_wiki(self):
        """
        Log in to the wiki.
        """
        return True

    def p_url(self, params):
        """
        Print the URL for debugging purposes.
        """
        if print_test[1] or "printurl" in sys.argv:
            no_url = ["lgpassword", "format"]
            no_remove = ["titles", "title"]
            pams2 = {k: v[:100] if isinstance(v, str) and len(v) > 100 and k not in no_remove else v for k, v in params.items() if k not in no_url}
            self.url_o_print = f"{self.endpoint}?{urllib.parse.urlencode(pams2)}".replace("&format=json", "")
            printe.output(self.url_o_print)

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

    def make_response(self, params, files=None, timeout=30):
        """
        Make a POST request to the API endpoint.
        """
        self.p_url(params)

        data = {}

        if params.get("list") == "querypage":
            timeout = 60

        req = self.post_it(params, files, timeout)
        # ---
        if req:
            data = self.parse_data(req)
        # ---
        return data

    def filter_params(self, params):
        """
        Filter out unnecessary parameters.
        """
        if self.family == "nccommons" and params.get("bot"):
            del params["bot"]

        if "workibrahem" in sys.argv:
            params["summary"] = ""

        if params["action"] in ["query"]:
            if "bot" in params:
                del params["bot"]
            if "summary" in params:
                del params["summary"]

        return params

    def post(self, params, Type="get", addtoken=False, CSRF=True, files=None):
        return self.post_params(params, Type=Type, addtoken=addtoken, CSRF=CSRF, files=files)

    def post_params(self, params, Type="get", addtoken=False, CSRF=True, files=None):
        """
        Make a POST request to the API endpoint with authentication token.
        """
        params["format"] = "json"
        params["utf8"] = 1
        params["maxlag"] = ar_lag[1]

        if addtoken or params["action"] in ["edit", "create", "upload", "delete", "move"]:
            if not self.r3_token:
                self.r3_token = self.get_r3token()

            if not self.r3_token:
                warn(warn_err('self.r3_token == "" '), UserWarning)

            params["token"] = self.r3_token

        params = self.filter_params(params)

        params.setdefault("formatversion", "1")

        data = self.make_response(params, files=files)

        if not data:
            printe.output("<<red>> super_login(post): not data. return {}.")
            return {}

        error = data.get("error", {})
        if error != {}:
            Invalid = error.get("info", "")
            # code = error.get("code", "")
            # ---
            printe.output(f"<<red>> super_login(post): error: {error}")
            # ---
            if Invalid == "Invalid CSRF token.":
                pywikibot.output(f'<<red>> ** error "Invalid CSRF token.".\n{self.r3_token} ')
                if CSRF:
                    # ---
                    self.r3_token = self.make_new_r3_token()
                    # ---
                    return self.post_params(params, Type=Type, addtoken=addtoken, CSRF=False)

        if "printdata" in sys.argv:
            printe.output(data)

        return data
