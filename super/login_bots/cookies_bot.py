"""

from newapi.super.login_bots.cookies_bot import get_cookies
# cookies = get_cookies(lang, family, username)

"""
import os
import stat
from pathlib import Path
from newapi import printe

statgroup = stat.S_IRWXU | stat.S_IRWXG
tool = os.getenv("HOME")
# ---
if not tool:
    tool = Path(__file__).parent
else:
    tool = Path(tool)
# ---
ta_dir = tool / "cookies"
# ---
if not ta_dir.exists():
    ta_dir.mkdir()
    printe.output("<<green>> mkdir:")
    printe.output(f"ta_dir:{ta_dir}")
    printe.output("<<green>> mkdir:")
    os.chmod(ta_dir, statgroup)

ta_tab = {}


def del_cookies_file(file_path):
    # ---
    file = Path(str(file_path))
    # ---
    if file.exists():
        file.unlink(missing_ok=True)
        printe.output("<<green>> unlink: file:{file}")


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
