# ---
"""
from newapi.mdwiki_page import MainPage as md_MainPage, CatDepth, CatDepthLogin
# CatDepthLogin(sitecode="en", family="wikipedia")
# cat_members = CatDepth(title, sitecode='en', family="wikipedia", depth=0, ns="all", nslist=[], onlyns=False, without_lang="", with_lang="", tempyes=[])

# from newapi.mdwiki_page import MainPage as md_MainPage
'''
page      = md_MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
# ---
page_edit = page.can_edit()
if not page_edit: return
# ---
if page.isRedirect() :  return
# target = page.get_redirect_target()
# ---
text        = page.get_text()
ns          = page.namespace()
links       = page.page_links()
categories  = page.get_categories(with_hidden=False)
langlinks   = page.get_langlinks()
wiki_links  = page.get_wiki_links_from_text()
refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
words       = page.get_words()
templates   = page.get_templates()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create      = page.Create(text='', summary='')
# ---
back_links  = page.page_backlinks()
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user        = page.get_user()
purge       = page.purge()
'''
"""
# ---
# import sys
from newapi.super import bot_api
from newapi.super import super_page
from newapi.super import catdepth_new

from apis import user_account_new

catdepth_new.SITECODE = "www"
catdepth_new.FAMILY = "mdwiki"

# ---
User_tables = {
    "username": user_account_new.my_username,
    "password": user_account_new.mdwiki_pass,
}
# ---
user_agent = super_page.default_user_agent()
# ---
super_page.User_tables["mdwiki"] = User_tables
bot_api.User_tables["mdwiki"] = User_tables
catdepth_new.User_tables["mdwiki"] = User_tables
# ---
NEW_API = bot_api.NEW_API

MainPage = super_page.MainPage
md_MainPage = MainPage

change_codes = super_page.change_codes
CatDepth = catdepth_new.subcatquery
CatDepthLogin = catdepth_new.login_wiki
# ---
# xxxxxxxxxxx


def test():
    """
    page      = MainPage(title, 'www', family='mdwiki')
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
    page = MainPage("User:Mr. Ibrahem/sandbox", "www", family="mdwiki")
    # ---
    text = page.get_text()
    print(f"{len(text)=}")
    # ---
    text_html   = page.get_text_html()
    # ---
    print('---------------------------')
    # print(text_html)
    print(f"{len(text_html)=}")
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
    # save = page.save(newtext=text + "\n{}")
    # api_new = NEW_API("www", family="mdwiki")
    # login   = api_new.Login_to_wiki()
    # pages   = api_new.Find_pages_exists_or_not(liste)
    # pages = api_new.Get_Newpages(limit=50)


# ---
if __name__ == "__main__":
    # python3 core8/pwb.py newapi/mdwiki_page
    # super_page.print_test[1] = True
    test()
