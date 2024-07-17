"""

from newapi.super.login_bots.cookies_bot import get_cookies
# cookies = get_cookies(lang, family, username)
# dump_cookies(lang, family, username, cookies)

"""
import os
from pathlib import Path

from newapi import printe

import stat

statgroup = stat.S_IRWXU | stat.S_IRWXG
ta_dir = Path(__file__).parent / "cookies"
# ---
if not ta_dir.exists():
    ta_dir.mkdir()
    printe.output("<<green>> mkdir:")
    printe.output(f"ta_dir:{ta_dir}")
    printe.output("<<green>> mkdir:")
    os.chmod(ta_dir, statgroup)

ta_tab = {}

def get_file_name(lang, family, username):
    # ---
    lang = lang.lower()
    family = family.lower()
    # ---
    username = username.lower().replace(" ", "_").split("@")[0]
    # ---
    file = ta_dir / f"{family}_{lang}_{username}.txt"
    # ---
    return file


def dump_cookies(lang, family, username, cookies):
    # ---
    ta_tab.setdefault(family, {}).setdefault(lang, {})
    # ---
    ta_tab[family][lang][username] = cookies
    # ---
    file = get_file_name(lang, family, username)
    # ---
    try:
        with open(file, "w") as f:
            f.write(cookies)
            os.chmod(str(file), statgroup)
    except Exception as e:
        printe.output(e)
    # ---
    return ""


def from_folder(lang, family, username):
    # ---
    file = get_file_name(lang, family, username)
    # ---
    cookies = False
    # ---
    if file.exists():
        with open(file, "r") as f:
            cookies = f.read()
    else:
        file.touch()
        os.chmod(str(file), statgroup)
    # ---
    return cookies


def get_cookies(lang, family, username):
    # ---
    cookies = ta_tab.get(family, {}).get(lang, {}).get(username, "")
    # ---
    if not cookies:
        cookies = from_folder(lang, family, username)
    # ---
    if not cookies:
        printe.output(f" <<red>> get_cookies: <<yellow>> [[{lang}:{family}]] user:{username} <<red>> not found")
        return "make_new"
    # ---
    return cookies
