"""
Usage:

from newapi.wiki_page import CatDepth, CatDepthLogin
# CatDepthLogin(sitecode="en", family="wikipedia")
# cat_members = CatDepth(title, sitecode='en', family="wikipedia", depth=0, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])

from newapi.wiki_page import MainPage, NEW_API
# api_new = NEW_API('en', family='wikipedia')
# login    = api_new.Login_to_wiki()
# move_it  = api_new.move(old_title, to, reason="", noredirect=False, movesubpages=False)
# pages    = api_new.Find_pages_exists_or_not(liste, get_redirect=False)
# json1    = api_new.post_params(params, addtoken=False)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Parse_Text('{{subst:page_name}}', title)
# extlinks = api_new.get_extlinks(title)
# revisions= api_new.get_revisions(title)
# logs     = api_new.get_logs(title)
# wantedcats  = api_new.querypage_list(qppage='Wantedcategories', qplimit="max", Max=5000)
# pages  = api_new.Get_template_pages(title, namespace="*", Max=10000)
"""
# ---
import os
import sys
from newapi.super import bot_api
from newapi.super import super_page
from newapi.super import catdepth_new

from apis import user_account_new

# ---
home_dir = os.getenv("HOME")
tool = home_dir.split("/")[-1] if home_dir else None
# ---
pyy_file = __file__.replace("\\", "/").split("/")[-1]
# ---
User_tables = {
    "username": user_account_new.my_username,
    "password": user_account_new.my_password,
}
# ---
if "botuser" in sys.argv:
    User_tables = {
        "username": user_account_new.bot_username,
        "password": user_account_new.bot_password,
    }
    # ---
    print(f"{pyy_file} use {User_tables['username']} account.")
# ---
user_agent = super_page.default_user_agent()
# ---
super_page.User_tables["wikipedia"] = User_tables
bot_api.User_tables["wikipedia"] = User_tables
catdepth_new.User_tables["wikipedia"] = User_tables
# ---
super_page.User_tables["wikidata"] = User_tables
bot_api.User_tables["wikidata"] = User_tables
catdepth_new.User_tables["wikidata"] = User_tables
# ---
NEW_API = bot_api.NEW_API
MainPage = super_page.MainPage
change_codes = super_page.change_codes
CategoryDepth = catdepth_new.CategoryDepth
CatDepth = catdepth_new.subcatquery
CatDepthLogin = catdepth_new.login_wiki


def test():
    """
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
    """
    # ---
    page = MainPage("تصنيف:اليمن", "ar", family="wikipedia")
    # ---
    text = page.get_text()
    print(f"{len(text)=}")

    # ---
    # ex = page.page_backlinks()
    # print('---------------------------')
    # print(f'page_backlinks:{ex}')
    page2 = MainPage("Category:Yemen", "en", family="wikipedia")
    # ---
    text2 = page2.get_text()
    print(f"{len(text2)=}")
    # ---
    page_backlinks = page.page_backlinks()
    print("---------------------------")
    print(f"{len(page_backlinks)=}")

    # ---
    # ---
    # hidden_categories= page.get_hidden_categories()
    # print('---------------------------')
    # print(f'hidden_categories:{hidden_categories}')
    # ---
    cat_members = CatDepth("Association football players by nationality", sitecode="en", family="wikipedia", depth=0, ns="14")
    # ---
    print(f"{len(cat_members)=}")
    # ---
    red = page.page_links()
    print(f"{len(red)=}")
    # ---
    # save = page.save(newtext='')
    # api_new = NEW_API('en', family='wikipedia')
    # login   = api_new.Login_to_wiki()
    # pages   = api_new.Find_pages_exists_or_not(liste)
    # pages   = api_new.Get_Newpages()


if __name__ == "__main__":
    # python3 core8/pwb.py newapi/wiki_page
    # super_page.print_test[1] = True
    test()
