r"""

from newapi.page import CatDepth, CatDepthLogin
# CatDepthLogin(sitecode="en", family="wikipedia")
# cat_members = CatDepth(title, sitecode='en', family="wikipedia", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])

match long ref:
    <ref[^>]*>[^<>]+<\/ref>

short ref:
    <ref[^>/]*\s*/\s*>
"""
# ---
import sys
from newapi import useraccount
from newapi.super import super_page
from newapi.super import super_login
from newapi.super import bot_api
from newapi.super import catdepth_new

# ---
User_tables = {
    "username": useraccount.username,
    "password": useraccount.password
}
# ---
himo_file = __file__.replace('\\', '/').split("/")[-1]
# ---
if "workibrahem" in sys.argv or himo_file == "himopage.py":
    User_tables['username'] = useraccount.hiacc
    User_tables['password'] = useraccount.hipass
    super_page.Edit_summary_line[1] = ' -Edit summary: %s: (will be removed)'
    # ---
    print(f"{himo_file} use Mr. Ibrahem account.")
    # ---
# ---
# xxxxxxxxxxx
# ---
super_login.User_tables["wikipedia"] = User_tables
super_login.User_tables["wikidata"] = User_tables
# ---
Login = super_login.Login
# ---
bot_api.login_def = Login
super_page.login_def = Login
catdepth_new.login_def = Login
# ---
NEW_API = bot_api.NEW_API
MainPage = super_page.MainPage
change_codes = super_page.change_codes
CatDepth = catdepth_new.subcatquery
CatDepthLogin = catdepth_new.login_wiki
# ---
# xxxxxxxxxxx


def test():
    '''
    page      = MainPage(title, 'ar', family='wikipedia')
    exists    = page.exists()
    text      = page.get_text()
    timestamp = page.get_timestamp()
    user      = page.get_user()
    links     = page.page_links()
    words     = page.get_words()
    purge     = page.purge()
    templates = page.get_templates()
    save_page = page.save(newtext='', summary='', nocreate=1, minor='')
    create    = page.Create(text='', summary='')
    '''
    # ---
    page = MainPage("تصنيف:اليمن", 'ar', family='wikipedia')
    # ---
    text = page.get_text()
    print(text)

    # ---
    # ex = page.page_backlinks()
    # print('---------------------------')
    # print(f'page_backlinks:{ex}')
    # ---
    # hidden_categories= page.get_hidden_categories()
    # print('---------------------------')
    # print(f'hidden_categories:{hidden_categories}')
    # ---
    # red = page.page_links()
    # print(f'page_links:{red}')
    # ---
    # save = page.save(newtext='')


# ---
if __name__ == '__main__':
    # python3 core8/pwb.py newapi/page
    super_page.print_test[1] = True
    super_login.print_test[1] = True
    test()
# ---
