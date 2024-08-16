"""

python3 I:\core\bots\new\newapi\super\login_bots\jar.py

"""

import os
import requests
from http.cookiejar import MozillaCookieJar
from mwclient.client import Site
from pathlib import Path
Dir = Path(__file__).parent

BOT_USER = "Mr.Ibrahembot"
BOT_PASSWORD = "Mr.Ibrahembot@scfg6odf3s2kb8t3bbtu5v0h2dd0ssgl"

cookies_file = Dir / "cookies.txt"

cookie_jar = MozillaCookieJar(cookies_file)
if os.path.exists(cookies_file):
    # Load cookies from file, including session cookies
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
print("We have %d cookies" % len(cookie_jar))

connection = requests.Session()
connection.cookies = cookie_jar  # Tell Requests session to use the cookiejar.

site = Site("en.wikipedia.org", pool=connection)

if not site.logged_in:
    print("Logging in")
    site.login(BOT_USER, BOT_PASSWORD)

if site.logged_in:
    print("Already logged in as " + site.username)

# Save cookies to file, including session cookies
cookie_jar.save(ignore_discard=True, ignore_expires=True)

# ... rest of script
