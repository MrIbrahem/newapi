"""

from newapi.super.login_bots.r3_token_bot import get_r3_token

Exception:{'login': {'result': 'Failed', 'reason': 'You have made too many recent login attempts. Please wait 5 minutes before trying again.'}}

"""
from pathlib import Path
from newapi import printe

# ---
tocken_dir = Path(__file__).parent / "r3_tokens"
# ---
if not tocken_dir.exists():
    tocken_dir.mkdir()
    printe.output("<<green>> mkdir:")
    printe.output(f"tocken_dir:{tocken_dir}")
    printe.output("<<green>> mkdir:")


def get_file_name(lang, family, username):
    # ---
    lang = lang.lower()
    family = family.lower()
    # ---
    username = username.lower().replace(" ", "_").split("@")[0]
    # ---
    file = tocken_dir / f"{family}_{lang}_{username}.txt"
    # ---
    return file


def dump_r3_token(lang, family, username, r3_token):
    # ---
    file = get_file_name(lang, family, username)
    # ---
    with open(file, "w") as f:
        f.write(r3_token)
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
    # ---
    return r3_token


def get_r3_token(lang, family, username):
    # ---
    r3_token = from_folder(lang, family, username)
    # ---
    if not r3_token:
        printe.output(f" <<red>> get_r3_token: <<yellow>> [[{lang}:{family}]] user:{username} <<red>> not found")
        return "make_new"
    # ---
    return r3_token
