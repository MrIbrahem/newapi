"""

from newapi.super.login_bots.r3_token_bot import get_r3_token

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}
WARNING: I:/core/bots/new/newapi/super/login_bots/bot.py:134: UserWarning:
def get_login_result(): Exception:{'login': {'result': 'Aborted', 'reason': 'Cannot log in when using MediaWiki\\Session\\BotPasswordSessionProvider sessions.'}}

WARNING: I:/core/bots/new/newapi/super/login_bots/bot.py:134: UserWarning:
def get_login_result(): Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 2 days before trying again.'}}

"""
import os
from pathlib import Path
from newapi import printe

import stat

statgroup = stat.S_IRWXU | stat.S_IRWXG
token_dir = Path(__file__).parent / "r3_tokens"
# ---
if not token_dir.exists():
    token_dir.mkdir()
    printe.output("<<green>> mkdir:")
    printe.output(f"token_dir:{token_dir}")
    printe.output("<<green>> mkdir:")
    os.chmod(token_dir, statgroup)

token_tab = {}

def get_file_name(lang, family, username):
    # ---
    lang = lang.lower()
    family = family.lower()
    # ---
    username = username.lower().replace(" ", "_").split("@")[0]
    # ---
    file = token_dir / f"{family}_{lang}_{username}.txt"
    # ---
    return file


def dump_r3_token(lang, family, username, r3_token):
    # ---
    token_tab.setdefault(family, {}).setdefault(lang, {})
    # ---
    token_tab[family][lang][username] = r3_token
    # ---
    file = get_file_name(lang, family, username)
    # ---
    try:
        with open(file, "w") as f:
            f.write(r3_token)
            os.chmod(str(file), statgroup)
    except Exception as e:
        printe.output(e)
    # ---
    return ""


def from_folder(lang, family, username):
    # ---
    file = get_file_name(lang, family, username)
    # ---
    r3_token = False
    # ---
    if file.exists():
        with open(file, "r") as f:
            r3_token = f.read()
    else:
        file.touch()
        os.chmod(str(file), statgroup)
    # ---
    return r3_token


def get_r3_token(lang, family, username):
    # ---
    r3_token = token_tab.get(family, {}).get(lang, {}).get(username, "")
    # ---
    if not r3_token:
        r3_token = from_folder(lang, family, username)
    # ---
    if not r3_token:
        printe.output(f" <<red>> get_r3_token: <<yellow>> [[{lang}:{family}]] user:{username} <<red>> not found")
        return "make_new"
    # ---
    return r3_token
