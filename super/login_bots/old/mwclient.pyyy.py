import os
import requests
from http.cookiejar import MozillaCookieJar
from mwclient import Site

BOT_USER = "CHANGE-ME"
BOT_PASSWORD = "CHANGE-ME"

cookies_file = "cookies.txt"

cookie_jar = MozillaCookieJar(cookies_file)
if os.path.exists(cookies_file):
    # Load cookies from file, including session cookies
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
print("We have %d cookies" % len(cookie_jar))

connection = requests.Session()
connection.cookies = cookie_jar  # Tell Requests session to use the cookiejar.

site = Site("en.wikipedia.org", pool=connection)
if site.logged_in:
    print("Already logged in as " + site.username)
else:
    print("Logging in")
    site.login(BOT_USER, BOT_PASSWORD)

# Save cookies to file, including session cookies
cookie_jar.save(ignore_discard=True, ignore_expires=True)

# ... rest of script
