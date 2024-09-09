"""

from newapi.super.login_bots.bot import LOGIN_HELPS

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}

"""
import sys
import os
import requests
from http.cookiejar import MozillaCookieJar

import pywikibot
from newapi import printe
from newapi.super.login_bots.cookies_bot import get_file_name, del_cookies_file
from newapi.except_err import exception_err
from newapi.super.login_bots.params_help import PARAMS_HELPS

# cookies = get_cookies(lang, family, username)
seasons_by_lang = {}
users_by_lang = {}
User_tables = {}
logins_count = {1: 0}


def default_user_agent():
    tool = os.getenv("HOME")
    # "/data/project/mdwiki"
    tool = tool.split("/")[-1] if tool else "himo"
    # ---
    li = f"{tool} bot/1.0 (https://{tool}.toolforge.org/; tools.{tool}@toolforge.org)"
    # ---
    # printe.output(f"default_user_agent: {li}")
    # ---
    return li


class LOGIN_HELPS(PARAMS_HELPS):
    def __init__(self) -> None:
        # print("class LOGIN_HELPS:")
        self.cookie_jar = False
        self.session = requests.Session()
        # ---
        super().__init__()
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

    def add_User_tables(self, family, table) -> None:
        # print(f"add_User_tables: {family=}")
        if self.family == family:
            self.user_table_done = True
            User_tables[family] = table
            self.username = table["username"]
            self.password = table["password"]
            self.sea_key = f"{self.lang}-{self.family}-{self.username}"

    def make_new_r3_token(self) -> str:
        # ---
        r3_params = {
            "format": "json",
            "action": "query",
            "meta": "tokens",
        }
        # ---
        req = self.post_it_parse_data(r3_params) or {}
        # ---
        if not req:
            return False

        csrftoken = req.get("query", {}).get("tokens", {}).get("csrftoken", "")
        # ---
        return csrftoken

    def log_in(self) -> bool:
        """
        Log in to the wiki and get authentication token.
        """
        # time.sleep(0.5)

        colors = {"ar": "yellow", "en": "lightpurple"}

        color = colors.get(self.lang, "")

        Bot_passwords = self.password.find("@") != -1
        logins_count[1] += 1
        printe.output(f"<<{color}>> newapi/page.py: Log_to_wiki {self.endpoint} count:{logins_count[1]}")
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

    def get_logintoken(self) -> str:
        r1_params = {
            "format": "json",
            "action": "query",
            "meta": "tokens",
            "type": "login",
        }

        # WARNING: /data/project/himo/core/bots/newapi/page.py:101: UserWarning: Exception:502 Server Error: Server Hangup for url: https://ar.wikipedia.org/w/api.php

        try:
            r11 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=r1_params, headers=self.headers)
            if not str(r11.status_code).startswith("2"):
                printe.output(f"<<red>> newapi {r11.status_code} Server Error: Server Hangup for url: {self.endpoint}")
        except Exception as e:
            exception_err(e)
            return ""

        jsson1 = {}

        try:
            jsson1 = r11.json()
        except Exception as e:
            print(r11.text)
            exception_err(e)
            return ""

        return jsson1.get("query", {}).get("tokens", {}).get("logintoken") or ""

    def get_login_result(self, logintoken) -> bool:
        if not self.password:
            printe.output("No password")
            return False

        r2_params = {
            "format": "json",
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.password,
            "lgtoken": logintoken,
        }
        # ---
        req = ""
        # ---
        try:
            req = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=r2_params, headers=self.headers)
        except Exception as e:
            exception_err(e)
            return False
        # ---
        r22 = {}
        if req:
            try:
                r22 = req.json()
            except Exception as e:
                exception_err(e)
                print(req.text)
                return False
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

    def log_to_wiki_1(self, do=False) -> str:
        # ---
        return self.make_new_r3_token()

    def loged_in(self) -> bool:
        params = {
            "format": "json",
            "action": "query",
            "meta": "userinfo",
            "uiprop": "groups|rights",
        }
        # ---
        req = ""
        try:
            req = seasons_by_lang[self.sea_key].request("POST", self.endpoint, data=params, headers=self.headers)
        except Exception as e:
            exception_err(e)
            return False
        # ---
        json1 = {}
        if req:
            try:
                json1 = req.json()
            except Exception as e:
                exception_err(e)
                print(req.text)
                return False
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

    def make_new_session(self) -> None:
        # ---
        print("make_new_session:")
        # ---
        seasons_by_lang[self.sea_key] = requests.Session()
        # ---
        self.cookies_file = get_file_name(self.lang, self.family, self.username)
        # ---
        self.cookie_jar = MozillaCookieJar(self.cookies_file)
        # ---
        if os.path.exists(self.cookies_file):
            print("Load cookies from file, including session cookies")
            try:
                self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
                print("We have %d cookies" % len(self.cookie_jar))
                # ---
            except Exception as e:
                print(e)
        # ---
        seasons_by_lang[self.sea_key].cookies = self.cookie_jar
        # ---
        loged_t = False
        # ---
        if len(self.cookie_jar) > 0:
            if self.loged_in():
                loged_t = True
                printe.output("<<green>> Already logged in as " + self.username_in)
        else:
            loged_t = self.log_in()
        # ---
        if loged_t:
            self.cookie_jar.save(ignore_discard=True, ignore_expires=True)

    def post_it_2(self, params, files=None, timeout=30) -> any or None:
        # ---
        if not self.user_table_done:
            printe.output("<<green>> user_table_done == False!")
            printe.output("<<green>> user_table_done == False!")
            printe.output("<<green>> user_table_done == False!")
            # do error
            if "raise" in sys.argv:
                raise Exception("user_table_done == False!")
        # ---
        args = {
            "files": files,
            "headers": self.headers,
            "data": params,
            "timeout": timeout,
        }
        # ---
        if "dopost" in sys.argv:
            printe.output("<<green>> dopost:::")
            printe.output(params)
            printe.output("<<green>> :::dopost")
            req0 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, **args)
            return req0
        # ---
        req0 = None
        # ---
        try:
            req0 = seasons_by_lang[self.sea_key].request("POST", self.endpoint, **args)

        except requests.exceptions.ReadTimeout:
            printe.output(f"<<red>> ReadTimeout: {self.endpoint=}, {timeout=}")

        except Exception as e:
            exception_err(e)
        # ---
        if req0:
            print(f"status_code: {req0.status_code}")
        # ---
        return req0

    def post_it(self, params, files=None, timeout=30) -> any or None:
        """Post data to a specified endpoint with optional file uploads.

        This method processes the given parameters and files, manages user
        sessions, and handles potential issues such as missing usernames or
        database lag. It ensures that a valid session is established before
        making the POST request and provides feedback on the request's success
        or failure.

        Args:
            params (dict): A dictionary of parameters to be sent in the POST request.
            files (dict?): A dictionary of files to be uploaded with the request. Defaults to None.
            timeout (int?): The timeout duration for the request in seconds. Defaults to 30.

        Returns:
            any or None: The response object from the POST request, or None if the
                request fails.
        """

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
            printe.output(f"<<red>> no username_in.. action:" + params.get("action"))
            # return {}
        # ---
        req0 = self.post_it_2(params, files=files, timeout=timeout)
        # ---
        if not req0:
            printe.output("<<red>> no req0.. ")
            return req0
        # ---
        if req0.headers and req0.headers.get("x-database-lag"):
            printe.output("<<red>> x-database-lag.. ")

            print(req0.headers)
            # raise
        # ---
        return req0

    def post_it_parse_data(self, params, files=None, timeout=30, relogin=False) -> dict:
        # ---
        req = self.post_it(params, files, timeout)
        # ---
        data = {}
        # ---
        if req:
            data = self.parse_data(req) or {}
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

    def get_rest_result(self, url) -> dict:
        # ---
        print("get_rest_result:")
        # ---
        result = {}
        # ---
        try:
            req0 = seasons_by_lang[self.sea_key].request("GET", url)
            result = req0.json()

        except Exception as e:
            exception_err(e)
        # ---
        return result
